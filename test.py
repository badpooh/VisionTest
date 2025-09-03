from function.func_ocr import PaddleOCRManager
from config.config_roi import ConfigROI as ConfigROI
from pymodbus.client import ModbusTcpClient as ModbusClient
import time
import threading
from config.config_map import ConfigMap
from config.config_touch import ConfigTouch

paddleocr_func = PaddleOCRManager()

class test:

    SERVER_IP = '10.10.26.156'
    TOUCH_PORT = '5200'
    SETUP_PORT = '502'
    is_connected = False

    def tcp_connect(self):
        if not self.SERVER_IP or not self.SETUP_PORT:
            print("Cannot connect: IP or PORT is missing.")
            return
        
        # self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
        self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

        # touch_ok = self.touch_client.connect()
        setup_ok = self.setup_client.connect()

        if setup_ok:
            self.is_connected = True
            print("is connected")
            print(setup_ok)
        else:
            # if not touch_ok:
            #     print("Failed to connect touch_client")
            if not setup_ok:
                print("Failed to connect setup_client")

    def check_connection(self):
        while self.is_connected:
            # if not self.touch_client.is_socket_open():
            #     print("Touch client disconnected, reconnecting...")
            #     if self.touch_client.connect():
            #         print("touch_client connected")
            if not self.setup_client.is_socket_open():
                print("Setup client disconnected, reconnecting...")
                if self.setup_client.connect():
                    print("setup_client connected")
            time.sleep(1)

    def start_monitoring(self):
        self.tcp_connect()
        threading.Thread(target=self.check_connection, daemon=True).start()
    
    def tcp_disconnect(self):
        self.setup_client.close()
        self.is_connected = False
        print("is disconnected")

    # def uitest_mode_start(self):
    #     if self.touch_client:
    #         self.touch_client.write_register(ConfigTouch.touch_addr_ui_test_mode.value, 1)
    #     else:
    #         print("client Error")

    def setup_initialization(self):
        # self.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]

        def value_32bit(value):
            return (value >> 16) & 0xFFFF, value & 0xFFFF

        if self.setup_client:
            for value in values:
                self.setup_client.write_register(ConfigMap.addr_setup_lock.value[0], value)
                time.sleep(0.6)
            for value_control in values_control:
                self.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            
            ### measurement setup ###
            self.setup_client.read_holding_registers(*ConfigMap.addr_measurement_setup_access.value)
            self.setup_client.write_register(ConfigMap.addr_wiring.value[0], 1)
            self.setup_client.write_register(ConfigMap.addr_measurement_setup_access.value[0], 1)
    
    def test001(self):
        image_path = r"C:\PNT\AutoProgram\Vision\image_test\10.10.26.159_2025-03-25_16_06_34_M_S_ME_Current.png"
        roi_keys = [ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2, ConfigROI.s_ct_secondary_curr_1, 
                    ConfigROI.s_ct_secondary_curr_2, ConfigROI.s_reference_curr_1, ConfigROI.s_reference_curr_2, 
                   ] # ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2, ConfigROI.s_min_meas_curr_1, ConfigROI.s_min_meas_curr_2, ConfigROI.s_tdd_reference_selection_1, ConfigROI.s_tdd_reference_selection_2,
        setup = 1
        ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)
        print(ocr_results)

    def test002(self):
        for i in range(3):
            self.start_monitoring()
            # self.setup_initialization()
            self.tcp_disconnect()
            print(i)


if __name__ == "__main__":
    start = test()
    start.test001()
    # start.test002()