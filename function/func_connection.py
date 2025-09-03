from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import time

class ConnectionManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.SERVER_IP = None  # 장치 IP 주소
            self.TOUCH_PORT = None  # 터치 포트
            self.SETUP_PORT = None  # 설정 포트
            self.is_connected = False
            self.touch_client = None
            self.setup_client = None
            self.initialized = True
    
    def ip_connect(self, selected_ip):
        self.SERVER_IP = selected_ip
        print(f"IP set to: {self.SERVER_IP}")
            
    def tp_update(self, selected_tp):
        self.TOUCH_PORT = selected_tp
    
    def sp_update(self, selected_sp):
        self.SETUP_PORT = selected_sp
        
    def tcp_connect(self):
        if not self.SERVER_IP or not self.TOUCH_PORT or not self.SETUP_PORT:
            print("Cannot connect: IP or PORT is missing.")
            return
        
        self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
        self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

        touch_ok = self.touch_client.connect()
        setup_ok = self.setup_client.connect()

        if touch_ok and setup_ok:
            self.is_connected = True
            print("is connected")
            print(setup_ok)
            print(touch_ok)
        else:
            if not touch_ok:
                print("Failed to connect touch_client")
            if not setup_ok:
                print("Failed to connect setup_client")

    def check_connection(self):
        while self.is_connected:
            if not self.touch_client.is_socket_open():
                print("Touch client disconnected, reconnecting...")
                if self.touch_client.connect():
                    print("touch_client connected")
            if not self.setup_client.is_socket_open():
                print("Setup client disconnected, reconnecting...")
                if self.setup_client.connect():
                    print("setup_client connected")
            time.sleep(1)

    def start_monitoring(self):
        self.tcp_connect()
        threading.Thread(target=self.check_connection, daemon=True).start()

    def tcp_disconnect(self):
        self.touch_client.close()
        self.setup_client.close()
        self.is_connected = False
        print("is disconnected")