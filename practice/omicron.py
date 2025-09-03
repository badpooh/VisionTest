###############################################################################
#   CMEngine control
###############################################################################
import Config
import win32com.client
import math
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLineEdit, QMainWindow, QApplication
import sys
import time
import threading

from ui_omicron import Ui_MainWindow

###############################################################################
#   class CMEngine
###############################################################################
class CMEngine(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("My Dashboard")   
        self.device_locked = False
        self.is_on = False
        self.serial = ""
        self.typ = ""
        self.device_ip = ""
        self.device_id = 0
        self.device_list = []  # 디바이스 리스트를 관리하는 내부 리스트
        self.cm_engine = win32com.client.Dispatch("OMICRON.CMEngAL")
        self.pushButton.clicked.connect(self.scan_device)
        self.pushButton_2.clicked.connect(self.select_device)
        self.pushButton_3.clicked.connect(self.start)
        self.pushButton_4.clicked.connect(self.stop)
        self.is_outputting = False
        self.output_thread = None
        
    def scan_device(self):
        self.scan_for_new()
        
    def select_device(self):
        self.lock_device()
        
    def start(self):
        self.start_output()
        
    def stop(self):
        self.stop_output()
        
    def scan_for_new(self):
        self.unlock_all_devices()
        self.devlog("scanning....")

        self.cm_engine.DevScanForNew(False)
        ret = self.cm_engine.DevGetList(0)  # Return all associated CMCs
        ret = ret.split(";")
        while '' in ret: ret.remove('')
        self.device_list = []
        for device in ret: 
            self.device_list.append(device.split(","))   
        
        if not len(self.device_list):
            self.devlog("no devices found!")
            return
        else:
            self.devlog("devices found:")
            for device in self.device_list:
                self.devlog("  {}".format(device))

    def unlock_all_devices(self):
        self.device_locked = False
        self.devlog("All devices unlocked.")  # 연결 해제 완료 메시지

    def lock_device(self):
        self.unlock_all_devices()
        # 예시: 첫 번째 디바이스를 잠금 대상으로 선택
        if self.device_list:
            self.device_id, self.serial, _, _ = self.device_list[0]
            self.device_id = int(self.device_id)
            self.serial = self.cm_engine.SerialNumber(self.device_id)
            self.typ = self.cm_engine.DeviceType(self.device_id)
            self.device_ip = self.cm_engine.IPAddress(self.device_id)
            self.cm_engine.DevLock(self.device_id)
            self.device_locked = True
            self.devlog(f"Mapper locked to: {self.serial} - {self.device_ip}")
            print("Connection complete.")  # 연결 완료 메시지
        else:
            self.devlog("No CMC-Device found or selected!")
    
    def devlog(self, message):
        # 로그 메시지 처리 방식 (예: 콘솔 출력)
        print(message)




###############################################################################
#   CMC output contol
###############################################################################

    def execute_command(self, cmd):
        try:
            print(f"Exec cmd: {cmd}")
            self.cm_engine.Exec(self.device_id, cmd)
            print("Command executed successfully.")
        except Exception as e:
            print(f"Failed to execute command. Error: {e}")

    def output(self):
        time.sleep(3)
    
        self.execute_command("out:v(1:1):a(110.000)")
        self.execute_command("out:v(1:1):p(0.000)")
        self.execute_command("out:v(1:1):f(60.000)")
        self.execute_command("out:v(1:2):a(110.000)")
        self.execute_command("out:v(1:2):p(300.000)")
        self.execute_command("out:v(1:2):f(60.000)")
        self.execute_command("out:v(1:3):a(110.000)")
        self.execute_command("out:v(1:3):p(130.000)")
        self.execute_command("out:v(1:3):f(60.000)")

        # 전류 설정
        self.execute_command("out:i(1:1):a(1.000)")
        self.execute_command("out:i(1:1):p(0.000)")
        self.execute_command("out:i(1:1):f(60.000)")
        self.execute_command("out:i(1:2):a(1.000)")
        self.execute_command("out:i(1:2):p(-120.000)")
        self.execute_command("out:i(1:2):f(60.000)")
        self.execute_command("out:i(1:3):a(1.000)")
        self.execute_command("out:i(1:3):p(120.000)")
        self.execute_command("out:i(1:3):f(60.000)")

        # 출력 시작
        time.sleep(2)
        self.execute_command("out:on")
        time.sleep(5)
        self.execute_command("out:off")

    def start_output(self):
        self.is_outputting = True
        while self.is_outputting:
            self.output()
        self.execute_command("out:off")
        
        

    def stop_output(self):
        self.is_outputting = False
        # 출력 중지
        self.execute_command("out:off")
        

    #----<logging>-------------------------------------------------------------
    def devlog(self, msg):
        print(msg)
    def execlog(self,msg):
        print(msg)

    #----<even trigered by editFinished>---------------------------------------
    def _exitEdit(self):
        self.setFormatedText("","1")
        
    #----<logging>-------------------------------------------------------------
    def execlog(self,msg):
        print(msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CMEngine()
    window.show()
    sys.exit(app.exec())