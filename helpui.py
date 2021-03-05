# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'helpui.ui'
##
# Created by: Qt User Interface Compiler version 6.0.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import res


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(563, 429)
        icon = QIcon()
        icon.addFile(u":/icon/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 20, 101, 91))
        self.label.setPixmap(QPixmap(u":/icon/icon.png"))
        self.label.setScaledContents(True)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 120, 311, 41))
        font = QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 160, 541, 201))
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 20, 511, 71))
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 90, 511, 91))
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(True)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(240, 380, 75, 24))

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.close)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate(
            "Dialog", u"\u4f7f\u7528\u5e2e\u52a9", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate(
            "Dialog", u"\u5927\u67a3\u65e0\u635f\u89c6\u9891\u5408\u5e76\u5668 2021-02\u7248", None))
        self.groupBox.setTitle(QCoreApplication.translate(
            "Dialog", u"\u5982\u4f55\u4f7f\u7528", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"      \u672c\u8f6f\u4ef6\u91c7\u7528Python+PySide6\u5f00\u53d1\uff0c\u8c03\u7528\u7684ffmpeg\u8fdb\u884c\u89c6\u9891\u5408\u5e76\u3002\u4e3b\u8981\u89e3\u51b3\u4e86\u4ee5\u5f80\u7684\u4e24\u4e2a\u95ee\u9898\uff1a\u4e00\u662f\u5408\u5e76\u89c6\u9891\u4e0d\u9700\u8981\u8f6c\u7801\uff0c\u4ec5\u4ec5\u662f\u5408\u5e76\u9700\u6c42\uff0c\u8fd9\u6837\u7684\u514d\u8d39\u8f6f\u4ef6\u8fd8\u4e0d\u592a\u597d\u627e\uff1b\u4e8c\u662f\u7c7b\u4f3c\u7684\u5408\u5e76\u8f6f\u4ef6\u4e0d\u652f\u6301\u4efb\u52a1\u5217\u8868\u65b9\u5f0f\uff0c\u4e00\u6b21\u53ea\u80fd\u5408\u5e76\u4e00\u4e2a\u76ee\u6807\u6587\u4ef6\uff0c\u4e0d\u5229\u4e8e\u5229\u7528\u534a\u591c\u95f2\u7f6e\u673a\u5668\u8fdb\u884c\u957f\u65f6\u95f4\u8fd0\u884c\u3002", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"      \u4f7f\u7528\u4e0a\u975e\u5e38\u7b80\u5355\uff0c\u53ea\u9700\u8981\u628a\u9700\u8981\u5408\u5e76\u7684\u89c6\u9891\u6587\u4ef6\u62d6\u653e\u8fdb\u5165\u4e0a\u65b9\u7684\u201c\u51c6\u5907\u5408\u5e76\u7684\u89c6\u9891\u201d\u5217\u8868\uff08\u6216\u8005\u70b9\u51fb\u201c\u52a0\u5165\u89c6\u9891\u201d\u6309\u94ae\u624b\u52a8\u9009\u62e9\u6587\u4ef6\u52a0\u5165\u5217\u8868\u4e5f\u53ef\u4ee5\uff09\uff0c\u7136\u540e\u70b9\u51fb\u201c\u5408\u5e76\u89c6\u9891\u201d\u6309\u94ae\uff0c\u8f93\u5165\u51c6\u5907\u5408\u5e76\u540e\u7684\u8def\u5f84\u53ca\u6587\u4ef6\u540d\uff0c\u90a3\u4e48\u8fd9\u4e2a\u51c6\u5907\u5408\u5e76\u7684\u6587\u4ef6\u5c31\u4f1a\u8fdb\u5165\u4e0b\u65b9\u7684\u201c\u5408\u5e76\u4efb\u52a1\u5217\u8868\u201d\u3002\u6b64\u64cd\u4f5c\u53cd\u590d\u591a\u6b21\uff0c\u53ef\u4ee5\u751f\u6210\u591a\u4e2a\u4efb\u52a1\u3002\u5f85\u4efb\u52a1\u51c6\u5907\u7ed3\u675f\u540e\uff0c\u70b9\u51fb\u4e0b\u65b9\u201c\u5f00\u59cb\u5408\u5e76\u4efb\u52a1\u201d\u6309\u94ae\uff0c\u5c06\u987a\u5e8f\u6267\u884c\u5408\u5e76"
                                                        "\u4efb\u52a1\u3002", None))
        self.pushButton.setText(QCoreApplication.translate(
            "Dialog", u"\u5173\u95ed", None))
    # retranslateUi
