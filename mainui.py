# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'mainui.ui'
##
# Created by: Qt User Interface Compiler version 6.0.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from myQlistwidget import myQListWidget
import res


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        icon = QIcon()
        icon.addFile(u":/icon/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QTabWidget.Rounded)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileListWidget = myQListWidget(self.groupBox)
        self.fileListWidget.setObjectName(u"fileListWidget")
        self.fileListWidget.setDragEnabled(True)
        self.fileListWidget.setDragDropMode(QAbstractItemView.DragDrop)

        self.horizontalLayout.addWidget(self.fileListWidget)

        self.horizontalSpacer = QSpacerItem(
            20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.verticalLayout.setContentsMargins(-1, -1, 10, -1)
        self.btnFileUp = QPushButton(self.groupBox)
        self.btnFileUp.setObjectName(u"btnFileUp")
        self.btnFileUp.setMaximumSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.btnFileUp)

        self.btnFileDown = QPushButton(self.groupBox)
        self.btnFileDown.setObjectName(u"btnFileDown")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.btnFileDown.sizePolicy().hasHeightForWidth())
        self.btnFileDown.setSizePolicy(sizePolicy)
        self.btnFileDown.setMaximumSize(QSize(32, 32))

        self.verticalLayout.addWidget(self.btnFileDown)

        self.verticalSpacer_2 = QSpacerItem(
            20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.btnJoinFile = QPushButton(self.groupBox)
        self.btnJoinFile.setObjectName(u"btnJoinFile")
        self.btnJoinFile.setMinimumSize(QSize(100, 0))

        self.verticalLayout.addWidget(self.btnJoinFile)

        self.verticalSpacer_4 = QSpacerItem(
            20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.btnSaveFile = QPushButton(self.groupBox)
        self.btnSaveFile.setObjectName(u"btnSaveFile")
        self.btnSaveFile.setMinimumSize(QSize(100, 0))

        self.verticalLayout.addWidget(self.btnSaveFile)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(
            20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableView = QTableView(self.groupBox_2)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setStyleSheet(u"border-bottom: 1px solid #D8D8D8;\n"
                                     "border-right:1px solid #D8D8D8;")
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setDragDropMode(QAbstractItemView.InternalMove)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setGridStyle(Qt.SolidLine)

        self.horizontalLayout_2.addWidget(self.tableView)

        self.horizontalSpacer_2 = QSpacerItem(
            20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, -1, 10, -1)
        self.verticalSpacer_6 = QSpacerItem(
            20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_6)

        self.btnStartJob = QPushButton(self.groupBox_2)
        self.btnStartJob.setObjectName(u"btnStartJob")
        sizePolicy.setHeightForWidth(
            self.btnStartJob.sizePolicy().hasHeightForWidth())
        self.btnStartJob.setSizePolicy(sizePolicy)
        self.btnStartJob.setMinimumSize(QSize(100, 100))

        self.verticalLayout_3.addWidget(self.btnStartJob)

        self.btnAbout = QPushButton(self.groupBox_2)
        self.btnAbout.setObjectName(u"btnAbout")

        self.verticalLayout_3.addWidget(self.btnAbout)

        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.verticalLayout_2.addWidget(self.groupBox_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"\u5927\u67a3\u65e0\u635f\u89c6\u9891\u5408\u5e76\u5668", None))
        self.groupBox.setTitle(QCoreApplication.translate(
            "MainWindow", u"\u51c6\u5907\u5408\u5e76\u7684\u89c6\u9891", None))
        self.btnFileUp.setText(QCoreApplication.translate(
            "MainWindow", u"\u25b2", None))
        self.btnFileDown.setText(
            QCoreApplication.translate("MainWindow", u"\u25bc", None))
        self.btnJoinFile.setText(QCoreApplication.translate(
            "MainWindow", u"\u52a0\u5165\u89c6\u9891", None))
        self.btnSaveFile.setText(QCoreApplication.translate(
            "MainWindow", u"\u5408\u5e76\u89c6\u9891", None))
        self.groupBox_2.setTitle(QCoreApplication.translate(
            "MainWindow", u"\u5408\u5e76\u4efb\u52a1\u5217\u8868", None))
        self.btnStartJob.setText(QCoreApplication.translate(
            "MainWindow", u"\u5f00\u59cb\u5408\u5e76\u4efb\u52a1", None))
        self.btnAbout.setText(QCoreApplication.translate(
            "MainWindow", u"\u4f7f\u7528\u5e2e\u52a9", None))
    # retranslateUi
