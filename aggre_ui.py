# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_aggregation_test.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 600)
        Form.setMinimumSize(QSize(800, 600))
        Form.setMaximumSize(QSize(800, 600))
        Form.setStyleSheet(u"background-color: white;")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(29, 99, 661, 451))
        self.widget_time = QWidget(self.widget)
        self.widget_time.setObjectName(u"widget_time")
        self.widget_time.setGeometry(QRect(10, 20, 192, 244))
        self.verticalLayout = QVBoxLayout(self.widget_time)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_8 = QLabel(self.widget_time)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_8)

        self.layout_step1 = QHBoxLayout()
        self.layout_step1.setSpacing(6)
        self.layout_step1.setObjectName(u"layout_step1")
        self.layout_step1.setContentsMargins(0, 0, 0, 0)
        self.label_time1 = QLabel(self.widget_time)
        self.label_time1.setObjectName(u"label_time1")
        self.label_time1.setFrameShape(QFrame.Shape.Panel)
        self.label_time1.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time1.setLineWidth(1)
        self.label_time1.setMidLineWidth(0)
        self.label_time1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step1.addWidget(self.label_time1)

        self.lineEdit_time1 = QLineEdit(self.widget_time)
        self.lineEdit_time1.setObjectName(u"lineEdit_time1")
        self.lineEdit_time1.setDragEnabled(True)
        self.lineEdit_time1.setClearButtonEnabled(False)

        self.layout_step1.addWidget(self.lineEdit_time1)


        self.verticalLayout.addLayout(self.layout_step1)

        self.layout_step2 = QHBoxLayout()
        self.layout_step2.setObjectName(u"layout_step2")
        self.label_time2 = QLabel(self.widget_time)
        self.label_time2.setObjectName(u"label_time2")
        self.label_time2.setFrameShape(QFrame.Shape.Panel)
        self.label_time2.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time2.setLineWidth(1)
        self.label_time2.setMidLineWidth(0)
        self.label_time2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step2.addWidget(self.label_time2)

        self.lineEdit_time2 = QLineEdit(self.widget_time)
        self.lineEdit_time2.setObjectName(u"lineEdit_time2")

        self.layout_step2.addWidget(self.lineEdit_time2)


        self.verticalLayout.addLayout(self.layout_step2)

        self.layout_step3 = QHBoxLayout()
        self.layout_step3.setObjectName(u"layout_step3")
        self.label_time3 = QLabel(self.widget_time)
        self.label_time3.setObjectName(u"label_time3")
        self.label_time3.setFrameShape(QFrame.Shape.Panel)
        self.label_time3.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time3.setLineWidth(1)
        self.label_time3.setMidLineWidth(0)
        self.label_time3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step3.addWidget(self.label_time3)

        self.lineEdit_time3 = QLineEdit(self.widget_time)
        self.lineEdit_time3.setObjectName(u"lineEdit_time3")

        self.layout_step3.addWidget(self.lineEdit_time3)


        self.verticalLayout.addLayout(self.layout_step3)

        self.layout_step4 = QHBoxLayout()
        self.layout_step4.setObjectName(u"layout_step4")
        self.label_time4 = QLabel(self.widget_time)
        self.label_time4.setObjectName(u"label_time4")
        self.label_time4.setFrameShape(QFrame.Shape.Panel)
        self.label_time4.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time4.setLineWidth(1)
        self.label_time4.setMidLineWidth(0)
        self.label_time4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step4.addWidget(self.label_time4)

        self.lineEdit_time4 = QLineEdit(self.widget_time)
        self.lineEdit_time4.setObjectName(u"lineEdit_time4")

        self.layout_step4.addWidget(self.lineEdit_time4)


        self.verticalLayout.addLayout(self.layout_step4)

        self.layout_step5 = QHBoxLayout()
        self.layout_step5.setObjectName(u"layout_step5")
        self.label_time5 = QLabel(self.widget_time)
        self.label_time5.setObjectName(u"label_time5")
        self.label_time5.setFrameShape(QFrame.Shape.Panel)
        self.label_time5.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time5.setLineWidth(1)
        self.label_time5.setMidLineWidth(0)
        self.label_time5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step5.addWidget(self.label_time5)

        self.lineEdit_time5 = QLineEdit(self.widget_time)
        self.lineEdit_time5.setObjectName(u"lineEdit_time5")

        self.layout_step5.addWidget(self.lineEdit_time5)


        self.verticalLayout.addLayout(self.layout_step5)

        self.layout_step6 = QHBoxLayout()
        self.layout_step6.setObjectName(u"layout_step6")
        self.label_time6 = QLabel(self.widget_time)
        self.label_time6.setObjectName(u"label_time6")
        self.label_time6.setFrameShape(QFrame.Shape.Panel)
        self.label_time6.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time6.setLineWidth(1)
        self.label_time6.setMidLineWidth(0)
        self.label_time6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step6.addWidget(self.label_time6)

        self.lineEdit_time6 = QLineEdit(self.widget_time)
        self.lineEdit_time6.setObjectName(u"lineEdit_time6")

        self.layout_step6.addWidget(self.lineEdit_time6)


        self.verticalLayout.addLayout(self.layout_step6)

        self.layout_step7 = QHBoxLayout()
        self.layout_step7.setObjectName(u"layout_step7")
        self.label_time7 = QLabel(self.widget_time)
        self.label_time7.setObjectName(u"label_time7")
        self.label_time7.setFrameShape(QFrame.Shape.Panel)
        self.label_time7.setFrameShadow(QFrame.Shadow.Plain)
        self.label_time7.setLineWidth(1)
        self.label_time7.setMidLineWidth(0)
        self.label_time7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_step7.addWidget(self.label_time7)

        self.lineEdit_time7 = QLineEdit(self.widget_time)
        self.lineEdit_time7.setObjectName(u"lineEdit_time7")

        self.layout_step7.addWidget(self.lineEdit_time7)


        self.verticalLayout.addLayout(self.layout_step7)

        self.widget_voltage = QWidget(self.widget)
        self.widget_voltage.setObjectName(u"widget_voltage")
        self.widget_voltage.setGeometry(QRect(220, 20, 192, 244))
        self.verticalLayout_2 = QVBoxLayout(self.widget_voltage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_9 = QLabel(self.widget_voltage)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_9)

        self.layout_source_step1 = QHBoxLayout()
        self.layout_source_step1.setSpacing(6)
        self.layout_source_step1.setObjectName(u"layout_source_step1")
        self.layout_source_step1.setContentsMargins(0, 0, 0, 0)
        self.label_source1 = QLabel(self.widget_voltage)
        self.label_source1.setObjectName(u"label_source1")
        self.label_source1.setFrameShape(QFrame.Shape.Panel)
        self.label_source1.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source1.setLineWidth(1)
        self.label_source1.setMidLineWidth(0)
        self.label_source1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step1.addWidget(self.label_source1)

        self.lineEdit_source1 = QLineEdit(self.widget_voltage)
        self.lineEdit_source1.setObjectName(u"lineEdit_source1")

        self.layout_source_step1.addWidget(self.lineEdit_source1)


        self.verticalLayout_2.addLayout(self.layout_source_step1)

        self.layout_source_step2 = QHBoxLayout()
        self.layout_source_step2.setObjectName(u"layout_source_step2")
        self.label_source2 = QLabel(self.widget_voltage)
        self.label_source2.setObjectName(u"label_source2")
        self.label_source2.setFrameShape(QFrame.Shape.Panel)
        self.label_source2.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source2.setLineWidth(1)
        self.label_source2.setMidLineWidth(0)
        self.label_source2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step2.addWidget(self.label_source2)

        self.lineEdit_source2 = QLineEdit(self.widget_voltage)
        self.lineEdit_source2.setObjectName(u"lineEdit_source2")

        self.layout_source_step2.addWidget(self.lineEdit_source2)


        self.verticalLayout_2.addLayout(self.layout_source_step2)

        self.layout_source_step3 = QHBoxLayout()
        self.layout_source_step3.setObjectName(u"layout_source_step3")
        self.label_source3 = QLabel(self.widget_voltage)
        self.label_source3.setObjectName(u"label_source3")
        self.label_source3.setFrameShape(QFrame.Shape.Panel)
        self.label_source3.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source3.setLineWidth(1)
        self.label_source3.setMidLineWidth(0)
        self.label_source3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step3.addWidget(self.label_source3)

        self.lineEdit_source3 = QLineEdit(self.widget_voltage)
        self.lineEdit_source3.setObjectName(u"lineEdit_source3")

        self.layout_source_step3.addWidget(self.lineEdit_source3)


        self.verticalLayout_2.addLayout(self.layout_source_step3)

        self.layout_source_step4 = QHBoxLayout()
        self.layout_source_step4.setObjectName(u"layout_source_step4")
        self.label_source4 = QLabel(self.widget_voltage)
        self.label_source4.setObjectName(u"label_source4")
        self.label_source4.setFrameShape(QFrame.Shape.Panel)
        self.label_source4.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source4.setLineWidth(1)
        self.label_source4.setMidLineWidth(0)
        self.label_source4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step4.addWidget(self.label_source4)

        self.lineEdit_source4 = QLineEdit(self.widget_voltage)
        self.lineEdit_source4.setObjectName(u"lineEdit_source4")

        self.layout_source_step4.addWidget(self.lineEdit_source4)


        self.verticalLayout_2.addLayout(self.layout_source_step4)

        self.layout_source_step5 = QHBoxLayout()
        self.layout_source_step5.setObjectName(u"layout_source_step5")
        self.label_source5 = QLabel(self.widget_voltage)
        self.label_source5.setObjectName(u"label_source5")
        self.label_source5.setFrameShape(QFrame.Shape.Panel)
        self.label_source5.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source5.setLineWidth(1)
        self.label_source5.setMidLineWidth(0)
        self.label_source5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step5.addWidget(self.label_source5)

        self.lineEdit_source5 = QLineEdit(self.widget_voltage)
        self.lineEdit_source5.setObjectName(u"lineEdit_source5")

        self.layout_source_step5.addWidget(self.lineEdit_source5)


        self.verticalLayout_2.addLayout(self.layout_source_step5)

        self.layout_source_step6 = QHBoxLayout()
        self.layout_source_step6.setObjectName(u"layout_source_step6")
        self.label_source6 = QLabel(self.widget_voltage)
        self.label_source6.setObjectName(u"label_source6")
        self.label_source6.setFrameShape(QFrame.Shape.Panel)
        self.label_source6.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source6.setLineWidth(1)
        self.label_source6.setMidLineWidth(0)
        self.label_source6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step6.addWidget(self.label_source6)

        self.lineEdit_source6 = QLineEdit(self.widget_voltage)
        self.lineEdit_source6.setObjectName(u"lineEdit_source6")

        self.layout_source_step6.addWidget(self.lineEdit_source6)


        self.verticalLayout_2.addLayout(self.layout_source_step6)

        self.layout_source_step7 = QHBoxLayout()
        self.layout_source_step7.setObjectName(u"layout_source_step7")
        self.label_source7 = QLabel(self.widget_voltage)
        self.label_source7.setObjectName(u"label_source7")
        self.label_source7.setFrameShape(QFrame.Shape.Panel)
        self.label_source7.setFrameShadow(QFrame.Shadow.Plain)
        self.label_source7.setLineWidth(1)
        self.label_source7.setMidLineWidth(0)
        self.label_source7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_source_step7.addWidget(self.label_source7)

        self.lineEdit_source7 = QLineEdit(self.widget_voltage)
        self.lineEdit_source7.setObjectName(u"lineEdit_source7")

        self.layout_source_step7.addWidget(self.lineEdit_source7)


        self.verticalLayout_2.addLayout(self.layout_source_step7)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(40, 40, 308, 42))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_start = QPushButton(self.widget_2)
        self.btn_start.setObjectName(u"btn_start")

        self.horizontalLayout.addWidget(self.btn_start)

        self.btn_stop = QPushButton(self.widget_2)
        self.btn_stop.setObjectName(u"btn_stop")

        self.horizontalLayout.addWidget(self.btn_stop)

        self.btn_device = QPushButton(self.widget_2)
        self.btn_device.setObjectName(u"btn_device")

        self.horizontalLayout.addWidget(self.btn_device)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(370, 40, 313, 42))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_ip = QLineEdit(self.widget_3)
        self.lineEdit_ip.setObjectName(u"lineEdit_ip")

        self.horizontalLayout_2.addWidget(self.lineEdit_ip)

        self.btn_connect = QPushButton(self.widget_3)
        self.btn_connect.setObjectName(u"btn_connect")

        self.horizontalLayout_2.addWidget(self.btn_connect)

        self.btn_disconnect = QPushButton(self.widget_3)
        self.btn_disconnect.setObjectName(u"btn_disconnect")

        self.horizontalLayout_2.addWidget(self.btn_disconnect)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"TIME(Sec)", None))
        self.label_time1.setText(QCoreApplication.translate("Form", u"Step1", None))
        self.lineEdit_time1.setText("")
        self.label_time2.setText(QCoreApplication.translate("Form", u"Step2", None))
        self.lineEdit_time2.setText("")
        self.label_time3.setText(QCoreApplication.translate("Form", u"Step3", None))
        self.lineEdit_time3.setText("")
        self.label_time4.setText(QCoreApplication.translate("Form", u"Step4", None))
        self.lineEdit_time4.setText("")
        self.label_time5.setText(QCoreApplication.translate("Form", u"Step5", None))
        self.lineEdit_time5.setText("")
        self.label_time6.setText(QCoreApplication.translate("Form", u"Step6", None))
        self.lineEdit_time6.setText("")
        self.label_time7.setText(QCoreApplication.translate("Form", u"Step7", None))
        self.lineEdit_time7.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"Voltage A (V)", None))
        self.label_source1.setText(QCoreApplication.translate("Form", u"Step1", None))
        self.lineEdit_source1.setText("")
        self.label_source2.setText(QCoreApplication.translate("Form", u"Step2", None))
        self.lineEdit_source2.setText("")
        self.label_source3.setText(QCoreApplication.translate("Form", u"Step3", None))
        self.lineEdit_source3.setText("")
        self.label_source4.setText(QCoreApplication.translate("Form", u"Step4", None))
        self.lineEdit_source4.setText("")
        self.label_source5.setText(QCoreApplication.translate("Form", u"Step5", None))
        self.lineEdit_source5.setText("")
        self.label_source6.setText(QCoreApplication.translate("Form", u"Step6", None))
        self.lineEdit_source6.setText("")
        self.label_source7.setText(QCoreApplication.translate("Form", u"Step7", None))
        self.lineEdit_source7.setText("")
        self.btn_start.setText(QCoreApplication.translate("Form", u"START", None))
        self.btn_stop.setText(QCoreApplication.translate("Form", u"STOP", None))
        self.btn_device.setText(QCoreApplication.translate("Form", u"Connect_CMC256Plus", None))
        self.btn_connect.setText(QCoreApplication.translate("Form", u"Connect", None))
        self.btn_disconnect.setText(QCoreApplication.translate("Form", u"Disconnect", None))
    # retranslateUi

