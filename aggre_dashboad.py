from PySide6.QtWidgets import QMainWindow
from aggre_ui import Ui_Form
from aggre_function import ConnectionManager, CMEngine, ModbusManager

class MyDashBoard(QMainWindow, Ui_Form):
        
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("My DashBoard")
        
        # 외부에서 생성된 매니저 인스턴스를 저장합니다.
        self.connection_manager = ConnectionManager()
        cm_engine = CMEngine()
        self.cm_engine = cm_engine
        self.modbus_manager = ModbusManager(self.connection_manager)

        # UI 요소의 시그널과 슬롯을 연결합니다.
        self.btn_connect.clicked.connect(self.on_connect_clicked)
        self.btn_disconnect.clicked.connect(self.on_disconnect_clicked)

    def on_connect_clicked(self):
        ip_address = self.lineEdit_ip.text()
        self.connection_manager.ip_connect(ip_address)
        # 포트도 UI에서 입력받는다면 아래와 같이 추가할 수 있습니다.
        # self.connection_manager.tp_update(self.lineEdit_tp.text())
        # self.connection_manager.sp_update(self.lineEdit_sp.text())
        
        # 임시로 포트 값을 하드코딩합니다. 실제로는 UI에서 가져와야 합니다.
        self.connection_manager.tp_update(5100)
        self.connection_manager.sp_update(502)
        
        self.connection_manager.start_monitoring()

    def on_disconnect_clicked(self):
        self.connection_manager.tcp_disconnect()