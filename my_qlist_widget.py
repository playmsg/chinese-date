from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget


class MyQListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_ext = {"mp4", "mkv", "wmv", "avi", "flv"}

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            return
        event.ignore()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if not file_path:
                continue
            _, separator, suffix = file_path.rpartition(".")
            if separator and suffix.lower() in self.media_ext:
                self.addItem(file_path)
        event.acceptProposedAction()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self._delete_selected_items()
            return
        super().keyPressEvent(event)

    def _delete_selected_items(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))
