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
        Form.resize(959, 1077)
        Form.setMinimumSize(QSize(800, 600))
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1018, 1025))
        self.verticalLayout_37 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.widget_2 = QWidget(self.scrollAreaWidgetContents)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(1000, 1000))
        self.widget_2.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.btn_apply = QPushButton(self.widget_2)
        self.btn_apply.setObjectName(u"btn_apply")
        self.btn_apply.setGeometry(QRect(770, 75, 75, 24))
        self.btn_cancel = QPushButton(self.widget_2)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(775, 110, 75, 24))
        self.sub_menu7 = QWidget(self.widget_2)
        self.sub_menu7.setObjectName(u"sub_menu7")
        self.sub_menu7.setGeometry(QRect(10, 485, 721, 476))
        self.sub_menu7.setMinimumSize(QSize(120, 0))
        self.sub_menu7.setStyleSheet(u"QWidget{\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.verticalLayout_32 = QVBoxLayout(self.sub_menu7)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.btn_menu_meter = QPushButton(self.sub_menu7)
        self.btn_menu_meter.setObjectName(u"btn_menu_meter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_menu_meter.sizePolicy().hasHeightForWidth())
        self.btn_menu_meter.setSizePolicy(sizePolicy)
        self.btn_menu_meter.setMinimumSize(QSize(130, 24))
        self.btn_menu_meter.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_meter.setCheckable(True)
        self.btn_menu_meter.setChecked(False)
        self.btn_menu_meter.setAutoDefault(False)
        self.btn_menu_meter.setFlat(False)

        self.verticalLayout_32.addWidget(self.btn_menu_meter)

        self.widget_4 = QWidget(self.sub_menu7)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget_8 = QWidget(self.widget_4)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_14 = QVBoxLayout(self.widget_8)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_31 = QVBoxLayout()
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.btn_menu_measurement = QPushButton(self.widget_8)
        self.btn_menu_measurement.setObjectName(u"btn_menu_measurement")
        sizePolicy.setHeightForWidth(self.btn_menu_measurement.sizePolicy().hasHeightForWidth())
        self.btn_menu_measurement.setSizePolicy(sizePolicy)
        self.btn_menu_measurement.setMinimumSize(QSize(130, 24))
        self.btn_menu_measurement.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_measurement.setCheckable(True)
        self.btn_menu_measurement.setChecked(False)
        self.btn_menu_measurement.setAutoDefault(False)
        self.btn_menu_measurement.setFlat(False)

        self.verticalLayout_5.addWidget(self.btn_menu_measurement)

        self.setup_check_box_2 = QWidget(self.widget_8)
        self.setup_check_box_2.setObjectName(u"setup_check_box_2")
        sizePolicy.setHeightForWidth(self.setup_check_box_2.sizePolicy().hasHeightForWidth())
        self.setup_check_box_2.setSizePolicy(sizePolicy)
        self.verticalLayout_17 = QVBoxLayout(self.setup_check_box_2)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.cb_m_s_meas_all = QCheckBox(self.setup_check_box_2)
        self.cb_m_s_meas_all.setObjectName(u"cb_m_s_meas_all")

        self.verticalLayout_17.addWidget(self.cb_m_s_meas_all)

        self.cb_m_s_vol = QCheckBox(self.setup_check_box_2)
        self.cb_m_s_vol.setObjectName(u"cb_m_s_vol")

        self.verticalLayout_17.addWidget(self.cb_m_s_vol)

        self.cb_m_s_curr = QCheckBox(self.setup_check_box_2)
        self.cb_m_s_curr.setObjectName(u"cb_m_s_curr")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.cb_m_s_curr.sizePolicy().hasHeightForWidth())
        self.cb_m_s_curr.setSizePolicy(sizePolicy1)

        self.verticalLayout_17.addWidget(self.cb_m_s_curr)

        self.cb_m_s_demand = QCheckBox(self.setup_check_box_2)
        self.cb_m_s_demand.setObjectName(u"cb_m_s_demand")

        self.verticalLayout_17.addWidget(self.cb_m_s_demand)

        self.cb_m_s_power = QCheckBox(self.setup_check_box_2)
        self.cb_m_s_power.setObjectName(u"cb_m_s_power")

        self.verticalLayout_17.addWidget(self.cb_m_s_power)


        self.verticalLayout_5.addWidget(self.setup_check_box_2)


        self.verticalLayout_31.addLayout(self.verticalLayout_5)

        self.verticalLayout_28 = QVBoxLayout()
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.btn_menu_setup_test = QPushButton(self.widget_8)
        self.btn_menu_setup_test.setObjectName(u"btn_menu_setup_test")
        sizePolicy.setHeightForWidth(self.btn_menu_setup_test.sizePolicy().hasHeightForWidth())
        self.btn_menu_setup_test.setSizePolicy(sizePolicy)
        self.btn_menu_setup_test.setMinimumSize(QSize(130, 24))
        self.btn_menu_setup_test.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_setup_test.setCheckable(True)
        self.btn_menu_setup_test.setChecked(False)
        self.btn_menu_setup_test.setAutoDefault(False)
        self.btn_menu_setup_test.setFlat(False)

        self.verticalLayout_28.addWidget(self.btn_menu_setup_test)

        self.setup_check_box_1 = QWidget(self.widget_8)
        self.setup_check_box_1.setObjectName(u"setup_check_box_1")
        sizePolicy.setHeightForWidth(self.setup_check_box_1.sizePolicy().hasHeightForWidth())
        self.setup_check_box_1.setSizePolicy(sizePolicy)
        self.verticalLayout_18 = QVBoxLayout(self.setup_check_box_1)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.cb_m_s_initialize = QCheckBox(self.setup_check_box_1)
        self.cb_m_s_initialize.setObjectName(u"cb_m_s_initialize")

        self.verticalLayout_18.addWidget(self.cb_m_s_initialize)

        self.cb_setup_n_a = QCheckBox(self.setup_check_box_1)
        self.cb_setup_n_a.setObjectName(u"cb_setup_n_a")
        sizePolicy1.setHeightForWidth(self.cb_setup_n_a.sizePolicy().hasHeightForWidth())
        self.cb_setup_n_a.setSizePolicy(sizePolicy1)

        self.verticalLayout_18.addWidget(self.cb_setup_n_a)


        self.verticalLayout_28.addWidget(self.setup_check_box_1)


        self.verticalLayout_31.addLayout(self.verticalLayout_28)


        self.verticalLayout_14.addLayout(self.verticalLayout_31)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_6)


        self.horizontalLayout_2.addWidget(self.widget_8)

        self.widget_7 = QWidget(self.widget_4)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_13 = QVBoxLayout(self.widget_7)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.btn_menu_event = QPushButton(self.widget_7)
        self.btn_menu_event.setObjectName(u"btn_menu_event")
        sizePolicy.setHeightForWidth(self.btn_menu_event.sizePolicy().hasHeightForWidth())
        self.btn_menu_event.setSizePolicy(sizePolicy)
        self.btn_menu_event.setMinimumSize(QSize(130, 24))
        self.btn_menu_event.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_event.setCheckable(True)
        self.btn_menu_event.setChecked(False)
        self.btn_menu_event.setAutoDefault(False)
        self.btn_menu_event.setFlat(False)

        self.verticalLayout_16.addWidget(self.btn_menu_event)

        self.setup_check_box_3 = QWidget(self.widget_7)
        self.setup_check_box_3.setObjectName(u"setup_check_box_3")
        sizePolicy.setHeightForWidth(self.setup_check_box_3.sizePolicy().hasHeightForWidth())
        self.setup_check_box_3.setSizePolicy(sizePolicy)
        self.verticalLayout_19 = QVBoxLayout(self.setup_check_box_3)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.cb_m_s_event_all = QCheckBox(self.setup_check_box_3)
        self.cb_m_s_event_all.setObjectName(u"cb_m_s_event_all")

        self.verticalLayout_19.addWidget(self.cb_m_s_event_all)

        self.cb_m_s_dip = QCheckBox(self.setup_check_box_3)
        self.cb_m_s_dip.setObjectName(u"cb_m_s_dip")

        self.verticalLayout_19.addWidget(self.cb_m_s_dip)

        self.cb_m_s_swell = QCheckBox(self.setup_check_box_3)
        self.cb_m_s_swell.setObjectName(u"cb_m_s_swell")
        sizePolicy1.setHeightForWidth(self.cb_m_s_swell.sizePolicy().hasHeightForWidth())
        self.cb_m_s_swell.setSizePolicy(sizePolicy1)

        self.verticalLayout_19.addWidget(self.cb_m_s_swell)

        self.cb_m_s_pq_curve = QCheckBox(self.setup_check_box_3)
        self.cb_m_s_pq_curve.setObjectName(u"cb_m_s_pq_curve")

        self.verticalLayout_19.addWidget(self.cb_m_s_pq_curve)

        self.cb_m_s_volt_conn = QCheckBox(self.setup_check_box_3)
        self.cb_m_s_volt_conn.setObjectName(u"cb_m_s_volt_conn")

        self.verticalLayout_19.addWidget(self.cb_m_s_volt_conn)


        self.verticalLayout_16.addWidget(self.setup_check_box_3)


        self.verticalLayout_30.addLayout(self.verticalLayout_16)

        self.verticalLayout_25 = QVBoxLayout()
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.btn_menu_network = QPushButton(self.widget_7)
        self.btn_menu_network.setObjectName(u"btn_menu_network")
        sizePolicy.setHeightForWidth(self.btn_menu_network.sizePolicy().hasHeightForWidth())
        self.btn_menu_network.setSizePolicy(sizePolicy)
        self.btn_menu_network.setMinimumSize(QSize(130, 24))
        self.btn_menu_network.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_network.setCheckable(True)
        self.btn_menu_network.setChecked(False)
        self.btn_menu_network.setAutoDefault(False)
        self.btn_menu_network.setFlat(False)

        self.verticalLayout_25.addWidget(self.btn_menu_network)

        self.setup_check_box_4 = QWidget(self.widget_7)
        self.setup_check_box_4.setObjectName(u"setup_check_box_4")
        sizePolicy.setHeightForWidth(self.setup_check_box_4.sizePolicy().hasHeightForWidth())
        self.setup_check_box_4.setSizePolicy(sizePolicy)
        self.verticalLayout_20 = QVBoxLayout(self.setup_check_box_4)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.cb_m_s_network_all = QCheckBox(self.setup_check_box_4)
        self.cb_m_s_network_all.setObjectName(u"cb_m_s_network_all")

        self.verticalLayout_20.addWidget(self.cb_m_s_network_all)

        self.cb_m_s_ethernet = QCheckBox(self.setup_check_box_4)
        self.cb_m_s_ethernet.setObjectName(u"cb_m_s_ethernet")

        self.verticalLayout_20.addWidget(self.cb_m_s_ethernet)

        self.cb_m_s_rs485 = QCheckBox(self.setup_check_box_4)
        self.cb_m_s_rs485.setObjectName(u"cb_m_s_rs485")
        sizePolicy1.setHeightForWidth(self.cb_m_s_rs485.sizePolicy().hasHeightForWidth())
        self.cb_m_s_rs485.setSizePolicy(sizePolicy1)

        self.verticalLayout_20.addWidget(self.cb_m_s_rs485)

        self.cb_m_s_advanced = QCheckBox(self.setup_check_box_4)
        self.cb_m_s_advanced.setObjectName(u"cb_m_s_advanced")

        self.verticalLayout_20.addWidget(self.cb_m_s_advanced)


        self.verticalLayout_25.addWidget(self.setup_check_box_4)


        self.verticalLayout_30.addLayout(self.verticalLayout_25)


        self.verticalLayout_13.addLayout(self.verticalLayout_30)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_5)


        self.horizontalLayout_2.addWidget(self.widget_7)

        self.widget_6 = QWidget(self.widget_4)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_11 = QVBoxLayout(self.widget_6)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.btn_menu_control = QPushButton(self.widget_6)
        self.btn_menu_control.setObjectName(u"btn_menu_control")
        sizePolicy.setHeightForWidth(self.btn_menu_control.sizePolicy().hasHeightForWidth())
        self.btn_menu_control.setSizePolicy(sizePolicy)
        self.btn_menu_control.setMinimumSize(QSize(130, 24))
        self.btn_menu_control.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_control.setCheckable(True)
        self.btn_menu_control.setChecked(False)
        self.btn_menu_control.setAutoDefault(False)
        self.btn_menu_control.setFlat(False)

        self.verticalLayout_24.addWidget(self.btn_menu_control)

        self.setup_check_box_5 = QWidget(self.widget_6)
        self.setup_check_box_5.setObjectName(u"setup_check_box_5")
        sizePolicy.setHeightForWidth(self.setup_check_box_5.sizePolicy().hasHeightForWidth())
        self.setup_check_box_5.setSizePolicy(sizePolicy)
        self.verticalLayout_21 = QVBoxLayout(self.setup_check_box_5)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.cb_m_s_control_all = QCheckBox(self.setup_check_box_5)
        self.cb_m_s_control_all.setObjectName(u"cb_m_s_control_all")

        self.verticalLayout_21.addWidget(self.cb_m_s_control_all)

        self.cb_m_s_data_reset = QCheckBox(self.setup_check_box_5)
        self.cb_m_s_data_reset.setObjectName(u"cb_m_s_data_reset")

        self.verticalLayout_21.addWidget(self.cb_m_s_data_reset)

        self.cb_m_s_demand_sync = QCheckBox(self.setup_check_box_5)
        self.cb_m_s_demand_sync.setObjectName(u"cb_m_s_demand_sync")
        sizePolicy1.setHeightForWidth(self.cb_m_s_demand_sync.sizePolicy().hasHeightForWidth())
        self.cb_m_s_demand_sync.setSizePolicy(sizePolicy1)

        self.verticalLayout_21.addWidget(self.cb_m_s_demand_sync)

        self.cb_m_s_test_mode = QCheckBox(self.setup_check_box_5)
        self.cb_m_s_test_mode.setObjectName(u"cb_m_s_test_mode")

        self.verticalLayout_21.addWidget(self.cb_m_s_test_mode)


        self.verticalLayout_24.addWidget(self.setup_check_box_5)


        self.verticalLayout_29.addLayout(self.verticalLayout_24)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.btn_menu_module = QPushButton(self.widget_6)
        self.btn_menu_module.setObjectName(u"btn_menu_module")
        sizePolicy.setHeightForWidth(self.btn_menu_module.sizePolicy().hasHeightForWidth())
        self.btn_menu_module.setSizePolicy(sizePolicy)
        self.btn_menu_module.setMinimumSize(QSize(130, 24))
        self.btn_menu_module.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_module.setCheckable(True)
        self.btn_menu_module.setChecked(False)
        self.btn_menu_module.setAutoDefault(False)
        self.btn_menu_module.setFlat(False)

        self.verticalLayout_26.addWidget(self.btn_menu_module)

        self.setup_check_box_6 = QWidget(self.widget_6)
        self.setup_check_box_6.setObjectName(u"setup_check_box_6")
        sizePolicy.setHeightForWidth(self.setup_check_box_6.sizePolicy().hasHeightForWidth())
        self.setup_check_box_6.setSizePolicy(sizePolicy)
        self.verticalLayout_22 = QVBoxLayout(self.setup_check_box_6)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.cb_m_s_module_n_a = QCheckBox(self.setup_check_box_6)
        self.cb_m_s_module_n_a.setObjectName(u"cb_m_s_module_n_a")

        self.verticalLayout_22.addWidget(self.cb_m_s_module_n_a)


        self.verticalLayout_26.addWidget(self.setup_check_box_6)


        self.verticalLayout_29.addLayout(self.verticalLayout_26)


        self.verticalLayout_11.addLayout(self.verticalLayout_29)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_4)


        self.horizontalLayout_2.addWidget(self.widget_6)

        self.widget_5 = QWidget(self.widget_4)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_9 = QVBoxLayout(self.widget_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.btn_menu_setup_system = QPushButton(self.widget_5)
        self.btn_menu_setup_system.setObjectName(u"btn_menu_setup_system")
        sizePolicy.setHeightForWidth(self.btn_menu_setup_system.sizePolicy().hasHeightForWidth())
        self.btn_menu_setup_system.setSizePolicy(sizePolicy)
        self.btn_menu_setup_system.setMinimumSize(QSize(130, 24))
        self.btn_menu_setup_system.setMaximumSize(QSize(16777215, 24))
        self.btn_menu_setup_system.setCheckable(True)
        self.btn_menu_setup_system.setChecked(False)
        self.btn_menu_setup_system.setAutoDefault(False)
        self.btn_menu_setup_system.setFlat(False)

        self.verticalLayout_27.addWidget(self.btn_menu_setup_system)

        self.setup_check_box_7 = QWidget(self.widget_5)
        self.setup_check_box_7.setObjectName(u"setup_check_box_7")
        sizePolicy.setHeightForWidth(self.setup_check_box_7.sizePolicy().hasHeightForWidth())
        self.setup_check_box_7.setSizePolicy(sizePolicy)
        self.verticalLayout_23 = QVBoxLayout(self.setup_check_box_7)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.cb_m_s_system_all = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_system_all.setObjectName(u"cb_m_s_system_all")

        self.verticalLayout_23.addWidget(self.cb_m_s_system_all)

        self.cb_m_s_description = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_description.setObjectName(u"cb_m_s_description")

        self.verticalLayout_23.addWidget(self.cb_m_s_description)

        self.cb_m_s_locale = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_locale.setObjectName(u"cb_m_s_locale")
        sizePolicy1.setHeightForWidth(self.cb_m_s_locale.sizePolicy().hasHeightForWidth())
        self.cb_m_s_locale.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_locale)

        self.cb_m_s_local_time = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_local_time.setObjectName(u"cb_m_s_local_time")

        self.verticalLayout_23.addWidget(self.cb_m_s_local_time)

        self.cb_m_s_summer_time = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_summer_time.setObjectName(u"cb_m_s_summer_time")
        sizePolicy1.setHeightForWidth(self.cb_m_s_summer_time.sizePolicy().hasHeightForWidth())
        self.cb_m_s_summer_time.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_summer_time)

        self.cb_m_s_ntp = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_ntp.setObjectName(u"cb_m_s_ntp")
        sizePolicy1.setHeightForWidth(self.cb_m_s_ntp.sizePolicy().hasHeightForWidth())
        self.cb_m_s_ntp.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_ntp)

        self.cb_m_s_led = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_led.setObjectName(u"cb_m_s_led")
        sizePolicy1.setHeightForWidth(self.cb_m_s_led.sizePolicy().hasHeightForWidth())
        self.cb_m_s_led.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_led)

        self.cb_m_s_lcd_buzzer = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_lcd_buzzer.setObjectName(u"cb_m_s_lcd_buzzer")
        sizePolicy1.setHeightForWidth(self.cb_m_s_lcd_buzzer.sizePolicy().hasHeightForWidth())
        self.cb_m_s_lcd_buzzer.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_lcd_buzzer)

        self.cb_m_s_cb = QCheckBox(self.setup_check_box_7)
        self.cb_m_s_cb.setObjectName(u"cb_m_s_cb")
        sizePolicy1.setHeightForWidth(self.cb_m_s_cb.sizePolicy().hasHeightForWidth())
        self.cb_m_s_cb.setSizePolicy(sizePolicy1)

        self.verticalLayout_23.addWidget(self.cb_m_s_cb)


        self.verticalLayout_27.addWidget(self.setup_check_box_7)


        self.verticalLayout_9.addLayout(self.verticalLayout_27)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_8)


        self.horizontalLayout_2.addWidget(self.widget_5)


        self.verticalLayout_32.addWidget(self.widget_4)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_32.addItem(self.verticalSpacer_7)

        self.layoutWidget = QWidget(self.widget_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(12, 5, 728, 464))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_meter_meas_test = QPushButton(self.layoutWidget)
        self.btn_meter_meas_test.setObjectName(u"btn_meter_meas_test")
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

        self.cb_tm_balance = QCheckBox(self.tm_check_box)
        self.cb_tm_balance.setObjectName(u"cb_tm_balance")
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

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.verticalLayout_37.addWidget(self.widget_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.retranslateUi(Form)
        self.btn_menu_module.toggled.connect(self.setup_check_box_6.setHidden)
        self.btn_menu_network.toggled.connect(self.setup_check_box_4.setHidden)
        self.btn_menu_setup_test.toggled.connect(self.setup_check_box_1.setHidden)
        self.btn_menu_measurement.toggled.connect(self.setup_check_box_2.setHidden)
        self.btn_menu_control.toggled.connect(self.setup_check_box_5.setHidden)
        self.btn_menu_voltage.toggled.connect(self.vol_check_box.setHidden)
        self.btn_menu_setup_system.toggled.connect(self.setup_check_box_7.setHidden)
        self.btn_menu_meter.toggled.connect(self.widget_4.setHidden)
        self.btn_menu_system.toggled.connect(self.sys_check_box.setHidden)
        self.btn_menu_event.toggled.connect(self.setup_check_box_3.setHidden)
        self.btn_menu_current.toggled.connect(self.curr_check_box.setHidden)
        self.btn_menu_power.toggled.connect(self.pow_check_box.setHidden)
        self.btn_menu_test_mode.toggled.connect(self.tm_check_box.setHidden)
        self.btn_menu_analysis.toggled.connect(self.anal_check_box.setHidden)
        self.btn_meter_meas_test.toggled.connect(self.widget_3.setHidden)

        self.btn_menu_meter.setDefault(True)
        self.btn_menu_measurement.setDefault(True)
        self.btn_menu_setup_test.setDefault(True)
        self.btn_menu_event.setDefault(True)
        self.btn_menu_network.setDefault(True)
        self.btn_menu_control.setDefault(True)
        self.btn_menu_module.setDefault(True)
        self.btn_menu_setup_system.setDefault(True)
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
        self.btn_apply.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"Cancel", None))
        self.btn_menu_meter.setText(QCoreApplication.translate("Form", u"METER SETUP TEST \u2228", None))
        self.btn_menu_measurement.setText(QCoreApplication.translate("Form", u"MEASUREMENT \u2228", None))
        self.cb_m_s_meas_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_vol.setText(QCoreApplication.translate("Form", u"Voltage", None))
        self.cb_m_s_curr.setText(QCoreApplication.translate("Form", u"Current", None))
        self.cb_m_s_demand.setText(QCoreApplication.translate("Form", u"Demand", None))
        self.cb_m_s_power.setText(QCoreApplication.translate("Form", u"Power", None))
        self.btn_menu_setup_test.setText(QCoreApplication.translate("Form", u"SETUP TEST \u2228", None))
        self.cb_m_s_initialize.setText(QCoreApplication.translate("Form", u"Initialize", None))
        self.cb_setup_n_a.setText(QCoreApplication.translate("Form", u"N/A", None))
        self.btn_menu_event.setText(QCoreApplication.translate("Form", u"EVENT \u2228", None))
        self.cb_m_s_event_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_dip.setText(QCoreApplication.translate("Form", u"Dip", None))
        self.cb_m_s_swell.setText(QCoreApplication.translate("Form", u"Swell", None))
        self.cb_m_s_pq_curve.setText(QCoreApplication.translate("Form", u"PQ Curve", None))
        self.cb_m_s_volt_conn.setText(QCoreApplication.translate("Form", u"Volt. Conn", None))
        self.btn_menu_network.setText(QCoreApplication.translate("Form", u"NETWORK \u2228", None))
        self.cb_m_s_network_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_ethernet.setText(QCoreApplication.translate("Form", u"Ethernet", None))
        self.cb_m_s_rs485.setText(QCoreApplication.translate("Form", u"RS-485", None))
        self.cb_m_s_advanced.setText(QCoreApplication.translate("Form", u"Advanced", None))
        self.btn_menu_control.setText(QCoreApplication.translate("Form", u"CONTROL \u2228", None))
        self.cb_m_s_control_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_data_reset.setText(QCoreApplication.translate("Form", u"Data Reset", None))
        self.cb_m_s_demand_sync.setText(QCoreApplication.translate("Form", u"Demand Sync", None))
        self.cb_m_s_test_mode.setText(QCoreApplication.translate("Form", u"Test Mode", None))
        self.btn_menu_module.setText(QCoreApplication.translate("Form", u"MODULE \u2228", None))
        self.cb_m_s_module_n_a.setText(QCoreApplication.translate("Form", u"N/A", None))
        self.btn_menu_setup_system.setText(QCoreApplication.translate("Form", u"SYSTEM \u2228", None))
        self.cb_m_s_system_all.setText(QCoreApplication.translate("Form", u"ALL", None))
        self.cb_m_s_description.setText(QCoreApplication.translate("Form", u"Description", None))
        self.cb_m_s_locale.setText(QCoreApplication.translate("Form", u"Locale", None))
        self.cb_m_s_local_time.setText(QCoreApplication.translate("Form", u"Local Time", None))
        self.cb_m_s_summer_time.setText(QCoreApplication.translate("Form", u"Summer Time", None))
        self.cb_m_s_ntp.setText(QCoreApplication.translate("Form", u"NTP", None))
        self.cb_m_s_led.setText(QCoreApplication.translate("Form", u"LED", None))
        self.cb_m_s_lcd_buzzer.setText(QCoreApplication.translate("Form", u"LCD & Buzzer", None))
        self.cb_m_s_cb.setText(QCoreApplication.translate("Form", u"CB", None))
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
    # retranslateUi

