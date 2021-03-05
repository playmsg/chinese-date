from PySide6.QtWidgets import QListView, QListWidget
from PySide6.QtCore import Qt
#from PySide6.QtGui import QStandardItemModel, QStandardItem


class myQListWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.mediaExt = ['mp4', 'mkv', 'wmv', 'avi']
        #self.filelistModel = QStandardItemModel()
        # self.setModel(self.filelistModel)

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pass

    def dropEvent(self, event):  # 放下文件后的动作
        for u in event.mimeData().urls():
            fileurl = str(u.toLocalFile())
            if fileurl.split(".")[-1].lower() in self.mediaExt:
                self.addItem(fileurl)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self._del_item()

    def _del_item(self):
        for item in self.selectedItems():
            self.takeItem(self.row(item))

        """
        flags = Qt.ItemIsEnabled | Qt.ItemIsDragEnabled | Qt.ItemIsSelectable

        for u in event.mimeData().urls():
            fileurl = str(u.toLocalFile())
            print(fileurl.split(".")[-1])
            if fileurl.split(".")[-1].lower() in self.mediaExt:
                filelistItem = QStandardItem(fileurl)
                filelistItem.setFlags(flags)
                self.filelistModel.appendRow(filelistItem)
        """
