from os import error
import re
import threading
import time
import numpy as np
import cv2
from datetime import datetime
import time
from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import shutil
import os
import pandas as pd
from itertools import chain
from paddleocr import PaddleOCR

from function.func_connection import ConnectionManager

from setup_test.setup_config import ConfigSetup
from setup_test.setup_config import ConfigTextRef as ec
from setup_test.setup_config import ConfigROI as ecr
from setup_test.setup_config import ConfigTouch as ect

config_data = ConfigSetup()


# class SetupModbusManager:

#     SERVER_IP = ''  # 장치 IP 주소
#     TOUCH_PORT = ''  # 내부터치
#     SETUP_PORT = ''  # 설정

#     def __init__(self):
#         self.SERVER_IP = ''  # 장치 IP 주소
#         self.TOUCH_PORT = ''  # 내부터치
#         self.SETUP_PORT = ''  # 설정
#         self.is_connected = False
#         self.touch_client = None
#         self.setup_client = None
    
#     def ip_connect(self, selected_ip):
#         self.SERVER_IP = selected_ip
#         print(f"IP set to: {self.SERVER_IP}")
            
#     def tp_update(self, selected_tp):
#         self.TOUCH_PORT = selected_tp
    
#     def sp_update(self, selected_sp):
#         self.SETUP_PORT = selected_sp
        
#     def tcp_connect(self):
#         if not self.SERVER_IP or not self.TOUCH_PORT or not self.SETUP_PORT:
#             print("Cannot connect: IP or PORT is missing.")
#             return
        
#         self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
#         self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

#         touch_ok = self.touch_client.connect()
#         setup_ok = self.setup_client.connect()

#         if touch_ok and setup_ok:
#             self.is_connected = True
#             print("is connected")
#         else:
#             if not touch_ok:
#                 print("Failed to connect touch_client")
#             if not setup_ok:
#                 print("Failed to connect setup_client")

#     def check_connection(self):
#         while self.is_connected:
#             if not self.touch_client.is_socket_open():
#                 print("Touch client disconnected, reconnecting...")
#                 if self.touch_client.connect():
#                     print("touch_client connected")
#             if not self.setup_client.is_socket_open():
#                 print("Setup client disconnected, reconnecting...")
#                 if self.setup_client.connect():
#                     print("setup_client connected")
#             time.sleep(1)

#     def start_monitoring(self):
#         self.tcp_connect()
#         threading.Thread(target=self.check_connection, daemon=True).start()

#     def tcp_disconnect(self):
#         self.touch_client.close()
#         self.setup_client.close()
#         self.is_connected = False
#         print("is disconnected")

class TouchManager:

    # mobus_manager = SetupModbusManager()
    mobus_manager = ConnectionManager()

    hex_value = int("A5A5", 16)

    def __init__(self):
        self.client_check = self.mobus_manager.touch_client
        self.coords_touch = config_data.touch_data()
        self.coords_color = config_data.color_detection_data()

    def touch_write(self, address, value, delay=0.6):
        attempt = 0
        # print("Touching", end='', flush=True)
        while attempt < 2:
            self.client_check.write_register(address, value)
            read_value = self.client_check.read_holding_registers(address)
            time.sleep(delay)
            if read_value == value:
                print("\nTouched")
                return
            else:
                attempt += 1
                # print(".", end='', flush=True) 
        # print(f"Failed to write value {value} to address {
        #       address}. Read back {read_value} instead.")

    def uitest_mode_start(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_ui_test_mode.value, 1)
        else:
            print("client Error")

    def screenshot(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_screen_capture.value, self.hex_value)
        else:
            print("client Error")

    def menu_touch(self, menu_key):
        if self.client_check:
            data_view_x, data_view_y = menu_key
            self.touch_write(ect.touch_addr_pos_x.value, data_view_x)
            self.touch_write(ect.touch_addr_pos_y.value, data_view_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Menu Touch Error")

    def btn_popup_touch(self, btn_popup_key):
        if self.client_check:
            btn_x, btn_y = self.coords_touch[btn_popup_key]
            self.touch_write(ect.touch_addr_pos_x.value, btn_x)
            self.touch_write(ect.touch_addr_pos_y.value, btn_y)
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Popup Touch Error")

    def number_1_touch(self, number_key):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(
                ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_2_touch(self, number_key1, number_key2):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def number_3_touch(self, number_key1, number_key2, number_key3):
        if self.client_check:
            number_x, number_y = self.coords_touch[number_key1]
            self.touch_write(ect.touch_addr_pos_x.value, number_x)
            self.touch_write(ect.touch_addr_pos_y.value, number_y)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_a, number_b = self.coords_touch[number_key2]
            self.touch_write(ect.touch_addr_pos_x.value, number_a)
            self.touch_write(ect.touch_addr_pos_y.value, number_b)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            number_c, number_d = self.coords_touch[number_key3]
            self.touch_write(ect.touch_addr_pos_x.value, number_c)
            self.touch_write(ect.touch_addr_pos_y.value, number_d)
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_popup_enter"][0])
            self.touch_write(
                ect.touch_addr_pos_y.value, self.coords_touch["btn_popup_enter"][1])
            self.touch_write(self.coords_TA["touch_mode"], 1)
            self.touch_write(self.coords_TA["touch_mode"], 0)
        else:
            print("Number Touch Error")

    def btn_apply_touch(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_pos_x.value, self.coords_touch["btn_apply"][0])
            self.touch_write(ect.touch_addr_pos_y.value, self.coords_touch["btn_apply"][1])
            self.touch_write(ect.touch_addr_touch_mode.value, 1)
            self.touch_write(ect.touch_addr_touch_mode.value, 0)
        else:
            print("Button Apply Touch Error")

    def btn_front_setup(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 2)
        else:
            print("Button Apply Touch Error")

    def btn_front_meter(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 64)
        else:
            print("Button Apply Touch Error")

    def btn_front_home(self):
        if self.client_check:
            self.touch_write(ect.touch_addr_setup_button.value, 0)
            self.touch_write(ect.touch_addr_setup_button_bit.value, 1)
        else:
            print("Button Apply Touch Error")

class OCRManager:

    def __init__(self, n=3):
        self.n = n
        self.config = ConfigSetup(n=self.n)
        self.rois = self.config.roi_params()
        self.phasor_condition = 0

    def color_detection(self, image, color_data):
        x, y, w, h, R, G, B = color_data
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        selected_area = image_rgb[y:y+h, x:x+w]
        average_color = np.mean(selected_area, axis=(0, 1))
        target_color = np.array([R, G, B])
        color_difference = np.linalg.norm(average_color - target_color)
        return color_difference
    
    def update_n(self, new_n):
        self.n = new_n
        self.config.update_n(new_n)
        self.rois = self.config.roi_params()
        # print(f"n 값이 {new_n}으로 변경되었습니다.")

    def update_phasor_condition(self, new_c):
        self.phasor_condition = new_c

    def ocr_basic(self, image, roi_keys):
        image = cv2.imread(image)
        if image is None:
            print(f"이미지를 읽을 수 없습니다: {image}")
            return []

        ocr = PaddleOCR(use_gpu=False, use_angle_cls=False, lang='en', use_space_char=True, show_log=False)

        ocr_results = {}
        for roi_key in roi_keys:
            # 이미지 처리
            if self.phasor_condition == 0:
                self.update_n(3)
                resized_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 30, 9, 21)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                sharpened_image = cv2.filter2D(denoised_image, -1, kernel)
            
            elif self.phasor_condition == 1:
                self.update_n(3)
                sharpened_image = cv2.resize(image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)

            else:
                print(f"Error {self.phasor_condition}")


            if roi_key in self.rois:
                extracted_texts = []
                low_confidence_texts = []
                x, y, w, h = self.rois[roi_key]
                roi_image = sharpened_image[y:y+h, x:x+w]

                # cv2.imshow("test", roi_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                
                text_results = ocr.ocr(roi_image, cls=False)
                original_results = []
                
                # text_results를 평탄화
                if text_results:
                    text_results_filtered = [tr for tr in text_results if tr is not None]
                    if text_results_filtered:
                        flat_text_results = list(chain.from_iterable(text_results_filtered))
                        for result in flat_text_results:
                            coords, (text, confidence) = result
                            text = text.strip()
                            confidence = float(confidence)
                            original_results.append((coords, text, confidence))
                            # 신뢰도 검사
                            if confidence >= 0.975:
                                pass
                                # extracted_texts.append(text)
                            else:
                                low_confidence_texts.append((coords, text, confidence))
                    else:
                        flat_text_results = []
                        extracted_texts.append("empty")
                else:
                    print("text_results error")

                height, width = roi_image.shape[:2]
                margin = 5
                # 신뢰도 낮은 텍스트 처리
                for coords, text, conf in low_confidence_texts:
                    max_retries = 3
                    retry_count = 0
                    success = False

                    print(f"ROI '{roi_key}'에서 신뢰도 98% 미만의 텍스트:")
                    print(f" - '{text}' (신뢰도: {conf * 100:.2f}%)")
                    # coords를 사용하여 해당 텍스트 영역 이미지 추출
                    x_min = max(0, int(min([pt[0] for pt in coords])) - margin)
                    x_max = min(width, int(max([pt[0] for pt in coords])) + margin)
                    y_min = max(0, int(min([pt[1] for pt in coords])) - margin)
                    y_max = min(height, int(max([pt[1] for pt in coords])) + margin)
                    text_roi = roi_image[y_min:y_max, x_min:x_max]

                    # 이미지 전처리 및 OCR 재시도
                    if text_roi.size == 0:
                        continue  # 유효하지 않은 영역은 건너뜁니다
                    while retry_count < max_retries and not success:
                        char_image = text_roi.copy()
                        ### 일반 텍스트 영역 / 97% 초과가 되지않으면 바로 실행
                        if retry_count == 0 and self.phasor_condition == 0:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)
                        
                        ### 그림 영역 / 97% 초과가 되지않으면 바로 실행 (Phasor와 같은 A, B, C 주위에 색박스로 된 부분)
                        elif retry_count == 0 and self.phasor_condition == 1:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, sharpening_kernel)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 100, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            edges = cv2.Canny(thresh_char, 50, 150)
                            char_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
                        
                        ### 일반 텍스트 영역 재시도 2번째
                        elif retry_count == 1 and self.phasor_condition == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 150, 255, cv2.THRESH_BINARY)
                            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(9, 9))
                            enhanced_char = clahe.apply(thresh_char)
                            char_image = cv2.cvtColor(enhanced_char, cv2.COLOR_GRAY2BGR)

                        ### 그림 영역 재시도 2번째
                        elif retry_count == 1 and self.phasor_condition == 1:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        ### 일반 텍스트 영역 재시도 3번째
                        elif retry_count > 1 and self.phasor_condition == 0:
                            self.update_n(3)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_LANCZOS4)
                            char_image = cv2.Canny(char_image, 0, 200)
                            kernel = np.array([
                                                [-1, -1, -1, -1, -1],
                                                [-1,  1,  1,  1, -1],
                                                [-1,  1,  5,  1, -1],
                                                [-1,  1,  1,  1, -1],
                                                [-1, -1, -1, -1, -1]], dtype=np.float32)
                            char_image = cv2.filter2D(char_image, -1, kernel)

                        elif retry_count > 1 and self.phasor_condition == 1:
                            self.update_n(4)
                            char_image = cv2.resize(char_image, None, fx=self.n, fy=self.n, interpolation=cv2.INTER_CUBIC)
                            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                            char_image = cv2.filter2D(char_image, -1, kernel2)
                            gray_char = cv2.cvtColor(char_image, cv2.COLOR_BGR2GRAY)
                            _, thresh_char = cv2.threshold(gray_char, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                            char_image = cv2.cvtColor(thresh_char, cv2.COLOR_GRAY2BGR)

                        # cv2.imshow("test2", char_image)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()

                        retry_result = ocr.ocr(char_image, cls=False)
                        print(f"재시도 OCR 결과 (시도 {retry_count}):", retry_result)
                        if retry_result and retry_result[0]:
                            flat_retry_result = list(chain.from_iterable(retry_result))
                            for res in flat_retry_result:
                                new_coords, (new_text, new_confidence) = res
                                new_text = new_text.strip()
                                new_confidence = float(new_confidence)

                                if new_confidence >= 0.94 or new_text.lower() == "c" or ((new_text.upper() == "V0" or new_text.upper() == "U0") and new_confidence >= 0.85):
                                    # original_results에서 해당 좌표를 찾아 업데이트
                                    for i, (orig_coords, orig_text, orig_conf) in enumerate(original_results):
                                        if orig_coords == coords:
                                            combined_text = self.merge_texts(orig_text, new_text, orig_coords, new_coords)
                                            original_results[i] = (orig_coords, combined_text, new_confidence)
                                            success = True
                                            break
                                    success = True
                                    break
                        else:
                            print("재시도 후에도 텍스트를 인식하지 못했습니다.")
                        retry_count += 1
                
                extracted_texts = [text for coords, text, conf in original_results]
                extracted_texts = ' '.join(extracted_texts)
                extracted_texts = self.handle_special_cases(extracted_texts)
                if extracted_texts:
                    ocr_results[roi_key] = extracted_texts
            else:
                print(f"{roi_key}가 self.rois에 존재하지 않습니다.")

        for roi_key, text in ocr_results.items():
            print(f'{roi_key}: {text}')

        # 유효한 텍스트만 리스트로 반환
        ocr_results_list = [text for text in ocr_results.values() if text]
        return ocr_results_list

    def merge_texts(self, orig_text, new_text, orig_coords, new_coords):
        if len(new_text) < len(orig_text):
            if new_coords[0][0] > orig_coords[0][0]:
                return orig_text[:len(orig_text)-len(new_text)] + new_text
            else:    
                return new_text + orig_text[len(new_text):]
        else:
            return new_text

    def handle_special_cases(self, text):
        words = text.strip().split()
        processed_words = []
        for i, word in enumerate(words):
            if word == 'V':
                has_word_before = (i > 0)
                has_word_after = (i < len(words) - 1)
                if has_word_before and has_word_after:
                    # 앞뒤로 단어가 있는 경우 'V'를 제외
                    print(f"예외 처리: '{word}'를 결과에서 제외")
                    continue  # 'V'를 결과에서 제외하고 다음 단어로 이동
            processed_words.append(word)
        return ' '.join(processed_words)

class ModbusLabels:

    touch_manager = TouchManager()
    
    meter_m_vol_mappings_value, meter_m_vol_mappings_uint16, meter_m_vol_mappings_uint32 = config_data.meter_m_vol_mapping()
    meter_m_cur_mappings_value, meter_m_cur_mappings_uint16, meter_m_cur_mappings_uint32 = config_data.meter_m_cur_mapping()

    def __init__(self):
        pass

    def read_all_modbus_values(self):
        self.read_results = {}
        for address, info in self.meter_m_vol_mappings_value.items():
            result = self.read_modbus_value(
                address, self.meter_m_vol_mappings_value)
            # self.results를 self.read_results로 바꿀껀데 검증 필요함
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint16.items():
            result = self.read_uint16(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_vol_mappings_uint32.items():
            result = self.read_uint32(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_value.items():
            result = self.read_modbus_value(
                address, self.meter_m_cur_mappings_value)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_uint16.items():
            result = self.read_uint16(address)
            self.read_results[info["description"]] = result
        for address, info in self.meter_m_cur_mappings_uint32.items():
            result = self.read_uint32(address)
            self.read_results[info["description"]] = result
        return self.read_results

    def read_modbus_value(self, address, mapping):
        response = self.setup_client.read_holding_registers(address, count=1)
        if response.isError():
            print("Error reading VALUE", address)
            return None
        else:
            value = response.registers[0]
            return mapping[address]["values"].get(value, "Unknown Value")

    def read_uint16(self, address):
        response = self.setup_client.read_holding_registers(address, count=1)
        if response.isError():
            print("Error reading UINT16", address)
            return None
        else:
            value = response.registers[0]
            return value

    def read_uint32(self, address):
        response = self.setup_client.read_holding_registers(address, count=2)
        if response.isError():
            print("Error reading UINT32", address)
            return None
        else:
            high_register = response.registers[0]
            low_register = response.registers[1]
            value = (low_register << 16) + high_register
            return value

    def check_for_changes(self, initial_values):
        if self.read_results:
            current_values = self.read_results
            changes = {}
            for description, current_value in current_values.items():
                initial_value = initial_values.get(description)
                if initial_value != current_value:
                    changes[description] = (initial_value, current_value)
            return changes
        else:
            print("read_results is empty")

    def display_changes(self, initial_values):
        changes = self.check_for_changes(initial_values)
        change_count = len(changes)
        if changes:
            print("Changes detected:")
            for description, (initial, current) in changes.items():
                print(f"Address {description}: Initial Value = {initial}, Current Value = {current}")
        else:
            print("No changes detected.")
        return change_count

    def demo_test_setting(self):
        self.touch_manager.uitest_mode_start()
        addr_setup_lock = 2900
        addr_control_lock = 2901
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value in values:
                self.response = self.modbus_manager.setup_client.write_register(addr_setup_lock, value)
                time.sleep(0.6)
            vol_value_32bit = 1900
            high_word = (vol_value_32bit >> 16) & 0xFFFF  # 상위 16비트
            low_word = vol_value_32bit & 0xFFFF
            self.response = self.modbus_manager.setup_client.read_holding_registers(6000, 100)
            self.response = self.modbus_manager.setup_client.read_holding_registers(6100, 100)
            self.response = self.modbus_manager.setup_client.read_holding_registers(6200, 3)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.modbus_manager.setup_client.write_register(6001, 0)
            self.response = self.modbus_manager.setup_client.write_registers(6003, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6005, [high_word, low_word])
            self.response = self.modbus_manager.setup_client.write_registers(6007, 1900)
            self.response = self.modbus_manager.setup_client.write_register(6009, 0)
            self.response = self.modbus_manager.setup_client.write_register(6000, 1)
            time.sleep(0.6)
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(4002, 0)
            self.response = self.modbus_manager.setup_client.write_register(4000, 1)
            self.response = self.modbus_manager.setup_client.write_register(4001, 1)
            print("Done")
        else:
            print(self.response.isError())
    
    def reset_max_min(self):
        self.touch_manager.uitest_mode_start()
        addr_control_lock = 2901
        values_control = [2300, 0, 1600, 1]
        if self.modbus_manager.setup_client:
            for value_control in values_control:
                self.response = self.modbus_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            self.response = self.modbus_manager.setup_client.write_register(ec.addr_reset_max_min.value, 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time


class Evaluation:

    reset_time = None
    ocr_manager = OCRManager()
    rois = config_data.roi_params()

    def __init__(self):
        self.m_home, self.m_setup = config_data.match_m_setup_labels()

    ### With Demo Balance ###
    def eval_demo_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        color_data = config_data.color_detection_data()
        
        image = cv2.imread(image_path)

        ocr_right = right_key

        right_list = ' '.join(text.strip() for text in ocr_right).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_counter = Counter(right_list)
        ocr_rt_counter = Counter(ocr_rt_list)

        self.ocr_error = list((ocr_rt_counter - right_counter).elements())
        right_error = list((right_counter - ocr_rt_counter).elements())

        def check_results(values, limits, ocr_meas_subset):
            self.condition_met = True
            meas_results = []

            if isinstance(ocr_meas_subset, (float, int)):
                results = {values[0]: str(ocr_meas_subset)}
            elif isinstance(ocr_meas_subset, list):
                results = {name: str(value) for name, value in zip(values, ocr_meas_subset)}
            else:
                print("Unexpected ocr_meas_subset type.")
                return

            for name, value in results.items():
                match = re.match(r"([-+]?\d+\.?\d*)\s*(\D*)", value)
                if match:
                    numeric_value = float(match.group(1))  # 숫자 부분
                    unit = match.group(2)  # 단위 부분 (예: V)
                else:
                    numeric_value = None
                    unit = value.strip()

                    # 텍스트 정답을 처리하는 로직 추가
                text_matches = [lim for lim in limits if isinstance(lim, str)]
                if any(text_match == value for text_match in text_matches):
                    print(f"{name or 'empty'} = {value} (PASS by text match)")
                    meas_results.append(f"{name or 'empty'} = {value} (PASS by text)")
                    
                elif numeric_value is not None and len(limits) >= 3 and isinstance(limits[0], (int, float)):
                    if limits[0] <= numeric_value <= limits[1] and limits[2] == unit:
                        print(f"{name} = {numeric_value}{unit} (PASS)")
                        meas_results.append(f"{numeric_value}{unit} (PASS)")
                    else:
                        print(f"{name} = {value} (FAIL)")
                        meas_results.append(f"{value} (FAIL)")
                        self.meas_error = True
                else:
                    print(f"{name} = {value} (FAIL)")
                    meas_results.append(f"{value} (FAIL)")
                    self.meas_error = True
            return meas_results
        
        all_meas_results = []

        if "RMS Voltage" in ''.join(ocr_res[0]) or "Fund. Volt." in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (180, 200, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, ecr.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (100, 120, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, ecr.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (2.0, 4.0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, ecr.color_vol_thd_ln.value) <= 10:
                    all_meas_results.extend(check_results(["A", "B", "C"], (3.0, 4.0, "%"), ocr_res_meas[:4]))
                else:
                    print("Total Harmonic missed")

        elif "Frequency" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["Freq"], (59, 61, "Hz"), ocr_res_meas[:1]))

        elif "Residual Voltage" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS", "Fund."], (0, 10, "V"), ocr_res_meas[:2]))

        elif "RMS Current" in ''.join(ocr_res[0]) or "Fundamental Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Aver %"], (45, 55, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (2, 3, "A"), ocr_res_meas[4:]))

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_curr.value) <= 10: 
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 3.0, "%"), ocr_res_meas[:3]))

        elif "Total Demand" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1, 2.5, "%"), ocr_res_meas[:3]))

        elif "Crest Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1.3, 1.6, ""), ocr_res_meas[:3]))

        elif "K-Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (1.2, 1.5, ""), ocr_res_meas[:3]))

        elif "Residual Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS"], (70, 100, "mA"), ocr_res_meas[:1]))
            all_meas_results.extend(check_results(["RMS"], (20, 40, "mA"), ocr_res_meas[1:2]))
            
        elif "Active Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Total %"], (40, 50, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (230, 240, "W"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (705, 715, "W"), ocr_res_meas[7:8]))
            
        elif "Reactive Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(20, 30, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (130, 145, "VAR"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (400, 420, "VAR"), ocr_res_meas[7:8]))
            
        elif "Apparent Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A', 'B', 'C', 'Total'],(45, 55, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (270, 280, "VA"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (810, 830, "VA"), ocr_res_meas[7:8]))
            
        elif "Power Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(45, 55, "Lag"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Total"], (0.860, 0.870, ""), ocr_res_meas[4:8]))
            
        elif "Phasor" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (180, 195, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (25, 35, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (-95, -85, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (145, 155, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vll.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, ecr.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (100, 120, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (-0.2, 5, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (-125, -115, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (115, 125, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vln.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_harmonics_vol.value) <= 10:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    all_meas_results.extend("PASS?")
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (3.0, 4.0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
            else:
                if img_result == 1 or img_result == 0:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (1, 1, ""), img_result))  
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.95, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (2, 5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (100, 120, "v" or "V"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                else:
                    all_meas_results.extend(check_results(["CURR_A_THD", "CURR_B_THD", "CURR_C_THD"], (1.5, 2.5, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["CURR_A_Fund", "CURR_B_Fund", "CURR_C_Fund"], (2, 3, "A"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.98, 1, ""), img_result))
                    
        elif "Waveform" in ''.join(ocr_res[0]):
            if 0 < img_result < 1:
                all_meas_results.extend(check_results(["waveform_image"], (0.945, 1, ""), img_result))
            else:
                all_meas_results.extend(check_results(["waveform_img_detect"], (1, 1, ""), img_result))
                
        elif "Volt. Symm. Component" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (180, 200, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V0'], (180, 200, "V0"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V1'], (100, 110, "V" or "v"), ocr_res_meas[3:4]))
                all_meas_results.extend(check_results(['V2'], (0, 2, "V" or "v"), ocr_res_meas[4:5]))
                all_meas_results.extend(check_results(['V0'], (0, 1, "V" or "v"), ocr_res_meas[5:6]))
                
        elif "Voltage Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["NEMA LL"], (0, 1, "LL"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["NEMA LN"], (0, 1, "LN"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "U2"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["U0"], (0, 1, "U0"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["NEMA LL", "NEMA LN", "U2", "U0"], (0, 1, "%"), ocr_res_meas[4:8]))
            
        elif "Curr. Symm. Component" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["I1"], (0, 1, "l1"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["I2"], (0, 1, "l2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["I0"], (0, 1, "l0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["I1"], (2, 3, "A"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["I2"], (0, 0.1, "A"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["I0"], (0, 0.1, "A"), ocr_res_meas[5:6]))
            
        elif "Current Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results([""], (0, 1, "empty"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "U2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U0"], (0, 1, "U0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results([""], (0, 1, "%"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["U2"], (0, 1, "%"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["U0"], (0, 0.5, "%"), ocr_res_meas[5:6]))
            
        elif "Demand Currnet" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A%", "B%", "C%", "Aver%"], (40, 60, "%"), ocr_res_meas[0:5]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (4, 6, "A"), ocr_res_meas[5:9]))
        
        elif not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res, all_meas_results,

    ### No source, No Demo ###
    def eval_none_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        color_data = config_data.color_detection_data()
        
        image = cv2.imread(image_path)

        right_list = ' '.join(text.strip() for text in right_key).split()
        ocr_rt_list = ' '.join(result.strip() for result in ocr_res).split()

        right_counter = Counter(right_list)
        ocr_rt_counter = Counter(ocr_rt_list)

        self.ocr_error = list((ocr_rt_counter - right_counter).elements())
        right_error = list((right_counter - ocr_rt_counter).elements())

        def check_results(values, limits, ocr_meas_subset):
            self.condition_met = True
            meas_results = []

            if isinstance(ocr_meas_subset, (float, int)):
                results = {values[0]: str(ocr_meas_subset)}
            elif isinstance(ocr_meas_subset, list):
                results = {name: str(value) for name, value in zip(values, ocr_meas_subset)}
            else:
                print("Unexpected ocr_meas_subset type.")
                return

            for name, value in results.items():
                match = re.match(r"([-+]?\d+\.?\d*)\s*(\D*)", value)
                if match:
                    numeric_value = float(match.group(1))  # 숫자 부분
                    unit = match.group(2)  # 단위 부분 (예: V)
                else:
                    numeric_value = None
                    unit = value.strip()

                    # 텍스트 정답을 처리하는 로직 추가
                text_matches = [lim for lim in limits if isinstance(lim, str)]
                if any(text_match == value for text_match in text_matches):
                    print(f"{name or 'empty'} = {value} (PASS by text match)")
                    meas_results.append(f"{name or 'empty'} = {value} (PASS by text)")
                    
                elif numeric_value is not None and len(limits) >= 3 and isinstance(limits[0], (int, float)):
                    if limits[0] <= numeric_value <= limits[1] and limits[2] == unit:
                        print(f"{name} = {numeric_value}{unit} (PASS)")
                        meas_results.append(f"{numeric_value}{unit} (PASS)")
                    else:
                        print(f"{name} = {value} (FAIL)")
                        meas_results.append(f"{value} (FAIL)")
                        self.meas_error = True
                else:
                    print(f"{name} = {value} (FAIL)")
                    meas_results.append(f"{value} (FAIL)")
                    self.meas_error = True
            return meas_results
        
        all_meas_results = []

        if "RMS Voltage" in ''.join(ocr_res[0]) or "Fund. Volt." in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, ecr.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, ecr.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, ecr.color_vol_thd_ln.value) <= 10:
                    all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:4]))
                else:
                    print("Total Harmonic missed")

        elif "Frequency" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["Freq"], (0, 0, "Hz"), ocr_res_meas[:1]))

        elif "Residual Voltage" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS", "Fund."], (0, 0, "V"), ocr_res_meas[:2]))

        elif "RMS Current" in ''.join(ocr_res[0]) or "Fundamental Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Aver %"], (0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "A"), ocr_res_meas[4:]))

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_main_menu_curr.value) <= 10: 
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:3]))

        elif "Total Demand" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "%"), ocr_res_meas[:3]))

        elif "Crest Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, ""), ocr_res_meas[:3]))

        elif "K-Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, ""), ocr_res_meas[:3]))

        elif "Residual Current" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["RMS"], (0, 0, "A"), ocr_res_meas[:1]))
            all_meas_results.extend(check_results(["RMS"], (0, 0, "A"), ocr_res_meas[1:2]))
            
        elif "Active Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A %", "B %", "C %", "Total %"], (0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kW"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kW"), ocr_res_meas[7:8]))
            
        elif "Reactive Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kVAR"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kVAR"), ocr_res_meas[7:8]))
            
        elif "Apparent Power" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A', 'B', 'C', 'Total'],(0, 0, "%"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "kVA"), ocr_res_meas[4:7]))
            all_meas_results.extend(check_results(["Total"], (0, 0, "kVA"), ocr_res_meas[7:8]))
            
        elif "Power Factor" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(['A%', 'B%', 'C%', 'Total%'],(0, 0, "No Load"), ocr_res_meas[:4]))
            all_meas_results.extend(check_results(["A", "B", "C", "Total"], (1, 1, ""), ocr_res_meas[4:8]))
            
        elif "Phasor" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vll_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, ecr.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([ecir.img_ref_phasor_all_vln_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_harmonics_vol.value) <= 10:
                if img_result is not None:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (0, 0, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.9, 1, ""), img_result))
                    all_meas_results.extend(check_results(["VOL_A_THD", "VOL_B_THD", "VOL_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    all_meas_results.extend(check_results(["VOL_A_Fund", "VOL_B_Fund", "VOL_C_Fund"], (0, 0, "v"), ocr_res_meas[3:6]))
                    all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    print(ocr_res_meas)
                    all_meas_results.extend(check_results(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], (0, 0, ""), ocr_res_meas[0:10]))
                    print("test")
            else:
                if img_result is not None:
                    all_meas_results.extend(check_results(["harmonics_img_detect"], (0.9, 1, ""), img_result))  
                    # all_meas_results.extend(check_results(["CURR_A_THD", "CURR_B_THD", "CURR_C_THD"], (0, 0, "%"), ocr_res_meas[:3]))
                    # all_meas_results.extend(check_results(["CURR_A_Fund", "CURR_B_Fund", "CURR_C_Fund"], (0, 0, "A"), ocr_res_meas[3:6]))
                    # all_meas_results.extend(check_results(["harmonic_image"], (0.9, 1, ""), img_result))
                elif "[%]Fund" in ''.join(ocr_res[1]) or "[%]RMS" in ''.join(ocr_res[1]):
                    all_meas_results.extend(check_results(["harmonic_%_img"], (0.9, 1, ""), img_result))
                elif "Text" in ''.join(ocr_res[1]):
                    all_meas_results.extend("PASS?")
            
                    
        elif "Waveform" in ''.join(ocr_res[0]):
            if 0 < img_result < 1:
                all_meas_results.extend(check_results(["waveform_image"], (0.945, 1, ""), img_result))
            else:
                all_meas_results.extend(check_results(["waveform_img_detect"], (1, 1, ""), img_result))
                
        elif "Volt. Symm. Component" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (0, 0, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (0, 0, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, ecr.color_symm_thd_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (0, 0, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V0'], (0, 0, "V0"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V1'], (0, 0, "V" or "v"), ocr_res_meas[3:4]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V" or "v"), ocr_res_meas[4:5]))
                all_meas_results.extend(check_results(['V0'], (0, 0, "V" or "v"), ocr_res_meas[5:6]))
                
        elif "Voltage Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["NEMA LL"], (0, 0, "LL"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["NEMA LN"], (0, 0, "LN"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "U2"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "U0"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["NEMA LL", "NEMA LN", "U2", "U0"], (0, 1, "%"), ocr_res_meas[4:8]))
            
        elif "Curr. Symm. Component" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["I1"], (0, 0, "l1"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["I2"], (0, 0, "l2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["I0"], (0, 0, "l0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results(["I1"], (0, 0, "A"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["I2"], (0, 0, "A"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["I0"], (0, 0, "A"), ocr_res_meas[5:6]))
            
        elif "Current Unbalance" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results([""], (0, 0, "empty"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "U2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "U0"), ocr_res_meas[2:3]))
            all_meas_results.extend(check_results([""], (0, 0, "%"), ocr_res_meas[3:4]))
            all_meas_results.extend(check_results(["U2"], (0, 0, "%"), ocr_res_meas[4:5]))
            all_meas_results.extend(check_results(["U0"], (0, 0, "%"), ocr_res_meas[5:6]))
        
        elif "Demand Currnet" in ''.join(ocr_res[0]):
            all_meas_results.extend(check_results(["A%", "B%", "C%", "Aver%"], (0, 0, "%"), ocr_res_meas[0:5]))
            all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "A"), ocr_res_meas[5:9]))
            
        elif not self.condition_met:
            print("Nothing matching word")

        print(f"OCR - 정답: {self.ocr_error}")
        print(f"정답 - OCR: {right_error}")

        return self.ocr_error, right_error, self.meas_error, ocr_res, all_meas_results
    
    def check_text(self, ocr_results):
        results = []
        
        for value in ocr_results:
            if value.replace('.', '', 1).isdigit():
                result = f"{value} (PASS)"
            else:
                result = f"{value} (FAIL)"
            
            # 결과 리스트에 추가
            results.append(result)
        
        # 결과를 하나의 문자열로 합치기
        final_result = ", ".join(results)
        print(final_result)
        
        return final_result
    
    def img_match(self, image, roi_key, tpl_img_path):
            template_image_path = tpl_img_path
            image = cv2.imread(image)
            template_image = cv2.imread(template_image_path)
            x, y, w, h = self.rois[roi_key]
            # print(f"ROI coordinates: x={x}, y={y}, w={w}, h={h}")
            # print(f"Original image size: {image.shape}")
            # print(f"Template image size: {template_image.shape}")
            cut_img = image[y:y+h, x:x+w]
            cut_template = template_image[y:y+h, x:x+w]

            resized_cut_img = cv2.resize(
                cut_img, (cut_template.shape[1], cut_template.shape[0]))
            res = cv2.matchTemplate(
                resized_cut_img, cut_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            print(max_val)
            
            return max_val
    
    def img_detection(self, image_path, color_data, tolerance):
        image = cv2.imread(image_path)
        x, y, w, h, R, G, B = color_data
        cut_img = image[y:y+h, x:x+w]

        # cv2.imshow('Image', cut_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
        target_color = np.array([B, G, R])
        diff = np.abs(cut_img - target_color)
        match = np.all(diff <= tolerance, axis=2)

        if np.array_equal(target_color, np.array([0, 0, 0])):
            target_color = "Vol_A(X)"
        elif np.array_equal(target_color, np.array([37, 29, 255])):  # BGR 순서로 비교
            target_color = "Vol_B(X)"
        elif np.array_equal(target_color, np.array([255, 0, 0])):
            target_color = "Vol_C(X)"
        elif np.array_equal(target_color, np.array([153, 153, 153])):
            target_color = "Curr_A(X)"
        elif np.array_equal(target_color, np.array([245, 180, 255])):  # BGR 순서로 비교
            target_color = "Curr_B(X)"
        elif np.array_equal(target_color, np.array([255, 175, 54])):  # BGR 순서로 비교
            target_color = "Curr_C(X)"

        if np.any(match):
            print(f"{target_color} (FAIL)")
            result = 0
            csv_result = f"{target_color} FAIL"
        else:
            print(f"{target_color} (PASS)")
            result = 1
            csv_result = f"{target_color} PASS"
        return result, csv_result

    def check_time_diff(self, image, roi_keys, reset_time, test_mode):
        self.reset_time = reset_time
        if not self.reset_time:
            self.reset_time = datetime.now()

        ocr_results_time = self.ocr_manager.ocr_basic(image, roi_keys)

         # 유효한 텍스트만 리스트로 반환
        time_images = [text for text in ocr_results_time if text]

        time_format = "%Y-%m-%d %H:%M:%S"
        time_results = []
        for time_str in time_images:
            try:
                image_time = datetime.strptime(time_str, time_format)
                image_time = image_time.replace(tzinfo=timezone.utc)
                time_diff = abs((image_time - self.reset_time).total_seconds())
                if test_mode == "Demo":
                    if time_diff <= 120:
                        print(f"{time_str} (PASS)")
                        time_results.append(f"{time_str} (PASS)")
                    else:
                        print(f"{time_str} / {time_diff} seconds (FAIL)")
                        time_results.append(f"{time_str} / {time_diff} seconds (FAIL)")
                else:
                    if time_diff <= 5:
                        print(f"{time_str} (PASS)")
                        time_results.append(f"{time_str} (PASS)")
                    else:
                        print(f"{time_str} / {time_diff} seconds (FAIL)")
                        time_results.append(f"{time_str} / {time_diff} seconds (FAIL)")
            except ValueError as e:
                print(f"Time format error for {time_str}: {e}")
                time_results.append(f"{time_str} / format error (FAIL)")
        return time_results


    def save_csv(self, ocr_img, ocr_error, right_error, meas_error=False, ocr_img_meas=None, ocr_img_time=None, time_results=None, img_path=None, img_result=None, base_save_path=None, all_meas_results=None, invalid_elements=None):
        ocr_img_meas = ocr_img_meas if ocr_img_meas is not None else []
        # ocr_img_time = ocr_img_time if ocr_img_time is not None else []
        time_results = time_results if time_results is not None else []
        img_result = [img_result]

        if invalid_elements is None:
            invalid_elements = []

        if ocr_img_meas == bool:
            ocr_img_meas = []
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(time_results)+1, len(img_result)+1)
        else:
            num_entries = max(len(ocr_img), len(ocr_img_meas)+1, len(time_results)+1, len(img_result)+1)

        overall_result = "PASS"
        if ocr_error or right_error or meas_error:
            overall_result = "FAIL"
        if any("FAIL" in result for result in time_results):
            overall_result = "FAIL"
        
        if all_meas_results is not None:
            measurement_results = [f"{meas}" for meas in all_meas_results]
            if len(measurement_results) < num_entries:
                measurement_results = [None] + measurement_results + [None] * (num_entries - len(measurement_results) - 1)
            
            csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "Measurement": measurement_results,
            "OCR-Right": [None] + [f"{ocr_error} ({'FAIL' if ocr_error else 'PASS'})"] + [""]* (num_entries-2),
            "Right-OCR": [None] + [f"{right_error} ({'FAIL' if right_error else 'PASS'})"] + [""]* (num_entries-2),
            f"Time Stamp ({self.reset_time})": [None] + time_results + [None] * (num_entries - len(time_results)-1),
            "Img Match": [None] + img_result + [None] * (num_entries-len(img_result)-1),
            "H.Text": [None] + invalid_elements + [None] * (num_entries-len(img_result)-1),
            }
        
        else:
            csv_results = {
            "Main View": ocr_img + [None] * (num_entries - len(ocr_img)),
            "OCR-Right": [None] + [f"{ocr_error} ({'FAIL' if ocr_error else 'PASS'})"] + [""]* (num_entries-2),
            "Right-OCR": [None] + [f"{right_error} ({'FAIL' if right_error else 'PASS'})"] + [""]* (num_entries-2),
            f"Time Stemp ({self.reset_time})": [None] + time_results + [None] * (num_entries - len(time_results)-1),
            "Img Match": [None] + img_result + [None] * (num_entries-len(img_result)-1),
            "H.Text": [None] + invalid_elements + [None] * (num_entries-len(img_result)-1),
            }
        
        
        # Ensure all columns have the same length
        for key in csv_results:
            csv_results[key] = csv_results[key][:num_entries]
            if len(csv_results[key]) < num_entries:
                csv_results[key].extend([None] * (num_entries - len(csv_results[key])))

        df = pd.DataFrame(csv_results)

        # Saving the CSV
        file_name_with_extension = os.path.basename(img_path)
        ip_to_remove = f"{SERVER_IP}_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        image_file_name = os.path.splitext(file_name_without_ip)[0]
        
        save_path = os.path.join(base_save_path, f"{overall_result}_ocr_{image_file_name}.csv")

        df.to_csv(save_path, index=False)
        dest_image_path = os.path.join(base_save_path, file_name_without_ip)
        shutil.copy(img_path, dest_image_path)

    def count_csv_and_failures(self, folder_path):
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        total_csv_files = len(csv_files)

        fail_count = sum(1 for f in csv_files if 'FAIL' in f)

        return total_csv_files, fail_count
    
    def validate_ocr(self, ocr_img):     
        def is_float(value):
            try:
                float(value)
                return True
            except ValueError:
                return False
        def process_text(text):
            elements = text.split()
            numbers = []
            invalid_elements = []

            for elem in elements:
                if is_float(elem):
                    numbers.append(float(elem))
                else:
                    invalid_elements.append(elem)
            return numbers, invalid_elements

        for result in ocr_img:
            numbers, invalid_elements = process_text(result)
            
            if invalid_elements:
                print(f"FAIL: {invalid_elements}")
            else:
                print("PASS")
            
            print(f"추출된 숫자: {numbers}")
        return invalid_elements