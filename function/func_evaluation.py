import re
import numpy as np
import cv2
from datetime import datetime, timezone
import shutil
import os
import glob
import pandas as pd
from collections import Counter
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import time
import datetime

from function.func_ocr import PaddleOCRManager
from function.func_connection import ConnectionManager

from config.config_roi import Configs
from config.config_color import ConfigColor as cc
from config.config_ref import ConfigImgRef as cr
from config.config_map import ConfigMap as ConfigMap
from config.config_map import ConfigInitialValue as civ

class Evaluation:

    reset_time = None
    ocr_manager = PaddleOCRManager()
    config_data = Configs()
    rois = config_data.roi_params()
    connect_manager = ConnectionManager()

    def __init__(self):
        pass

    def load_image_file(self, search_pattern):
        self.now = datetime.now()
        self.file_time_diff = {}

        for file_path in glob.glob(search_pattern, recursive=True):
            creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
            time_diff = abs((self.now - creation_time).total_seconds())
            self.file_time_diff[file_path] = time_diff

        closest_file = min(self.file_time_diff,
                            key=self.file_time_diff.get, default=None)
        normalized_path = os.path.normpath(closest_file)
        self.latest_image_path = normalized_path

        print("가장 가까운 시간에 생성된 파일:", normalized_path)

        return self.latest_image_path

    ### With Demo Balance ###
    def eval_demo_test(self, ocr_res, correct_answers, test_step, reset_time=None, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        
        image = cv2.imread(image_path)

        def validate_percent(self, percent_list, lower_limit, upper_limit):
            percent_error = False
            for item in percent_list:
                match = re.match(r"([-+]?\d+\.?\d*)\s*(.*)", item)

                if match and match.group(1):
                    numeric_value = float(match.group(1))
                    unit = match.group(2).strip()

                    if unit == '%' and lower_limit < numeric_value < upper_limit:
                        print(f"'{item}' -> (PASS)")
                    else:
                        print(f"'{item}' -> (FAIL - 단위 또는 범위 오류)")
                        percent_error = True
                else:
                    print(f"'{item}' -> (INFO - Skipping non-numeric text)")
            
            return percent_error
        
        def validate_timestamp(self, timestamp_list, reset_time):
            timestamp_error = False
            for item in timestamp_list:
                dt_object = datetime.datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
                unix_timestamp = dt_object.timestamp()

                if reset_time - 30 < unix_timestamp < reset_time + 30:
                    print(f"'{item}' -> (PASS)")
                else:
                    print(f"'{item}' -> (FAIL - 단위 또는 범위 오류)")
                    timestamp_error = True
            
            return timestamp_error

        ### 고정 문자 가공 ###
        ocr_fixed_text = [result.strip() for result in ocr_res[:2]]
        ####################

        ### 변동 문자 가공 ###
        ocr_percent_text_tuple = re.findall(r'(\d+\.\d+\s*%)|([A-Z]+\s*%)', ocr_res[2])
        ocr_percent_text = [item1 + item2 for item1, item2 in ocr_percent_text_tuple]
        ocr_timestamp_text = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', ocr_res[2])
        ocr_measurement_text = re.findall(r'\d+\.\d+\s+[A-Za-z%]+', ocr_res[3])
        ####################

        ### 고정 문자 중 잘못된 문자 검증 ###
        ocr_fixed_text_counter = Counter(ocr_fixed_text)
        correct_answers_counter = Counter(correct_answers)

        self.ocr_error = list((ocr_fixed_text_counter - correct_answers_counter).elements())
        ocr_missing_item = list((correct_answers_counter - ocr_fixed_text_counter).elements())
        ####################
        
        all_meas_results = []

        ### 검사 test_step 개념: Relay:1, Meter:2, CURRENT:02, RMS:001, LL:0001

        if test_step == 221:
            all_meas_results.append(validate_percent(ocr_percent_text, 49.5, 50.5))

        if "RMS Voltage" in ocr_res[0]:
            if self.ocr_manager.color_detection(image, cc.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (180, 200, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, cc.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (100, 120, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, cc.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (2.0, 4.0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, cc.color_vol_thd_ln.value) <= 10:
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
            if self.ocr_manager.color_detection(image, cc.color_main_menu_curr.value) <= 10: 
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
            if self.ocr_manager.color_detection(image, cc.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (180, 195, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (25, 35, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (-95, -85, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (145, 155, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vll.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, cc.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (100, 120, "V" or "v"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (2, 3, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (-0.2, 5, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (-125, -115, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (115, 125, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (-35, -25, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (-155, -145, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (85, 95, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vln.value], (0.98, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_harmonics_vol.value) <= 10:
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
            if self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (180, 200, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (180, 200, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (180, 200, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 1, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
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
            all_meas_results.extend(check_results(["I1"], (0, 1, "I1"), ocr_res_meas[0:1]))
            all_meas_results.extend(check_results(["I2"], (0, 1, "I2"), ocr_res_meas[1:2]))
            all_meas_results.extend(check_results(["I0"], (0, 1, "I0"), ocr_res_meas[2:3]))
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
        print(f"정답 - OCR: {ocr_missing_item}")

        return self.ocr_error, ocr_missing_item, self.meas_error, ocr_res, all_meas_results,

    ### No source, No Demo ###
    def eval_none_test(self, ocr_res, right_key, ocr_res_meas=None, image_path=None, img_result=None):
        self.meas_error = False
        self.condition_met = False
        
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
            if self.ocr_manager.color_detection(image, cc.color_rms_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            elif self.ocr_manager.color_detection(image, cc.color_rms_vol_ln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C", "Aver"], (0, 0, "V"), ocr_res_meas[:5]))
            else:
                print("RMS Voltage missed")

        elif "Total Harmonic" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_main_menu_vol.value) <= 10: 
                if self.ocr_manager.color_detection(image, cc.color_vol_thd_ll.value) <= 10:
                    all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "%"), ocr_res_meas[:4]))
                elif self.ocr_manager.color_detection(image, cc.color_vol_thd_ln.value) <= 10:
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
            if self.ocr_manager.color_detection(image, cc.color_main_menu_curr.value) <= 10: 
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
            if self.ocr_manager.color_detection(image, cc.color_phasor_vll.value) <= 10:
                all_meas_results.extend(check_results(["AB", "BC", "CA"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["AB_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["BC_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["CA_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vll_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0.99, 1, ""), img_result[1:3]))
                
            elif self.ocr_manager.color_detection(image, cc.color_phasor_vln.value) <= 10:
                all_meas_results.extend(check_results(["A", "B", "C"], (0, 0, "V"), ocr_res_meas[:3]))
                all_meas_results.extend(check_results(["A_Curr", "B_Curr", "C_Curr"], (0, 0, "A"), ocr_res_meas[3:6]))
                all_meas_results.extend(check_results(["A_angle"], (0, 0, ""), ocr_res_meas[6:7]))
                all_meas_results.extend(check_results(["B_angle"], (0, 0, ""), ocr_res_meas[7:8]))
                all_meas_results.extend(check_results(["C_angle"], (0, 0, ""), ocr_res_meas[8:9]))
                all_meas_results.extend(check_results(["A_angle_cur"], (0, 0, ""), ocr_res_meas[9:10]))
                all_meas_results.extend(check_results(["B_angle_cur"], (0, 0, ""), ocr_res_meas[10:11]))
                all_meas_results.extend(check_results(["C_angle_cur"], (0, 0, ""), ocr_res_meas[11:12]))
                all_meas_results.extend(check_results([cr.img_ref_phasor_all_vln_none.value], (0.99, 1, ""), img_result[0]))
                all_meas_results.extend(check_results(["angle_image_1", "angle_image_2"], (0, 1, ""), img_result[1:3]))
                
            else:
                print("demo test evaluation error")

        elif "Harmonics" in ''.join(ocr_res[0]):
            if self.ocr_manager.color_detection(image, cc.color_harmonics_vol.value) <= 10:
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
            if self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ll.value) <= 10:
                all_meas_results.extend(check_results(['V1'], (0, 0, "V1"), ocr_res_meas[0:1]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V2"), ocr_res_meas[1:2]))
                all_meas_results.extend(check_results(['V1'], (0, 0, "V" or "v"), ocr_res_meas[2:3]))
                all_meas_results.extend(check_results(['V2'], (0, 0, "V" or "v"), ocr_res_meas[3:4]))
            elif self.ocr_manager.color_detection(image, cc.color_symm_thd_vol_ln.value) <= 10:
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
    
    def eval_setup_test(self, ocr_res, setup_expected_value, title, ecm_access_address, ecm_address, modbus_ref, modbus_unit=None, eval_type=None, sm_res=None, sm_condition=None, except_addr=None):
        """
        ocr_res: OCR 결과 리스트
        sm_res:  AccurSM 결과
        except_addr: 검사에서 제외해야 할 ConfigModbusMap 멤버의 집합 (예: {ConfigModbusMap.addr_wiring, ...})
        """

        if except_addr is None:
            except_addr = set()

        def check_configuration(title, ecm_access_address, ecm_address, modbus_ref, setup_expected_value=None):
            result_condition_1 = False
            setup_result = [
                                "Error", 
                                "No specific PASS/FAIL condition was met in the logic.",
                                f"OCR Title: {ocr_res[0]}",
                                f"OCR Value: {ocr_res[1]}",
                                f"{setup_expected_value}"
                            ]

            address, words = ecm_address.value
            
            if title in ''.join(ocr_res[0]):
                if ecm_access_address:
                    self.connect_manager.setup_client.read_holding_registers(*ecm_access_address)
                current_modbus = self.connect_manager.setup_client.read_holding_registers(*ecm_address.value)
                decoder = BinaryPayloadDecoder.fromRegisters(current_modbus.registers, byteorder=Endian.BIG)
                decoded_value = decoder.decode_16bit_int()
                
                # high_word = current_modbus.register[0]
                high_word = decoded_value
                if words == 2:
                    low_word = current_modbus.registers[1]
                    full_32 = (high_word << 16) | low_word  # unsigned 32bit
                val = ocr_res[1]

                if words == 1:
                    if ocr_res[1] == setup_expected_value:
                        ### Devie UI, modbus, sm > pass / 설정값이 문자열
                        if sm_res:
                            if setup_expected_value != "Infinite":
                                if eval_type == 'SELECTION':
                                    if high_word == modbus_ref and sm_condition == True:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']

                                elif eval_type == 'INTEGER':
                                    if high_word == int(modbus_ref)and sm_condition == True:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                
                                elif eval_type == 'FLOAT':
                                    if high_word == float(modbus_ref)*10 and sm_condition == True:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word*0.1}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word*0.1}/{modbus_ref}', f'AccuraSM = {sm_res}']

                            elif setup_expected_value == "Infinite" and eval_type == 'INTEGER':
                                setup_expected_value = 0
                                if high_word == int(setup_expected_value) and sm_condition == True:
                                    setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', 
                                    f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    result_condition_1 = True  
                                else:
                                    setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', 
                                    f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                            
                            else:
                                print("(AccuraSM) Test Mode Timeout[min] Error")

                        else:
                            if setup_expected_value != "Infinite":
                                if eval_type == 'SELECTION':
                                    if high_word == modbus_ref:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']

                                elif eval_type == 'INTEGER':
                                    if high_word == int(modbus_ref):
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                
                                elif eval_type == 'FLOAT':
                                    if high_word == float(modbus_ref)*10:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word*0.1}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True                         
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {high_word*0.1}/{modbus_ref}', f'AccuraSM = {sm_res}']

                            elif setup_expected_value == "Infinite" and eval_type == 'INTEGER':
                                setup_expected_value = 0
                                if high_word == int(setup_expected_value):
                                    setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', 
                                    f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    result_condition_1 = True  
                                else:
                                    setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', 
                                    f'Modbus = {high_word}/{modbus_ref}', f'AccuraSM = {sm_res}']
                            
                            else:
                                print("(AccuraSM) Test Mode Timeout[min] Error")

                    else:
                        setup_result = [f'{ocr_res[1]} != {setup_expected_value}']
                        print(f"{setup_result}: 이 부분에서 예외 사항으로 에러")

                elif words == 2:
                    if  ocr_res[1] == setup_expected_value:
                        if sm_res:
                            if setup_expected_value != "Reference Current":
                                if modbus_unit == 1:
                                    if (full_32 *0.1) == float(setup_expected_value) and sm_condition == True:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32 *0.1}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32 *0.1}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                else:
                                    if (full_32) == float(setup_expected_value) and sm_condition == True:
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{setup_expected_value}', f'AccuraSM = {sm_res}']

                            elif setup_expected_value == "Reference Current":
                                setup_expected_value = 0
                                if full_32 == int(setup_expected_value) and sm_condition == True:
                                    setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    result_condition_1 = True
                                else:
                                    setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    print(f"{full_32}, {setup_expected_value}, {type(full_32)}, {type(setup_expected_value)}")
                            else:
                                print("(AccuraSM) Current TDD Nominal Currrent Error")

                        else:
                            if setup_expected_value != "Reference Current":
                                if modbus_unit == 1:
                                    if (full_32 *0.1) == float(setup_expected_value):
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32 *0.1}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32 *0.1}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                else:
                                    if (full_32) == float(setup_expected_value):
                                        setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{setup_expected_value}', f'AccuraSM = {sm_res}']
                                        result_condition_1 = True
                                    else:
                                        setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{setup_expected_value}', f'AccuraSM = {sm_res}']

                            elif setup_expected_value == "Reference Current":
                                setup_expected_value = 0
                                if full_32 == int(setup_expected_value):
                                    setup_result = [f'PASS', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    result_condition_1 = True
                                else:
                                    setup_result = [f'FAIL', f'Device = {ocr_res[1]}/{setup_expected_value}', f'Modbus = {full_32}/{modbus_ref}', f'AccuraSM = {sm_res}']
                                    print(f"{full_32}, {setup_expected_value}, {type(full_32)}, {type(setup_expected_value)}")
                            else:
                                print("Current TDD Nominal Currrent Error")

                    else:
                        setup_result = [f'{ocr_res[1]} != {setup_expected_value}']
                        print(f"{setup_result}: 이 부분에서 예외 사항으로 에러")
                else:
                    print("words == 1,2: 이 부분에서 예외 사항으로 에러")

            else:
                setup_result = [f'{ocr_res[0]} != {title}']
                  
            return setup_result, result_condition_1
        
        if ocr_res:
            setup_result, ressult_condition_1 = check_configuration(
                title=title, 
                ecm_access_address=ecm_access_address, 
                ecm_address=ecm_address,
                modbus_ref=modbus_ref,
                setup_expected_value=setup_expected_value)
        else:
            setup_result = ['OCR result is None']
            ressult_condition_1 = False

        evaluation_results = {}

        for modbus_enum, expected in civ.initial_setup_values.value.items():
            if modbus_enum in except_addr:
                continue

            address, words = modbus_enum.value
            response = None  # 응답 변수 초기화
            max_attempts = 2 # 총 시도 횟수 (기본 1회 + 재시도 1회)

            for attempt in range(max_attempts):
                # Modbus 읽기 시도
                response = self.connect_manager.setup_client.read_holding_registers(address, words)
                
                # 응답이 성공적인지 확인
                if not isinstance(response, (ModbusIOException, ExceptionResponse)):
                    # 성공 시, 재시도 루프를 즉시 빠져나감
                    break
                
                # 실패 시, 로그를 남기고 잠시 대기 후 재시도
                print(f"Warning: Modbus read failed on attempt {attempt + 1}/{max_attempts}. Retrying...")
                time.sleep(1) # 1초 대기 후 재시도
            # -------------------- 재시도 로직 종료 --------------------

            # 모든 재시도 후에도 최종적으로 응답이 실패했는지 다시 한번 확인
            if isinstance(response, (ModbusIOException, ExceptionResponse)) or response is None:
                print(f"Error: All {max_attempts} attempts to read {modbus_enum.name} failed. Skipping.")
                continue # 다음 항목으로 넘어감

            if words is None:
                continue
            elif words == 1:
                current_value = response.registers[0]
            elif words == 2:
                high = response.registers[0]
                low = response.registers[1]
                current_value = (high << 16) | low
            else:
                current_value = None
            
            if expected is not None and current_value != expected:
                evaluation_results[modbus_enum] = {
                    "expected": expected,
                    "current": current_value
                }

        result_condition_2 = False
        modbus_result = []
        if evaluation_results:
            print("변경되지 말아야 할 레지스터 중 차이가 발견되었습니다:")
            for addr_enum, diff in evaluation_results.items():
                meassage = f"FAIL, 주소 {addr_enum.value}: 예상 {diff['expected']}, 실제 {diff['current']}"
                modbus_result.append(meassage)
                print(f"주소 {addr_enum.value}: 예상 {diff['expected']}, 실제 {diff['current']}")
        else:
            modbus_result = 'PASS(others)'
            result_condition_2 = True
            print("모든 변경되지 말아야 할 레지스터가 정상입니다.")

        overall_result = 'PASS' if ressult_condition_1 and result_condition_2 else 'FAIL'
        
        return title, setup_result, modbus_result, overall_result

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

        setup = 0
        ocr_results_time = self.ocr_manager.paddleocr_basic(image, roi_keys, test_type=setup)

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
        ip_to_remove = f"{self.connect_manager.SERVER_IP}_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        image_file_name = os.path.splitext(file_name_without_ip)[0]
        
        save_path = os.path.join(base_save_path, f"{overall_result}_ocr_{image_file_name}.csv")

        df.to_csv(save_path, index=False)
        dest_image_path = os.path.join(base_save_path, file_name_without_ip)
        shutil.copy(img_path, dest_image_path)

    def setup_save_csv(self, setup_result, modbus_result, img_path, base_save_path, overall_result, title):
        """
        setup_result: list,  예) ['PASS', 'Device = Delta', 'Modbus = 1', 'AccuraSM = Wye']
        modbus_result: str, 예) 'PASS'
        img_path:   원본 이미지 파일 경로
        base_save_path: CSV/이미지 저장할 폴더
        overall_result: 최종 결과(예: 'PASS', 'FAIL' 등)를 파일명에 사용
        title: 테스트 항목목
        """
        setup_result_str = ', '.join(setup_result)
        
        extra_row = {
            "Device Setup Result": setup_result_str,
            "Device Other Modbus Result": modbus_result
        }
        df = pd.DataFrame([extra_row])

        # 3) 파일명 가공
        # 이미지 파일명에서 서버 IP부분을 제거
        file_name_with_extension = os.path.basename(img_path)  # 예: "10.10.20.30_screenshot.png"
        ip_to_remove = f"{self.connect_manager.SERVER_IP}_"    # 예: "10.10.20.30_"
        if file_name_with_extension.startswith(ip_to_remove):
            file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
        else:
            file_name_without_ip = file_name_with_extension

        # 확장자 제거
        image_file_name = os.path.splitext(file_name_without_ip)[0]
        sanitized_title = re.sub(r'[\\/*?:"<>|]', '_', title)

        # 최종 CSV 저장 경로
        save_path = os.path.join(base_save_path, f"{overall_result}_{image_file_name}_{sanitized_title}.csv")

        # 4) CSV 저장
        df.to_csv(save_path, index=False, encoding='utf-8-sig')

        dest_image_path = os.path.join(base_save_path, file_name_without_ip)
        shutil.copy(img_path, dest_image_path)

    def count_csv_and_failures(self, folder_path, start_time, end_time):
        end_file = '.csv'
        csv_files = [f for f in os.listdir(folder_path) if f.endswith(end_file)]

        total_csv_files = 0
        fail_count = 0

        for file_name in csv_files:
            try:
                parts = file_name.split('_')
                # 날짜와 시간 부분 추출
                date_part = parts[1]  # '2025-01-22'
                time_part = "_".join(parts[2:5])  # '17_08_41'
                file_time_str = f"{date_part}_{time_part}"  # '2025-01-22_17_08_41'
                file_time = datetime.strptime(file_time_str, "%Y-%m-%d_%H_%M_%S")

                # start_time과 end_time의 타임존 정보 제거
                start_time_naive = start_time.replace(tzinfo=None)
                end_time_naive = end_time.replace(tzinfo=None)

                # 시간 범위 체크
                if start_time_naive <= file_time <= end_time_naive:
                    total_csv_files += 1
                    if 'FAIL' in file_name.upper():
                        fail_count += 1

            except (IndexError, ValueError):
                print(f"[DEBUG] 파일 이름 분리 결과: {file_name.split('_')}")
                print(f"[WARN] 파일 이름에서 시간을 추출할 수 없습니다: {file_name}")

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