import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QThread, Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
)

from help_ui import Ui_Dialog
from main_ui import Ui_MainWindow

logging.basicConfig(level=logging.INFO)

JOB_PENDING = "未解决"
JOB_RUNNING = "开始处理"
JOB_DONE = "已解决"
JOB_FAILED = "失败"

INPUT_FILTER = "视频文件 (*.mp4 *.avi *.mkv *.wmv *.flv)"
OUTPUT_FILTER = "视频文件 (*.mp4 *.avi *.mkv *.wmv)"
MP4_LIKE_SUFFIXES = {".mp4", ".m4v", ".mov"}


@dataclass(slots=True)
class JobTask:
    list_file: Path
    output_file: Path
    row_index: int


def build_concat_line(file_path: str) -> str:
    normalized_path = file_path.replace("\\", "/")
    escaped_path = normalized_path.replace("'", r"'\''")
    return f"file '{escaped_path}'\n"


def build_ffmpeg_command(list_file: Path, output_file: Path) -> list[str]:
    command = [
        "ffmpeg",
        "-hide_banner",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-map",
        "0",
        "-c",
        "copy",
    ]
    if output_file.suffix.lower() in MP4_LIKE_SUFFIXES:
        command.extend(["-movflags", "+faststart"])
    command.extend(["-progress", "pipe:1", "-nostats", str(output_file)])
    return command


class HelpWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class JobWorker(QThread):
    status_changed = Signal(int, str)
    job_error = Signal(int, str)
    all_finished = Signal()

    def __init__(self, tasks: list[JobTask], parent=None):
        super().__init__(parent)
        self.tasks = tasks

    def run(self):
        try:
            for task in self.tasks:
                if self.isInterruptionRequested():
                    break
                self._run_single_task(task)
        finally:
            self.all_finished.emit()

    def _run_single_task(self, task: JobTask):
        self.status_changed.emit(task.row_index, JOB_RUNNING)
        command = build_ffmpeg_command(task.list_file, task.output_file)
        logging.info("Running ffmpeg: %s", " ".join(command))
        try:
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
            ) as process:
                if process.stdout is not None:
                    for raw_line in process.stdout:
                        line = raw_line.strip()
                        if not line:
                            continue
                        if "=" not in line:
                            logging.info(line)
                            continue
                        key, value = line.split("=", maxsplit=1)
                        if key == "speed":
                            self.status_changed.emit(task.row_index, value)
                return_code = process.wait()
            if return_code == 0:
                self.status_changed.emit(task.row_index, JOB_DONE)
                return
            self.status_changed.emit(task.row_index, JOB_FAILED)
            self.job_error.emit(
                task.row_index,
                f"{task.output_file.name} 合并失败，ffmpeg 退出码: {return_code}",
            )
        except Exception as exc:  # pragma: no cover - UI runtime path
            logging.exception("Failed to run ffmpeg for task %s", task.output_file)
            self.status_changed.emit(task.row_index, JOB_FAILED)
            self.job_error.emit(task.row_index, f"{task.output_file.name} 合并异常: {exc}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cwd = os.getcwd()
        self.worker: JobWorker | None = None
        self.worker_errors: list[str] = []

        self.ui.btnJoinFile.clicked.connect(self.join_file)
        self.ui.btnFileUp.clicked.connect(self.file_up)
        self.ui.btnFileDown.clicked.connect(self.file_down)
        self.ui.btnSaveFile.clicked.connect(self.save_file)
        self.ui.btnStartJob.clicked.connect(self.start_job)
        self.ui.btnAbout.clicked.connect(self._open_help)

        self.joblist = QStandardItemModel()
        self.joblist.setHorizontalHeaderLabels(["任务", "速度/进度"])
        self.ui.tableView.setModel(self.joblist)
        self._setup_table_view()
        self._setup_status_bar()
        self.help_window = HelpWindow()

        if shutil.which("ffmpeg") is None:
            QMessageBox.critical(self, "你有压力", "ffmpeg.exe 不存在或者没有加入环境变量")
            sys.exit(1)

    def _setup_table_view(self):
        header = self.ui.tableView.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.Fixed)
        header.resizeSection(1, 100)
        header.setStyleSheet(
            "QHeaderView::section{"
            "border-top:0px solid #D8D8D8;"
            "border-left:0px solid #D8D8D8;"
            "border-right:1px solid #D8D8D8;"
            "border-bottom:1px solid #D8D8D8;"
            "background-color:white;"
            "padding:4px;"
            "}"
        )

    def _setup_status_bar(self):
        aboutme_text = (
            '<a href="https://dvd3.net/2021/03/cdffmpeg/" style="color:gray">'
            "如果觉得有用给老哥点个赞>></a>"
        )
        about_link = QLabel(aboutme_text)
        about_link.setOpenExternalLinks(True)
        self.ui.statusbar.setStyleSheet("QStatusBar::item{border: 0px}")
        self.ui.statusbar.addPermanentWidget(about_link)

    def _open_help(self):
        self.help_window.exec()

    def _set_controls_enabled(self, enabled: bool):
        self.ui.btnStartJob.setEnabled(enabled)
        self.ui.btnJoinFile.setEnabled(enabled)
        self.ui.btnSaveFile.setEnabled(enabled)

    def _set_job_status(self, row_index: int, text: str):
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        self.joblist.setItem(row_index, 1, item)

    def join_file(self):
        selected_files, _ = QFileDialog.getOpenFileNames(self, "选择视频文件", None, INPUT_FILTER)
        if selected_files:
            self.ui.fileListWidget.addItems(selected_files)

    def start_job(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, "你有压力", "任务正在执行中，请先等待当前任务结束")
            return

        if self.joblist.rowCount() == 0:
            QMessageBox.warning(self, "你有压力", "得先添加任务才能开始任务")
            return

        tasks: list[JobTask] = []
        self.worker_errors = []
        for row_index in range(self.joblist.rowCount()):
            status_item = self.joblist.item(row_index, 1)
            output_item = self.joblist.item(row_index, 0)
            if status_item is None or output_item is None:
                continue
            if status_item.text() != JOB_PENDING:
                continue
            job_list_file = Path(f"{row_index + 1}.job")
            if not job_list_file.exists():
                self._set_job_status(row_index, JOB_FAILED)
                self.worker_errors.append(f"{output_item.text()} 缺少任务文件: {job_list_file}")
                continue
            tasks.append(
                JobTask(
                    list_file=job_list_file,
                    output_file=Path(output_item.text()),
                    row_index=row_index,
                )
            )

        if not tasks:
            message = "当前所有任务已经完成，再戳也不会开始了"
            if self.worker_errors:
                message = "当前没有可执行任务，且发现任务文件缺失，请重新添加任务"
            QMessageBox.warning(self, "你有压力", message)
            return

        self._set_controls_enabled(False)
        self.worker = JobWorker(tasks, self)
        self.worker.status_changed.connect(self._set_job_status)
        self.worker.job_error.connect(self._on_job_error)
        self.worker.all_finished.connect(self._on_all_jobs_finished)
        self.worker.start()

    def _on_job_error(self, row_index: int, message: str):
        logging.error("Job %s failed: %s", row_index, message)
        self.worker_errors.append(message)

    def _on_all_jobs_finished(self):
        self._set_controls_enabled(True)
        if self.worker_errors:
            preview_count = min(len(self.worker_errors), 5)
            details = "\n".join(self.worker_errors[:preview_count])
            extra = ""
            if len(self.worker_errors) > preview_count:
                extra = f"\n... 还有 {len(self.worker_errors) - preview_count} 条错误"
            QMessageBox.warning(self, "合并任务完成（含失败）", details + extra)
        self.worker = None

    def save_file(self):
        list_count = self.ui.fileListWidget.count()
        if list_count == 0:
            QMessageBox.warning(self, "你有压力", "请先加入至少一个视频文件")
            return

        first_input_filename = self.ui.fileListWidget.item(0).text()
        base_name = os.path.splitext(os.path.basename(first_input_filename))[0]
        ext_name = os.path.splitext(os.path.basename(first_input_filename))[1]
        default_save_filename = f"{base_name}_合并视频{ext_name}"
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "文件保存",
            os.path.join(self.cwd, default_save_filename),
            OUTPUT_FILTER,
        )
        if not save_path:
            return

        job_file_name = f"{self.joblist.rowCount() + 1}.job"
        with open(job_file_name, "w", encoding="utf-8", newline="\n") as job_file:
            job_file.write("# generated by chinese-date\n")
            for index in range(list_count):
                media_file = self.ui.fileListWidget.item(index).text()
                job_file.write(build_concat_line(media_file))

        job_name_item = QStandardItem(save_path)
        job_status_item = QStandardItem(JOB_PENDING)
        job_status_item.setTextAlignment(Qt.AlignCenter)
        self.joblist.appendRow([job_name_item, job_status_item])
        self.ui.fileListWidget.clear()

    def file_up(self):
        current_row = self.ui.fileListWidget.currentRow()
        if current_row <= 0:
            return
        current_item = self.ui.fileListWidget.takeItem(current_row)
        if current_item is None:
            return
        new_row = current_row - 1
        self.ui.fileListWidget.insertItem(new_row, current_item)
        self.ui.fileListWidget.setCurrentRow(new_row)

    def file_down(self):
        current_row = self.ui.fileListWidget.currentRow()
        last_row = self.ui.fileListWidget.count() - 1
        if current_row < 0 or current_row >= last_row:
            return
        current_item = self.ui.fileListWidget.takeItem(current_row)
        if current_item is None:
            return
        new_row = current_row + 1
        self.ui.fileListWidget.insertItem(new_row, current_item)
        self.ui.fileListWidget.setCurrentRow(new_row)

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "你有压力", "当前任务还在执行，请等待合并完成后再退出")
            event.ignore()
            return

        if self.joblist.rowCount() == 0:
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "你有压力",
            "退出后未完成的任务列表将被清空，是否继续退出？",
            QMessageBox.Cancel | QMessageBox.Ok,
        )
        if reply != QMessageBox.Ok:
            event.ignore()
            return

        for pending_job_file in Path(".").glob("*.job"):
            if pending_job_file.stem.isdigit():
                pending_job_file.unlink(missing_ok=True)
        for pending_log_file in Path(".").glob("*.job.proc"):
            if pending_log_file.name.split(".")[0].isdigit():
                pending_log_file.unlink(missing_ok=True)
        event.accept()


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
