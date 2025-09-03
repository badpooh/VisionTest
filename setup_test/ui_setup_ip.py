# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setup_ip.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_setup_ip(object):
    def setupUi(self, setup_ip):
        if not setup_ip.objectName():
            setup_ip.setObjectName(u"setup_ip")
        setup_ip.resize(720, 480)
        self.widget = QWidget(setup_ip)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 720, 480))
        self.widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.btn_ip_add = QPushButton(self.widget)
        self.btn_ip_add.setObjectName(u"btn_ip_add")
        self.btn_ip_add.setGeometry(QRect(180, 90, 75, 24))
        self.btn_ip_select = QPushButton(self.widget)
        self.btn_ip_select.setObjectName(u"btn_ip_select")
        self.btn_ip_select.setGeometry(QRect(180, 170, 75, 24))
        self.btn_ip_del = QPushButton(self.widget)
        self.btn_ip_del.setObjectName(u"btn_ip_del")
        self.btn_ip_del.setGeometry(QRect(180, 120, 75, 24))
        self.ip_typing = QLineEdit(self.widget)
        self.ip_typing.setObjectName(u"ip_typing")
        self.ip_typing.setGeometry(QRect(20, 90, 151, 31))
        self.ip_list = QTableWidget(self.widget)
        if (self.ip_list.columnCount() < 1):
            self.ip_list.setColumnCount(1)
        self.ip_list.setObjectName(u"ip_list")
        self.ip_list.setGeometry(QRect(20, 150, 151, 191))
        self.ip_list.setFrameShape(QFrame.Shape.Panel)
        self.ip_list.setFrameShadow(QFrame.Shadow.Plain)
        self.ip_list.setLineWidth(2)
        self.ip_list.setMidLineWidth(0)
        self.ip_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ip_list.setRowCount(0)
        self.ip_list.setColumnCount(1)
        self.ip_list.horizontalHeader().setVisible(True)
        self.tp_typing = QLineEdit(self.widget)
        self.tp_typing.setObjectName(u"tp_typing")
        self.tp_typing.setGeometry(QRect(310, 90, 90, 30))
        self.sp_typing = QLineEdit(self.widget)
        self.sp_typing.setObjectName(u"sp_typing")
        self.sp_typing.setGeometry(QRect(520, 90, 90, 30))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(60, 60, 91, 21))
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(320, 60, 91, 21))
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(530, 60, 91, 21))
        self.btn_tp_add = QPushButton(self.widget)
        self.btn_tp_add.setObjectName(u"btn_tp_add")
        self.btn_tp_add.setGeometry(QRect(420, 90, 75, 24))
        self.btn_tp_select = QPushButton(self.widget)
        self.btn_tp_select.setObjectName(u"btn_tp_select")
        self.btn_tp_select.setGeometry(QRect(420, 170, 75, 24))
        self.btn_tp_del = QPushButton(self.widget)
        self.btn_tp_del.setObjectName(u"btn_tp_del")
        self.btn_tp_del.setGeometry(QRect(420, 120, 75, 24))
        self.btn_sp_del = QPushButton(self.widget)
        self.btn_sp_del.setObjectName(u"btn_sp_del")
        self.btn_sp_del.setGeometry(QRect(630, 120, 75, 24))
        self.btn_sp_select = QPushButton(self.widget)
        self.btn_sp_select.setObjectName(u"btn_sp_select")
        self.btn_sp_select.setGeometry(QRect(630, 170, 75, 24))
        self.btn_sp_add = QPushButton(self.widget)
        self.btn_sp_add.setObjectName(u"btn_sp_add")
        self.btn_sp_add.setGeometry(QRect(630, 90, 75, 24))
        self.tp_list = QTableWidget(self.widget)
        if (self.tp_list.columnCount() < 1):
            self.tp_list.setColumnCount(1)
        self.tp_list.setObjectName(u"tp_list")
        self.tp_list.setGeometry(QRect(300, 150, 111, 191))
        self.tp_list.setFrameShape(QFrame.Shape.Panel)
        self.tp_list.setFrameShadow(QFrame.Shadow.Plain)
        self.tp_list.setLineWidth(2)
        self.tp_list.setMidLineWidth(0)
        self.tp_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tp_list.setRowCount(0)
        self.tp_list.setColumnCount(1)
        self.tp_list.horizontalHeader().setVisible(False)
        self.sp_list = QTableWidget(self.widget)
        if (self.sp_list.columnCount() < 1):
            self.sp_list.setColumnCount(1)
        self.sp_list.setObjectName(u"sp_list")
        self.sp_list.setGeometry(QRect(510, 150, 111, 191))
        self.sp_list.setFrameShape(QFrame.Shape.Panel)
        self.sp_list.setFrameShadow(QFrame.Shadow.Plain)
        self.sp_list.setLineWidth(2)
        self.sp_list.setMidLineWidth(0)
        self.sp_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.sp_list.setRowCount(0)
        self.sp_list.setColumnCount(1)
        self.sp_list.horizontalHeader().setVisible(False)

        self.retranslateUi(setup_ip)

        QMetaObject.connectSlotsByName(setup_ip)
    # setupUi

    def retranslateUi(self, setup_ip):
        setup_ip.setWindowTitle(QCoreApplication.translate("setup_ip", u"Form", None))
        self.btn_ip_add.setText(QCoreApplication.translate("setup_ip", u"Add", None))
        self.btn_ip_select.setText(QCoreApplication.translate("setup_ip", u"Select", None))
        self.btn_ip_del.setText(QCoreApplication.translate("setup_ip", u"Del", None))
        self.label.setText(QCoreApplication.translate("setup_ip", u"IP ADDRESS", None))
        self.label_2.setText(QCoreApplication.translate("setup_ip", u"TOUCH PORT", None))
        self.label_3.setText(QCoreApplication.translate("setup_ip", u"SETUP PORT", None))
        self.btn_tp_add.setText(QCoreApplication.translate("setup_ip", u"T.P Add", None))
        self.btn_tp_select.setText(QCoreApplication.translate("setup_ip", u"T.P Select", None))
        self.btn_tp_del.setText(QCoreApplication.translate("setup_ip", u"T.P Del", None))
        self.btn_sp_del.setText(QCoreApplication.translate("setup_ip", u"S.P Del", None))
        self.btn_sp_select.setText(QCoreApplication.translate("setup_ip", u"S.P Select", None))
        self.btn_sp_add.setText(QCoreApplication.translate("setup_ip", u"S.P Add", None))
    # retranslateUi

