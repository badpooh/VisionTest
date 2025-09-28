# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        Form.setMaximumSize(QSize(800, 600))
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.scrollArea = QScrollArea(self.widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 818, 618))
        self.verticalLayout_37 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(800, 600))
        self.widget_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.layoutWidget = QWidget(self.widget_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(12, 5, 728, 522))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_meter_meas_test = QPushButton(self.layoutWidget)
        self.btn_meter_meas_test.setObjectName(u"btn_meter_meas_test")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_meter_meas_test.sizePolicy().hasHeightForWidth())
        self.btn_meter_meas_test.setSizePolicy(sizePolicy)
        self.btn_meter_meas_test.setMinimumSize(QSize(0, 24))
        self.btn_meter_meas_test.setMaximumSize(QSize(16777215, 24))
        self.btn_meter_meas_test.setCheckable(True)

        self.verticalLayout_3.addWidget(self.btn_meter_meas_test)

        self.widget_3 = QWidget(self.layoutWidget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_12 = QWidget(self.widget_3)
        self.widget_12.setObjectName(u"widget_12")
        self.verticalLayout_36 = QVBoxLayout(self.widget_12)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.sub_box1 = QVBoxLayout()
        self.sub_box1.setObjectName(u"sub_box1")
        self.btn_menu_voltage = QPushButton(self.widget_12)
        self.btn_menu_voltage.setObjectName(u"btn_menu_voltage")
        sizePolicy.setHeightForWidth(self.btn_menu_voltage.sizePolicy().hasHeightForWidth())
        self.btn_menu_voltage.setSizePolicy(sizePolicy)
        self.btn_menu_voltage.setMinimumSize(QSize(130, 24))
        self.btn_menu_voltage.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_voltage.setStyleSheet(u"QPushButton:checked {\n"
"  background-color: #d0d0d0;\n"
"}")
        self.btn_menu_voltage.setCheckable(True)
        self.btn_menu_voltage.setChecked(False)
        self.btn_menu_voltage.setAutoDefault(False)
        self.btn_menu_voltage.setFlat(False)

        self.sub_box1.addWidget(self.btn_menu_voltage)

        self.vol_check_box = QWidget(self.widget_12)
        self.vol_check_box.setObjectName(u"vol_check_box")
        sizePolicy.setHeightForWidth(self.vol_check_box.sizePolicy().hasHeightForWidth())
        self.vol_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.vol_check_box)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cb_vol_all = QCheckBox(self.vol_check_box)
        self.cb_vol_all.setObjectName(u"cb_vol_all")

        self.verticalLayout.addWidget(self.cb_vol_all)

        self.cb_vol_rms = QCheckBox(self.vol_check_box)
        self.cb_vol_rms.setObjectName(u"cb_vol_rms")
        self.cb_vol_rms.setCheckable(True)
        self.cb_vol_rms.setChecked(False)
        self.cb_vol_rms.setTristate(False)

        self.verticalLayout.addWidget(self.cb_vol_rms)

        self.cb_vol_fund = QCheckBox(self.vol_check_box)
        self.cb_vol_fund.setObjectName(u"cb_vol_fund")

        self.verticalLayout.addWidget(self.cb_vol_fund)

        self.cb_vol_thd = QCheckBox(self.vol_check_box)
        self.cb_vol_thd.setObjectName(u"cb_vol_thd")

        self.verticalLayout.addWidget(self.cb_vol_thd)

        self.cb_vol_freq = QCheckBox(self.vol_check_box)
        self.cb_vol_freq.setObjectName(u"cb_vol_freq")

        self.verticalLayout.addWidget(self.cb_vol_freq)

        self.cb_vol_residual = QCheckBox(self.vol_check_box)
        self.cb_vol_residual.setObjectName(u"cb_vol_residual")

        self.verticalLayout.addWidget(self.cb_vol_residual)

        self.cb_vol_sliding = QCheckBox(self.vol_check_box)
        self.cb_vol_sliding.setObjectName(u"cb_vol_sliding")

        self.verticalLayout.addWidget(self.cb_vol_sliding)


        self.sub_box1.addWidget(self.vol_check_box)


        self.verticalLayout_7.addLayout(self.sub_box1)

        self.sub_box2 = QVBoxLayout()
        self.sub_box2.setObjectName(u"sub_box2")
        self.btn_menu_test_mode = QPushButton(self.widget_12)
        self.btn_menu_test_mode.setObjectName(u"btn_menu_test_mode")
        sizePolicy.setHeightForWidth(self.btn_menu_test_mode.sizePolicy().hasHeightForWidth())
        self.btn_menu_test_mode.setSizePolicy(sizePolicy)
        self.btn_menu_test_mode.setMinimumSize(QSize(130, 24))
        self.btn_menu_test_mode.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_test_mode.setCheckable(True)
        self.btn_menu_test_mode.setChecked(False)
        self.btn_menu_test_mode.setAutoDefault(False)
        self.btn_menu_test_mode.setFlat(False)

        self.sub_box2.addWidget(self.btn_menu_test_mode)

        self.tm_check_box = QWidget(self.widget_12)
        self.tm_check_box.setObjectName(u"tm_check_box")
        sizePolicy.setHeightForWidth(self.tm_check_box.sizePolicy().hasHeightForWidth())
        self.tm_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.tm_check_box)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.cb_tm_all = QCheckBox(self.tm_check_box)
        self.cb_tm_all.setObjectName(u"cb_tm_all")

        self.verticalLayout_6.addWidget(self.cb_tm_all)

        self.cb_m_s_initialize = QCheckBox(self.tm_check_box)
        self.cb_m_s_initialize.setObjectName(u"cb_m_s_initialize")

        self.verticalLayout_6.addWidget(self.cb_m_s_initialize)

        self.cb_tm_balance = QCheckBox(self.tm_check_box)
        self.cb_tm_balance.setObjectName(u"cb_tm_balance")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_tm_balance.sizePolicy().hasHeightForWidth())
        self.cb_tm_balance.setSizePolicy(sizePolicy1)

        self.verticalLayout_6.addWidget(self.cb_tm_balance)

        self.cb_tm_noload = QCheckBox(self.tm_check_box)
        self.cb_tm_noload.setObjectName(u"cb_tm_noload")

        self.verticalLayout_6.addWidget(self.cb_tm_noload)


        self.sub_box2.addWidget(self.tm_check_box)


        self.verticalLayout_7.addLayout(self.sub_box2)


        self.verticalLayout_36.addLayout(self.verticalLayout_7)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_36.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget_12)

        self.widget_11 = QWidget(self.widget_3)
        self.widget_11.setObjectName(u"widget_11")
        self.verticalLayout_35 = QVBoxLayout(self.widget_11)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.sub_box3 = QVBoxLayout()
        self.sub_box3.setObjectName(u"sub_box3")
        self.btn_menu_current = QPushButton(self.widget_11)
        self.btn_menu_current.setObjectName(u"btn_menu_current")
        sizePolicy.setHeightForWidth(self.btn_menu_current.sizePolicy().hasHeightForWidth())
        self.btn_menu_current.setSizePolicy(sizePolicy)
        self.btn_menu_current.setMinimumSize(QSize(130, 24))
        self.btn_menu_current.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_current.setCheckable(True)
        self.btn_menu_current.setChecked(False)
        self.btn_menu_current.setAutoDefault(False)
        self.btn_menu_current.setFlat(False)

        self.sub_box3.addWidget(self.btn_menu_current)

        self.curr_check_box = QWidget(self.widget_11)
        self.curr_check_box.setObjectName(u"curr_check_box")
        sizePolicy.setHeightForWidth(self.curr_check_box.sizePolicy().hasHeightForWidth())
        self.curr_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_10 = QVBoxLayout(self.curr_check_box)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.cb_curr_all = QCheckBox(self.curr_check_box)
        self.cb_curr_all.setObjectName(u"cb_curr_all")
        self.cb_curr_all.setCheckable(True)
        self.cb_curr_all.setChecked(False)

        self.verticalLayout_10.addWidget(self.cb_curr_all)

        self.cb_curr_rms = QCheckBox(self.curr_check_box)
        self.cb_curr_rms.setObjectName(u"cb_curr_rms")

        self.verticalLayout_10.addWidget(self.cb_curr_rms)

        self.cb_curr_fund = QCheckBox(self.curr_check_box)
        self.cb_curr_fund.setObjectName(u"cb_curr_fund")

        self.verticalLayout_10.addWidget(self.cb_curr_fund)

        self.cb_curr_demand = QCheckBox(self.curr_check_box)
        self.cb_curr_demand.setObjectName(u"cb_curr_demand")

        self.verticalLayout_10.addWidget(self.cb_curr_demand)

        self.cb_curr_thd = QCheckBox(self.curr_check_box)
        self.cb_curr_thd.setObjectName(u"cb_curr_thd")

        self.verticalLayout_10.addWidget(self.cb_curr_thd)

        self.cb_curr_tdd = QCheckBox(self.curr_check_box)
        self.cb_curr_tdd.setObjectName(u"cb_curr_tdd")

        self.verticalLayout_10.addWidget(self.cb_curr_tdd)

        self.cb_curr_cf = QCheckBox(self.curr_check_box)
        self.cb_curr_cf.setObjectName(u"cb_curr_cf")

        self.verticalLayout_10.addWidget(self.cb_curr_cf)

        self.cb_curr_kf = QCheckBox(self.curr_check_box)
        self.cb_curr_kf.setObjectName(u"cb_curr_kf")

        self.verticalLayout_10.addWidget(self.cb_curr_kf)

        self.cb_curr_residual = QCheckBox(self.curr_check_box)
        self.cb_curr_residual.setObjectName(u"cb_curr_residual")

        self.verticalLayout_10.addWidget(self.cb_curr_residual)


        self.sub_box3.addWidget(self.curr_check_box)


        self.verticalLayout_35.addLayout(self.sub_box3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_35.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addWidget(self.widget_11)

        self.widget_10 = QWidget(self.widget_3)
        self.widget_10.setObjectName(u"widget_10")
        self.verticalLayout_34 = QVBoxLayout(self.widget_10)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.sub_box4 = QVBoxLayout()
        self.sub_box4.setObjectName(u"sub_box4")
        self.btn_menu_power = QPushButton(self.widget_10)
        self.btn_menu_power.setObjectName(u"btn_menu_power")
        sizePolicy.setHeightForWidth(self.btn_menu_power.sizePolicy().hasHeightForWidth())
        self.btn_menu_power.setSizePolicy(sizePolicy)
        self.btn_menu_power.setMinimumSize(QSize(130, 24))
        self.btn_menu_power.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_power.setCheckable(True)
        self.btn_menu_power.setChecked(False)
        self.btn_menu_power.setAutoDefault(False)
        self.btn_menu_power.setFlat(False)

        self.sub_box4.addWidget(self.btn_menu_power)

        self.pow_check_box = QWidget(self.widget_10)
        self.pow_check_box.setObjectName(u"pow_check_box")
        sizePolicy.setHeightForWidth(self.pow_check_box.sizePolicy().hasHeightForWidth())
        self.pow_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_12 = QVBoxLayout(self.pow_check_box)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.cb_pow_all = QCheckBox(self.pow_check_box)
        self.cb_pow_all.setObjectName(u"cb_pow_all")
        self.cb_pow_all.setCheckable(True)
        self.cb_pow_all.setChecked(False)

        self.verticalLayout_12.addWidget(self.cb_pow_all)

        self.cb_pow_p = QCheckBox(self.pow_check_box)
        self.cb_pow_p.setObjectName(u"cb_pow_p")

        self.verticalLayout_12.addWidget(self.cb_pow_p)

        self.cb_pow_q = QCheckBox(self.pow_check_box)
        self.cb_pow_q.setObjectName(u"cb_pow_q")

        self.verticalLayout_12.addWidget(self.cb_pow_q)

        self.cb_pow_s = QCheckBox(self.pow_check_box)
        self.cb_pow_s.setObjectName(u"cb_pow_s")

        self.verticalLayout_12.addWidget(self.cb_pow_s)

        self.cb_pow_pf = QCheckBox(self.pow_check_box)
        self.cb_pow_pf.setObjectName(u"cb_pow_pf")

        self.verticalLayout_12.addWidget(self.cb_pow_pf)

        self.cb_pow_demand = QCheckBox(self.pow_check_box)
        self.cb_pow_demand.setObjectName(u"cb_pow_demand")

        self.verticalLayout_12.addWidget(self.cb_pow_demand)

        self.cb_pow_energy = QCheckBox(self.pow_check_box)
        self.cb_pow_energy.setObjectName(u"cb_pow_energy")

        self.verticalLayout_12.addWidget(self.cb_pow_energy)


        self.sub_box4.addWidget(self.pow_check_box)


        self.verticalLayout_34.addLayout(self.sub_box4)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer_9)


        self.horizontalLayout.addWidget(self.widget_10)

        self.widget_9 = QWidget(self.widget_3)
        self.widget_9.setObjectName(u"widget_9")
        self.verticalLayout_33 = QVBoxLayout(self.widget_9)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.sub_box5 = QVBoxLayout()
        self.sub_box5.setObjectName(u"sub_box5")
        self.btn_menu_analysis = QPushButton(self.widget_9)
        self.btn_menu_analysis.setObjectName(u"btn_menu_analysis")
        sizePolicy.setHeightForWidth(self.btn_menu_analysis.sizePolicy().hasHeightForWidth())
        self.btn_menu_analysis.setSizePolicy(sizePolicy)
        self.btn_menu_analysis.setMinimumSize(QSize(130, 24))
        self.btn_menu_analysis.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_analysis.setCheckable(True)
        self.btn_menu_analysis.setChecked(False)
        self.btn_menu_analysis.setAutoDefault(False)
        self.btn_menu_analysis.setFlat(False)

        self.sub_box5.addWidget(self.btn_menu_analysis)

        self.anal_check_box = QWidget(self.widget_9)
        self.anal_check_box.setObjectName(u"anal_check_box")
        sizePolicy.setHeightForWidth(self.anal_check_box.sizePolicy().hasHeightForWidth())
        self.anal_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.anal_check_box)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cb_anal_all = QCheckBox(self.anal_check_box)
        self.cb_anal_all.setObjectName(u"cb_anal_all")

        self.verticalLayout_2.addWidget(self.cb_anal_all)

        self.cb_anal_phasor = QCheckBox(self.anal_check_box)
        self.cb_anal_phasor.setObjectName(u"cb_anal_phasor")

        self.verticalLayout_2.addWidget(self.cb_anal_phasor)

        self.cb_anal_harmonics = QCheckBox(self.anal_check_box)
        self.cb_anal_harmonics.setObjectName(u"cb_anal_harmonics")

        self.verticalLayout_2.addWidget(self.cb_anal_harmonics)

        self.cb_anal_waveform = QCheckBox(self.anal_check_box)
        self.cb_anal_waveform.setObjectName(u"cb_anal_waveform")

        self.verticalLayout_2.addWidget(self.cb_anal_waveform)

        self.cb_anal_volt_sym = QCheckBox(self.anal_check_box)
        self.cb_anal_volt_sym.setObjectName(u"cb_anal_volt_sym")

        self.verticalLayout_2.addWidget(self.cb_anal_volt_sym)

        self.cb_anal_volt_unbal = QCheckBox(self.anal_check_box)
        self.cb_anal_volt_unbal.setObjectName(u"cb_anal_volt_unbal")

        self.verticalLayout_2.addWidget(self.cb_anal_volt_unbal)

        self.cb_anal_curr_sym = QCheckBox(self.anal_check_box)
        self.cb_anal_curr_sym.setObjectName(u"cb_anal_curr_sym")

        self.verticalLayout_2.addWidget(self.cb_anal_curr_sym)

        self.cb_anal_curr_unbal = QCheckBox(self.anal_check_box)
        self.cb_anal_curr_unbal.setObjectName(u"cb_anal_curr_unbal")

        self.verticalLayout_2.addWidget(self.cb_anal_curr_unbal)


        self.sub_box5.addWidget(self.anal_check_box)


        self.verticalLayout_8.addLayout(self.sub_box5)

        self.sub_box6 = QVBoxLayout()
        self.sub_box6.setObjectName(u"sub_box6")
        self.btn_menu_system = QPushButton(self.widget_9)
        self.btn_menu_system.setObjectName(u"btn_menu_system")
        sizePolicy.setHeightForWidth(self.btn_menu_system.sizePolicy().hasHeightForWidth())
        self.btn_menu_system.setSizePolicy(sizePolicy)
        self.btn_menu_system.setMinimumSize(QSize(130, 24))
        self.btn_menu_system.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_system.setCheckable(True)
        self.btn_menu_system.setChecked(False)
        self.btn_menu_system.setAutoDefault(False)
        self.btn_menu_system.setFlat(False)

        self.sub_box6.addWidget(self.btn_menu_system)

        self.sys_check_box = QWidget(self.widget_9)
        self.sys_check_box.setObjectName(u"sys_check_box")
        sizePolicy.setHeightForWidth(self.sys_check_box.sizePolicy().hasHeightForWidth())
        self.sys_check_box.setSizePolicy(sizePolicy)
        self.verticalLayout_15 = QVBoxLayout(self.sys_check_box)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.cb_sys_all = QCheckBox(self.sys_check_box)
        self.cb_sys_all.setObjectName(u"cb_sys_all")

        self.verticalLayout_15.addWidget(self.cb_sys_all)


        self.sub_box6.addWidget(self.sys_check_box)


        self.verticalLayout_8.addLayout(self.sub_box6)


        self.verticalLayout_33.addLayout(self.verticalLayout_8)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_33.addItem(self.verticalSpacer_10)


        self.horizontalLayout.addWidget(self.widget_9)


        self.verticalLayout_3.addWidget(self.widget_3)

        self.btn_apply = QPushButton(self.layoutWidget)
        self.btn_apply.setObjectName(u"btn_apply")

        self.verticalLayout_3.addWidget(self.btn_apply)

        self.btn_cancel = QPushButton(self.layoutWidget)
        self.btn_cancel.setObjectName(u"btn_cancel")

        self.verticalLayout_3.addWidget(self.btn_cancel)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.verticalLayout_37.addWidget(self.widget_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.retranslateUi(Form)
        self.btn_menu_voltage.toggled.connect(self.vol_check_box.setHidden)
        self.btn_menu_system.toggled.connect(self.sys_check_box.setHidden)
        self.btn_menu_current.toggled.connect(self.curr_check_box.setHidden)
        self.btn_menu_power.toggled.connect(self.pow_check_box.setHidden)
        self.btn_menu_test_mode.toggled.connect(self.tm_check_box.setHidden)
        self.btn_menu_analysis.toggled.connect(self.anal_check_box.setHidden)
        self.btn_meter_meas_test.toggled.connect(self.widget_3.setHidden)

        self.btn_meter_meas_test.setDefault(True)
        self.btn_menu_voltage.setDefault(True)
        self.btn_menu_test_mode.setDefault(True)
        self.btn_menu_current.setDefault(True)
        self.btn_menu_power.setDefault(True)
        self.btn_menu_analysis.setDefault(True)
        self.btn_menu_system.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_meter_meas_test.setText(QCoreApplication.translate("Form", u"METER MEASUREMENT TEST \u2228", None))
        self.btn_menu_voltage.setText(QCoreApplication.translate("Form", u"VOLTAGE \u2228", None))
        self.cb_vol_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_vol_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.cb_vol_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.cb_vol_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.cb_vol_freq.setText(QCoreApplication.translate("Form", u"Frequency", None))
        self.cb_vol_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.cb_vol_sliding.setText(QCoreApplication.translate("Form", u"Sliding Ref.", None))
        self.btn_menu_test_mode.setText(QCoreApplication.translate("Form", u"TEST MODE \u2228", None))
        self.cb_tm_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_initialize.setText(QCoreApplication.translate("Form", u"Initialize", None))
        self.cb_tm_balance.setText(QCoreApplication.translate("Form", u"Balance", None))
        self.cb_tm_noload.setText(QCoreApplication.translate("Form", u"No Load", None))
        self.btn_menu_current.setText(QCoreApplication.translate("Form", u"CURRENT \u2228", None))
        self.cb_curr_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_curr_rms.setText(QCoreApplication.translate("Form", u"RMS", None))
        self.cb_curr_fund.setText(QCoreApplication.translate("Form", u"Fundamental", None))
        self.cb_curr_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.cb_curr_thd.setText(QCoreApplication.translate("Form", u"THD %", None))
        self.cb_curr_tdd.setText(QCoreApplication.translate("Form", u"TDD %", None))
        self.cb_curr_cf.setText(QCoreApplication.translate("Form", u"Crest Factor", None))
        self.cb_curr_kf.setText(QCoreApplication.translate("Form", u"K-Factor", None))
        self.cb_curr_residual.setText(QCoreApplication.translate("Form", u"Residual", None))
        self.btn_menu_power.setText(QCoreApplication.translate("Form", u"POWER \u2228", None))
        self.cb_pow_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_pow_p.setText(QCoreApplication.translate("Form", u"Active(P)", None))
        self.cb_pow_q.setText(QCoreApplication.translate("Form", u"Reactive(Q)", None))
        self.cb_pow_s.setText(QCoreApplication.translate("Form", u"Apparent(S)", None))
        self.cb_pow_pf.setText(QCoreApplication.translate("Form", u"PF", None))
        self.cb_pow_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.cb_pow_energy.setText(QCoreApplication.translate("Form", u"Energy", None))
        self.btn_menu_analysis.setText(QCoreApplication.translate("Form", u"ANALYSIS \u2228", None))
        self.cb_anal_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_anal_phasor.setText(QCoreApplication.translate("Form", u"Phasor", None))
        self.cb_anal_harmonics.setText(QCoreApplication.translate("Form", u"Harmonics", None))
        self.cb_anal_waveform.setText(QCoreApplication.translate("Form", u"Waveform", None))
        self.cb_anal_volt_sym.setText(QCoreApplication.translate("Form", u"Volt.Symm.", None))
        self.cb_anal_volt_unbal.setText(QCoreApplication.translate("Form", u"Volt.Unbal.%", None))
        self.cb_anal_curr_sym.setText(QCoreApplication.translate("Form", u"Curr.Symm.", None))
        self.cb_anal_curr_unbal.setText(QCoreApplication.translate("Form", u"Curr.Unbal.%", None))
        self.btn_menu_system.setText(QCoreApplication.translate("Form", u"SYSTEM \u2228", None))
        self.cb_sys_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.btn_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
    # retranslateUi

