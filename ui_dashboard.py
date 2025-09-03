# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dashboard.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QSize(1280, 720))
        MainWindow.setStyleSheet(u"background-color: rgb(245, 250, 254);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_menu = QWidget(self.centralwidget)
        self.main_menu.setObjectName(u"main_menu")
        self.verticalLayout_5 = QVBoxLayout(self.main_menu)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.stackedWidget = QStackedWidget(self.main_menu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        font = QFont()
        font.setPointSize(20)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        self.label_4 = QLabel(self.home_page)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 10, 48, 16))
        self.stackedWidget.addWidget(self.home_page)
        self.ui_test_page = QWidget()
        self.ui_test_page.setObjectName(u"ui_test_page")
        self.gridLayout_3 = QGridLayout(self.ui_test_page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.menu_widget = QWidget(self.ui_test_page)
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_widget.setMinimumSize(QSize(0, 100))
        self.menu_widget.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_6 = QHBoxLayout(self.menu_widget)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_test_start = QPushButton(self.menu_widget)
        self.btn_test_start.setObjectName(u"btn_test_start")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_test_start.sizePolicy().hasHeightForWidth())
        self.btn_test_start.setSizePolicy(sizePolicy)
        self.btn_test_start.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.btn_test_start)

        self.btn_test_stop = QPushButton(self.menu_widget)
        self.btn_test_stop.setObjectName(u"btn_test_stop")

        self.horizontalLayout_6.addWidget(self.btn_test_stop)

        self.horizontalSpacer_2 = QSpacerItem(725, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_2 = QWidget(self.menu_widget)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_add_tc = QPushButton(self.widget_2)
        self.btn_add_tc.setObjectName(u"btn_add_tc")

        self.horizontalLayout_4.addWidget(self.btn_add_tc)

        self.btn_del_tc = QPushButton(self.widget_2)
        self.btn_del_tc.setObjectName(u"btn_del_tc")

        self.horizontalLayout_4.addWidget(self.btn_del_tc)

        self.btn_tc_save = QPushButton(self.widget_2)
        self.btn_tc_save.setObjectName(u"btn_tc_save")

        self.horizontalLayout_4.addWidget(self.btn_tc_save)

        self.btn_tc_load = QPushButton(self.widget_2)
        self.btn_tc_load.setObjectName(u"btn_tc_load")

        self.horizontalLayout_4.addWidget(self.btn_tc_load)


        self.verticalLayout_7.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.menu_widget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cb_accurasm = QCheckBox(self.widget_3)
        self.cb_accurasm.setObjectName(u"cb_accurasm")
        self.cb_accurasm.setChecked(True)

        self.horizontalLayout_5.addWidget(self.cb_accurasm)


        self.verticalLayout_7.addWidget(self.widget_3)


        self.horizontalLayout_6.addLayout(self.verticalLayout_7)


        self.verticalLayout_6.addWidget(self.menu_widget)

        self.tc_widget = QWidget(self.ui_test_page)
        self.tc_widget.setObjectName(u"tc_widget")
        self.tc_widget.setMinimumSize(QSize(0, 500))
        self.horizontalLayout = QHBoxLayout(self.tc_widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tableWidget = QTableWidget(self.tc_widget)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setStyleSheet(u"QHeaderView::section {\n"
"	border-bottom: 10px solid black;\n"
"}")
        self.tableWidget.setFrameShape(QFrame.Shape.Box)
        self.tableWidget.setFrameShadow(QFrame.Shadow.Sunken)
        self.tableWidget.setLineWidth(1)
        self.tableWidget.setMidLineWidth(1)
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setGridStyle(Qt.PenStyle.SolidLine)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)

        self.horizontalLayout.addWidget(self.tableWidget)


        self.verticalLayout_6.addWidget(self.tc_widget)


        self.gridLayout_3.addLayout(self.verticalLayout_6, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.ui_test_page)
        self.setup_test_page = QWidget()
        self.setup_test_page.setObjectName(u"setup_test_page")
        self.stackedWidget.addWidget(self.setup_test_page)
        self.frame_test_page = QWidget()
        self.frame_test_page.setObjectName(u"frame_test_page")
        self.btn_select_webcam = QPushButton(self.frame_test_page)
        self.btn_select_webcam.setObjectName(u"btn_select_webcam")
        self.btn_select_webcam.setGeometry(QRect(20, 30, 101, 31))
        self.btn_select_webcam.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    color: black;\n"
"}\n"
"QPushButton:checked {\n"
"    background-color: black;\n"
"    color: white;\n"
"    border: 1px solid black;\n"
"}")
        self.btn_select_webcam.setCheckable(True)
        self.btn_start_webcam = QPushButton(self.frame_test_page)
        self.btn_start_webcam.setObjectName(u"btn_start_webcam")
        self.btn_start_webcam.setGeometry(QRect(30, 90, 75, 24))
        self.btn_stop_webcam = QPushButton(self.frame_test_page)
        self.btn_stop_webcam.setObjectName(u"btn_stop_webcam")
        self.btn_stop_webcam.setGeometry(QRect(120, 90, 75, 24))
        self.label_5 = QLabel(self.frame_test_page)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(40, 140, 71, 16))
        self.lineEdit = QLineEdit(self.frame_test_page)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(40, 170, 113, 31))
        self.stackedWidget.addWidget(self.frame_test_page)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.stackedWidget.addWidget(self.page_5)

        self.verticalLayout_5.addWidget(self.stackedWidget)


        self.gridLayout.addWidget(self.main_menu, 1, 2, 1, 1)

        self.condition_bar = QWidget(self.centralwidget)
        self.condition_bar.setObjectName(u"condition_bar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.condition_bar.sizePolicy().hasHeightForWidth())
        self.condition_bar.setSizePolicy(sizePolicy2)
        self.condition_bar.setMinimumSize(QSize(0, 70))
        self.gridLayout_4 = QGridLayout(self.condition_bar)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer = QSpacerItem(868, 19, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.tp_display = QLabel(self.condition_bar)
        self.tp_display.setObjectName(u"tp_display")
        self.tp_display.setMinimumSize(QSize(60, 30))
        self.tp_display.setFrameShape(QFrame.Shape.WinPanel)
        self.tp_display.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.tp_display, 1, 5, 1, 1)

        self.btn_setting = QPushButton(self.condition_bar)
        self.btn_setting.setObjectName(u"btn_setting")
        self.btn_setting.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        padding: 5 10px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.btn_setting.setCheckable(False)
        self.btn_setting.setAutoDefault(False)

        self.gridLayout_4.addWidget(self.btn_setting, 1, 0, 1, 1)

        self.btn_all_connect = QPushButton(self.condition_bar)
        self.btn_all_connect.setObjectName(u"btn_all_connect")
        self.btn_all_connect.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        padding: 5 10px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.btn_all_connect.setCheckable(False)

        self.gridLayout_4.addWidget(self.btn_all_connect, 1, 1, 1, 1)

        self.ip_display = QLabel(self.condition_bar)
        self.ip_display.setObjectName(u"ip_display")
        self.ip_display.setMinimumSize(QSize(130, 30))
        self.ip_display.setFrameShape(QFrame.Shape.WinPanel)
        self.ip_display.setFrameShadow(QFrame.Shadow.Raised)
        self.ip_display.setLineWidth(1)

        self.gridLayout_4.addWidget(self.ip_display, 1, 4, 1, 1)

        self.btn_all_disconnect = QPushButton(self.condition_bar)
        self.btn_all_disconnect.setObjectName(u"btn_all_disconnect")
        self.btn_all_disconnect.setStyleSheet(u"QPushButton {\n"
"        border: 1px solid #8f8f91;\n"
"        border-radius: 5px;\n"
"        padding: 5 10px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"        background-color: #d0d0d0;\n"
"    }")
        self.btn_all_disconnect.setCheckable(False)
        self.btn_all_disconnect.setChecked(False)
        self.btn_all_disconnect.setFlat(False)

        self.gridLayout_4.addWidget(self.btn_all_disconnect, 1, 2, 1, 1)

        self.label_6 = QLabel(self.condition_bar)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFrameShape(QFrame.Shape.Box)
        self.label_6.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.label_6, 0, 4, 1, 1)

        self.label_7 = QLabel(self.condition_bar)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFrameShape(QFrame.Shape.Box)
        self.label_7.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.label_7, 0, 5, 1, 1)

        self.sp_display = QLabel(self.condition_bar)
        self.sp_display.setObjectName(u"sp_display")
        self.sp_display.setMinimumSize(QSize(60, 30))
        self.sp_display.setFrameShape(QFrame.Shape.WinPanel)
        self.sp_display.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.sp_display, 1, 6, 1, 1)

        self.label_9 = QLabel(self.condition_bar)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFrameShape(QFrame.Shape.Box)
        self.label_9.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.label_9, 0, 6, 1, 1)

        self.label_10 = QLabel(self.condition_bar)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFrameShape(QFrame.Shape.Box)
        self.label_10.setFrameShadow(QFrame.Shadow.Raised)

        self.gridLayout_4.addWidget(self.label_10, 0, 0, 1, 2)


        self.gridLayout.addWidget(self.condition_bar, 0, 2, 1, 1, Qt.AlignmentFlag.AlignVCenter)

        self.icon_name_widget = QWidget(self.centralwidget)
        self.icon_name_widget.setObjectName(u"icon_name_widget")
        self.icon_name_widget.setEnabled(True)
        self.icon_name_widget.setMinimumSize(QSize(0, 0))
        self.icon_name_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(175, 221, 236);\n"
"}\n"
"\n"
"QPushButton {\n"
"	color:black;\n"
"	text-align:left;\n"
"	height:30px;\n"
"	border:none;\n"
"	padding-left:10px;\n"
"	border-top-left-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color:#F5FAFE;\n"
"	font-weight:bold;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(self.icon_name_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.icon_name_widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(40, 40))
        self.label_2.setMaximumSize(QSize(40, 40))
        self.label_2.setPixmap(QPixmap(u":/images/Rootech.png"))
        self.label_2.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.icon_name_widget)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_3.setFont(font1)

        self.horizontalLayout_3.addWidget(self.label_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.pushButton_12 = QPushButton(self.icon_name_widget)
        self.pushButton_12.setObjectName(u"pushButton_12")
        icon = QIcon()
        icon.addFile(u":/images/dashboard.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_12.setIcon(icon)
        self.pushButton_12.setCheckable(True)
        self.pushButton_12.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.pushButton_12)

        self.btn_home_2 = QPushButton(self.icon_name_widget)
        self.btn_home_2.setObjectName(u"btn_home_2")
        icon1 = QIcon()
        icon1.addFile(u":/images/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_home_2.setIcon(icon1)
        self.btn_home_2.setCheckable(True)
        self.btn_home_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_home_2)

        self.btn_ui_test_2 = QPushButton(self.icon_name_widget)
        self.btn_ui_test_2.setObjectName(u"btn_ui_test_2")
        icon2 = QIcon()
        icon2.addFile(u":/images/brand_family.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_ui_test_2.setIcon(icon2)
        self.btn_ui_test_2.setCheckable(True)
        self.btn_ui_test_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_ui_test_2)

        self.btn_demo_test = QPushButton(self.icon_name_widget)
        self.btn_demo_test.setObjectName(u"btn_demo_test")
        icon3 = QIcon()
        icon3.addFile(u":/images/computer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_demo_test.setIcon(icon3)
        self.btn_demo_test.setCheckable(True)
        self.btn_demo_test.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_demo_test)

        self.btn_frame_test_2 = QPushButton(self.icon_name_widget)
        self.btn_frame_test_2.setObjectName(u"btn_frame_test_2")
        icon4 = QIcon()
        icon4.addFile(u":/images/videocam.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_frame_test_2.setIcon(icon4)
        self.btn_frame_test_2.setCheckable(True)
        self.btn_frame_test_2.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.btn_frame_test_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 383, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.pushButton_7 = QPushButton(self.icon_name_widget)
        self.pushButton_7.setObjectName(u"pushButton_7")
        icon5 = QIcon()
        icon5.addFile(u":/images/logout.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_7.setIcon(icon5)
        self.pushButton_7.setCheckable(True)

        self.verticalLayout_4.addWidget(self.pushButton_7)


        self.gridLayout.addWidget(self.icon_name_widget, 0, 1, 2, 1)

        self.icon_only_widget = QWidget(self.centralwidget)
        self.icon_only_widget.setObjectName(u"icon_only_widget")
        self.icon_only_widget.setMinimumSize(QSize(0, 0))
        self.icon_only_widget.setMaximumSize(QSize(70, 16777215))
        self.icon_only_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(175, 221, 236);\n"
"}\n"
"\n"
"QPushButton {\n"
"	color:black;\n"
"	text-align:center;\n"
"	height:30px;\n"
"	border:none;\n"
"	border-top-left-radius:10px;\n"
"	border-bottom-left-radius:10px;\n"
"	border-top-right-radius:10px;\n"
"	border-bottom-right-radius:10px;\n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color:#F5FAFE;\n"
"	font-weight:bold;\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.label = QLabel(self.icon_only_widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 40))
        self.label.setMaximumSize(QSize(40, 40))
        self.label.setPixmap(QPixmap(u":/images/Rootech.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.label)

        self.horizontalSpacer_4 = QSpacerItem(18, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 15, -1, -1)
        self.pushButton_3 = QPushButton(self.icon_only_widget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setIcon(icon)
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.pushButton_3)

        self.btn_home_1 = QPushButton(self.icon_only_widget)
        self.btn_home_1.setObjectName(u"btn_home_1")
        self.btn_home_1.setIcon(icon1)
        self.btn_home_1.setCheckable(True)
        self.btn_home_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_home_1)

        self.btn_ui_test_1 = QPushButton(self.icon_only_widget)
        self.btn_ui_test_1.setObjectName(u"btn_ui_test_1")
        self.btn_ui_test_1.setIcon(icon2)
        self.btn_ui_test_1.setCheckable(True)
        self.btn_ui_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_ui_test_1)

        self.btn_setup_test_1 = QPushButton(self.icon_only_widget)
        self.btn_setup_test_1.setObjectName(u"btn_setup_test_1")
        self.btn_setup_test_1.setIcon(icon3)
        self.btn_setup_test_1.setCheckable(True)
        self.btn_setup_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_setup_test_1)

        self.btn_frame_test_1 = QPushButton(self.icon_only_widget)
        self.btn_frame_test_1.setObjectName(u"btn_frame_test_1")
        self.btn_frame_test_1.setIcon(icon4)
        self.btn_frame_test_1.setCheckable(True)
        self.btn_frame_test_1.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.btn_frame_test_1)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 383, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.pushButton_6 = QPushButton(self.icon_only_widget)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setCheckable(True)

        self.verticalLayout_3.addWidget(self.pushButton_6)


        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.btn_frame_test_1.toggled.connect(self.btn_frame_test_2.setChecked)
        self.btn_setup_test_1.toggled.connect(self.btn_demo_test.setChecked)
        self.btn_ui_test_1.toggled.connect(self.btn_ui_test_2.setChecked)
        self.btn_home_1.toggled.connect(self.btn_home_2.setChecked)
        self.btn_home_2.toggled.connect(self.btn_home_1.setChecked)
        self.btn_ui_test_2.toggled.connect(self.btn_ui_test_1.setChecked)
        self.btn_demo_test.toggled.connect(self.btn_setup_test_1.setChecked)
        self.btn_frame_test_2.toggled.connect(self.btn_frame_test_1.setChecked)
        self.pushButton_6.toggled.connect(MainWindow.close)
        self.pushButton_7.toggled.connect(MainWindow.close)
        self.pushButton_12.toggled.connect(self.pushButton_3.setChecked)
        self.pushButton_12.clicked["bool"].connect(self.icon_only_widget.setVisible)
        self.pushButton_12.clicked["bool"].connect(self.icon_name_widget.setHidden)
        self.pushButton_3.toggled.connect(self.pushButton_12.setChecked)
        self.pushButton_3.clicked["bool"].connect(self.icon_only_widget.setHidden)
        self.pushButton_3.clicked["bool"].connect(self.icon_name_widget.setVisible)

        self.stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"home", None))
        self.btn_test_start.setText(QCoreApplication.translate("MainWindow", u"START", None))
        self.btn_test_stop.setText(QCoreApplication.translate("MainWindow", u"STOP", None))
        self.btn_add_tc.setText(QCoreApplication.translate("MainWindow", u"ADD TC", None))
        self.btn_del_tc.setText(QCoreApplication.translate("MainWindow", u"DEL TC", None))
        self.btn_tc_save.setText(QCoreApplication.translate("MainWindow", u"SAVE", None))
        self.btn_tc_load.setText(QCoreApplication.translate("MainWindow", u"LOAD", None))
        self.cb_accurasm.setText(QCoreApplication.translate("MainWindow", u"AccuraSM", None))
        self.btn_select_webcam.setText(QCoreApplication.translate("MainWindow", u"Select WebCam", None))
        self.btn_start_webcam.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_stop_webcam.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"focus_value", None))
        self.tp_display.setText("")
        self.btn_setting.setText(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.btn_all_connect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.ip_display.setText("")
        self.btn_all_disconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"TCP/IP", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Touch Port", None))
        self.sp_display.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Setup Port", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Ethernet connect menu", None))
        self.label_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"ROOTECH", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"DASHBOARD", None))
        self.btn_home_2.setText(QCoreApplication.translate("MainWindow", u"HOME", None))
        self.btn_ui_test_2.setText(QCoreApplication.translate("MainWindow", u"UI TEST", None))
        self.btn_demo_test.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.btn_frame_test_2.setText(QCoreApplication.translate("MainWindow", u"FRAME TEST", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"Sign Out", None))
        self.label.setText("")
        self.pushButton_3.setText("")
        self.btn_home_1.setText("")
        self.btn_ui_test_1.setText("")
        self.btn_setup_test_1.setText("")
        self.btn_frame_test_1.setText("")
        self.pushButton_6.setText("")
    # retranslateUi

