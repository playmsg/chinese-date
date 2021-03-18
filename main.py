import logging
import os
import sys
import time
from queue import Queue
from PySide6.QtCore import (QObject, QProcess, Qt,
                            QThread)
from PySide6.QtGui import QStandardItem, QStandardItemModel
# import subprocess
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel,
                               QMainWindow, QMessageBox)

from helpui import Ui_Dialog
from mainui import Ui_MainWindow
jobQ = Queue()
logging.basicConfig(level=logging.NOTSET)


class helpWindow(QDialog, Ui_Dialog):
    def __init__(self):
        super(helpWindow, self).__init__()
        self.setupUi(self)


class logStatus(QThread):
    def __init__(self, jobListFile, joblist, jobtableviewIndex, parent=None):
        super().__init__()
        self.joblist = joblist
        self.jobListFile = jobListFile
        self.jobtableviewIndex = jobtableviewIndex

    def run(self):
        self.processStatus = ""
        self.logdict = {}
        logging.info(self.jobListFile+".proc")
        with open(self.jobListFile+".proc", 'r') as logFile:
            jobStatus = QStandardItem("开始处理")
            jobStatus.setTextAlignment(Qt.AlignCenter)
            self.joblist.setItem(self.jobtableviewIndex, 1, jobStatus)

            while self.processStatus != "end":
                time.sleep(0.5)
                loglist = logFile.readlines()
                for logvalue in loglist:
                    logvalueN = logvalue.replace("\n", "")
                    key, value = logvalueN.split("=", maxsplit=1)
                    self.logdict[key] = value
                self.processSpeed = self.logdict['speed']
                self.processStatus = self.logdict['progress']
                jobSpeed = QStandardItem(self.processSpeed)
                jobSpeed.setTextAlignment(Qt.AlignCenter)
                self.joblist.setItem(self.jobtableviewIndex, 1, jobSpeed)

            jobStatus = QStandardItem("已解决")
            jobStatus.setTextAlignment(Qt.AlignCenter)
            self.joblist.setItem(self.jobtableviewIndex, 1, jobStatus)
            self.exit(0)
        self.exit(1)


class watchjob(QObject):
    def __init__(self, joblist, ui):
        super(watchjob, self).__init__()
        self.joblist = joblist
        self.ui = ui

    def btn(self):
        while True:
            time.sleep(2)
            jobStatus = self.joblist.item(self.joblist.rowCount()-1, 1).text()
            logging.info("jobstatus:"+jobStatus)
            if jobStatus == "已解决":
                self.ui.btnStartJob.setEnabled(True)
                break


class job(QObject):
    def __init__(self, joblist):
        super(job, self).__init__()
        self.joblist = joblist

    def res(self,  exitCode,  exitStatus):
        logging.info("res code:")
        logging.info(exitStatus)

    def runJoinP(self):
        while True:
            if jobQ.empty():
                break
            jobQlist = jobQ.get()
            jobQ.task_done()
            jobListFile = jobQlist[0]
            jobOutFile = jobQlist[1]
            jobtableviewIndex = jobQlist[2]
            self.process = QProcess()
            self.process.setProgram("ffmpeg")
            # ffmpeg.exe -y -hwaccel cuda -f concat -safe 0 -i job1.txt -c copy 14.mp4 -progress job1out.txt
            self.process.setArguments(['-y', '-f', 'concat', '-safe', '0', '-i',
                                       jobListFile, '-c', 'copy', jobOutFile, '-progress', jobListFile+".proc", '-loglevel', 'quiet'])

            # self.process.startDetached()
            # logging.info(str(self.process.arguments()))
            # self.process.finished.connect(self.res)
            self.process.start()
            time.sleep(1)
            if os.path.exists(jobListFile):
                self._logStatus = logStatus(
                    jobListFile, self.joblist, jobtableviewIndex)
                self._logStatus.start()
                self._logStatus.wait()
            self.process.waitForFinished(-1)
            logging.info(self.process.state())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cwd = os.getcwd()
        self.ui.btnJoinFile.clicked.connect(self.joinFile)
        self.ui.btnFileUp.clicked.connect(self.fileUp)
        self.ui.btnFileDown.clicked.connect(self.fileDown)
        self.ui.btnSaveFile.clicked.connect(self.saveFile)
        self.ui.btnStartJob.clicked.connect(self.startJob)
        self.joblist = QStandardItemModel()
        self.joblist.setHorizontalHeaderLabels(['任务', '速度/进度'])
        self.ui.tableView.setModel(self.joblist)
        self.header = self.ui.tableView.horizontalHeader()
        self.header.setSectionResizeMode(0, self.header.Stretch)
        self.header.setSectionResizeMode(1, self.header.Fixed)
        self.header.resizeSection(1, 100)
        self.header.setStyleSheet(
            "QHeaderView::section{"
            "border-top:0px solid #D8D8D8;"
            "border-left:0px solid #D8D8D8;"
            "border-right:1px solid #D8D8D8;"
            "border-bottom: 1px solid #D8D8D8;"
            "background-color:white;"
            "padding:4px;"
            "}")
        aboutmeText = '''<a href="https://dvd3.net/2021/03/cdffmpeg/" style="color:gray">如果觉得有用给老哥点个赞>></a>'''
        self.ui.aboutlink = QLabel(aboutmeText)
        self.ui.aboutlink.setOpenExternalLinks(True)
        self.ui.statusbar.setStyleSheet("QStatusBar::item{border: 0px}")
        self.ui.statusbar.addPermanentWidget(self.ui.aboutlink)
        self.helpWindows = helpWindow()
        self.ui.btnAbout.clicked.connect(self.helpWindows.exec)

    def joinFile(self):
        fileName_choose, filetype = QFileDialog.getOpenFileNames(
            self, "文件保存", "", "视频文件 (*.mp4 *.avi *.mkv *.wmv)")
        if len(fileName_choose) > 0:
            self.ui.fileListWidget.addItems(fileName_choose)
            # logging.info(fileName_choose)

    def startJob(self):
        fineNum = 0
        self.ui.btnStartJob.setEnabled(False)
        QApplication.processEvents()
        if self.joblist.rowCount() == 0:
            QMessageBox.warning(self, "你有压力", "得先添加任务才能开始任务")
            self.ui.btnStartJob.setEnabled(True)
        else:
            for i in range(self.joblist.rowCount()):
                jobStatus = self.joblist.item(i, 1).text()
                logging.info("join job:"+jobStatus)
                if jobStatus == "未解决":
                    jobListFile = str(i+1)+".job"
                    jobOutFile = self.joblist.item(i, 0).text()
                    jobtableviewIndex = i
                    jobQlist = []
                    jobQlist.append(jobListFile)
                    jobQlist.append(jobOutFile)
                    jobQlist.append(jobtableviewIndex)
                    jobQ.put(jobQlist)
                    fineNum = fineNum+1
            if fineNum == 0:
                QMessageBox.warning(self, "你有压力", "当前所有任务已经完成，再戳也不会开始了")
                self.ui.btnStartJob.setEnabled(True)
            else:
                # 启动任务线程
                self.tJob = job(self.joblist)
                self.tJobThread = QThread()
                self.tJob.moveToThread(self.tJobThread)
                self.tJobThread.started.connect(self.tJob.runJoinP)
                self.tJobThread.start()
                self.tJobThread.exit(0)
                # 启动任务状态监视线程，实现按钮可用性调整
                self.watchJob = watchjob(self.joblist, self.ui)
                self.watchJobT = QThread()
                self.watchJob.moveToThread(self.watchJobT)
                self.watchJobT.started.connect(self.watchJob.btn)
                self.watchJobT.start()
                self.watchJobT.exit(0)

            # self.ui.btnStartJob.setEnabled(True)
            QApplication.processEvents()

    def saveFile(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                self.cwd,
                                                                "视频文件 (*.mp4 *.avi *.mkv *.wmv)")

        jobstat = QStandardItem("未解决")
        jobstat.setTextAlignment(Qt.AlignCenter)

        if fileName_choose != "":
            jobfilename = QStandardItem(fileName_choose)
            self.joblist.appendRow([jobfilename, jobstat])

            jobtaskname = str(self.joblist.rowCount())+".job"
            with open(jobtaskname, "w", encoding='utf-8') as jobfile:
                jobfile.writelines("#begin\n")
                listCount = self.ui.fileListWidget.count()
                for i in range(listCount):
                    mediaFile = "file "+"\'" + \
                        self.ui.fileListWidget.item(i).text()+"\'"
                    # logging.info(mediaFile)
                    jobfile.write(mediaFile+"\r")
            self.ui.fileListWidget.clear()

    def fileUp(self):
        currentRow = self.ui.fileListWidget.currentRow()
        currentItem = self.ui.fileListWidget.takeItem(currentRow)
        if currentRow > 0:
            newRow = currentRow-1
        else:
            newRow = currentRow

        self.ui.fileListWidget.insertItem(newRow, currentItem)
        self.ui.fileListWidget.setCurrentRow(newRow)

    def fileDown(self):
        currentRow = self.ui.fileListWidget.currentRow()
        currentItem = self.ui.fileListWidget.takeItem(currentRow)
        if currentRow < self.ui.fileListWidget.count():
            newRow = currentRow+1
        else:
            newRow = currentRow
        self.ui.fileListWidget.insertItem(newRow, currentItem)
        self.ui.fileListWidget.setCurrentRow(newRow)

    def closeEvent(self, e):
        res = QMessageBox.question(
            self, "你有压力", "退出后未完成的任务列表将被清空，是否继续退出？", QMessageBox.Cancel | QMessageBox.Ok)
        if res == QMessageBox.Ok:
            fileList = os.scandir('.')
            for sFile in fileList:
                if sFile.is_file() and sFile.name.split(".")[-1].lower() == "job" and sFile.name.split(".")[0].lower().isdigit():
                    logging.info(os.getcwd()+"\\"+sFile.name)
                    jobfile = os.getcwd()+"\\"+sFile.name
                    jobfilelog = os.getcwd()+"\\"+sFile.name+".proc"
                    os.remove(jobfile)
                    if os.path.exists(jobfilelog):
                        os.remove(jobfilelog)
            e.accept()
        else:
            e.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()
    sys.exit(app.exec_())
