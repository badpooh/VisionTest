import re
import numpy as np
import cv2
from datetime import datetime, timezone
import shutil
import os
import glob
import pandas as pd
import math
from collections import Counter
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import time

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
    def eval_test_mode_balance(self, ocr_res, correct_answers, modbus_meas_value, meas_rules, ratio_lower=None, ratio_upper=None, reset_time=None, modbus_timestamp_value=None, image_path=None):
        self.demo_test_result = False
        self.measurement_error = False
        self.condition_met = False
        
        image = cv2.imread(image_path)

        def validate_ratio(percent_list, lower_limit, upper_limit):
            results_list = []
            percent_error = False

            for item in percent_list:
                match = re.match(r"([-+]?\d+\.?\d*)\s*(.*)", item)

                if match and match.group(1):
                    numeric_value = float(match.group(1))
                    unit = match.group(2).strip()

                    if unit == '%' and lower_limit < numeric_value < upper_limit:
                        print(f"'{item}' -> PASS")
                        result = f"{item} -> PASS"
                        results_list.append(result)
                    
                    else:
                        print(f"'{item}' -> (FAIL / 단위 또는 범위 오류)")
                        percent_error = True
                        result = f"{item} -> FAIL"
                        results_list.append(result)
                else:
                    print(f"'{item}' -> (INFO - Skipping non-numeric text)")
            
            return percent_error, results_list
        
        def validate_timestamp(timestamp_list, reset_time):
            timestamp_error = False
            results_list = []
            numeric_list = []
            reset_timestamp = reset_time.timestamp()
            print(reset_time)

            for item in timestamp_list:
                naive_dt_object = datetime.strptime(item, '%Y-%m-%d %H:%M:%S')
                utc_dt_object = naive_dt_object.replace(tzinfo=timezone.utc)
                unix_timestamp = utc_dt_object.timestamp()

                if reset_timestamp - 30 < unix_timestamp < reset_timestamp + 30:
                    print(f"'{item}' -> PASS")
                    result = f"{item} -> PASS"
                    results_list.append(result)
                    numeric_list.append(unix_timestamp)
                else:
                    print(f"'{item}' -> (FAIL - 단위 또는 범위 오류)")
                    timestamp_error = True
                    result = f"{item} -> FAIL"
                    results_list.append(result)
                    numeric_list.append(unix_timestamp)
            
            return timestamp_error, results_list, numeric_list
        
        def validate_measurement(measurement_list, rules_list):
            results_list = []
            numeric_list = []

            if len(measurement_list) != len(rules_list):
                print(f"FAIL - Mismatch between number of measurements and rules.")
                return True, ["Length mismatch"], []

            for item, rules in zip(measurement_list, rules_list):
                match = re.match(r"([-+]?\d+\.?\d*)\s*(.*)", item)
                if match and match.group(1):
                    numeric_value = float(match.group(1))
                    unit = match.group(2).strip()

                    # 해당 항목에 맞는 개별 규칙을 가져옵니다.
                    lower_limit = rules['low']
                    upper_limit = rules['high']
                    right_unit = rules['unit']

                    if lower_limit < numeric_value < upper_limit and unit == right_unit:
                        result = f"'{item}' -> PASS"
                        results_list.append(result)
                        numeric_list.append(numeric_value)
                    else:
                        result = f"'{item}' -> (FAIL)"
                        results_list.append(result)
                        self.measurement_error = True
                        numeric_list.append(numeric_value)
            
            return self.measurement_error, results_list, numeric_list
        
        def validate_modbus(modbus_value, right_value, tolerance=0.5):
            formatted_value = []
            modbus_error = False

            for item in modbus_value:
                value = abs(item)
                if value >= 1000:
                    value = value / 1000

                if round(value, 1) >= 100:
                    for_value = f'{value:.1f}'
                    formatted_value.append(for_value)
                elif round(value, 2) >= 10:
                    for_value = f'{value:.2f}'
                    formatted_value.append(for_value)
                elif round(value, 3) >= 1:
                    for_value = f'{value:.3f}'
                    formatted_value.append(for_value)
                else:
                    for_value = f'{value:.3f}'
                    formatted_value.append(for_value)

            for modbus_val, ocr_val in zip(formatted_value, right_value):
        
                if modbus_val is None or ocr_val is None:
                    result_str = f"Modbus: {modbus_val}, OCR: {ocr_val} -> FAIL (Invalid value)"
                    print("len(mobus_val) != len(ocr_val)")
                    continue
                
                modbus_val = float(modbus_val)
                ocr_val = float(ocr_val)

                difference = abs(modbus_val) - abs(ocr_val)
                abs_difference = abs(difference)
                if abs_difference <= tolerance:
                    result_str = f"Modbus: {modbus_val:.3f}, OCR: {ocr_val:.3f} -> PASS (Diff: {abs_difference:.3f})"
                    print(f"{result_str}")
                else:
                    result_str = f"Modbus: {modbus_val:.3f}, OCR: {ocr_val:.3f} -> FAIL (Diff: {abs_difference:.3f})"
                    print(f"{result_str}")
                    modbus_error = True

            return modbus_error, formatted_value
 
        ### 고정 문자 가공 ###
        ocr_fixed_text = [result.strip() for result in ocr_res[:2]]
        ####################

        ### 변동 문자 가공 ###
        if len(ocr_res) > 3:
            ocr_ratio_text_tuple = re.findall(r'(\d+\.\d+\s*%)|([A-Z]+\s*%)', ocr_res[2])
            ocr_ratio_text = [item1 + item2 for item1, item2 in ocr_ratio_text_tuple]
            ocr_timestamp_text = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', ocr_res[2])
            ocr_measurement_text = re.findall(r'\d+\.\d+\s+[A-Za-z%]+', ocr_res[3])
        else:
            ocr_ratio_text = []
            ocr_timestamp_text = []
            ocr_measurement_text = re.findall(r'\d+\.\d+\s+[A-Za-z%]+', ocr_res[2])
        ####################

        # if len(ocr_res) > 3:
        #     ratio_matches = re.findall(r'(\d+\.\d+\s*%)|([A-Z]+\s*%)', ocr_res[2] or "")
        #     ocr_ratio_text = [ (a or "") + (b or "") for a, b in ratio_matches ]  # 빈 결과면 []
        #     ocr_timestamp_text = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', ocr_res[2] or "")
        #     ocr_measurement_text = re.findall(r'\d+\.\d+\s+[A-Za-z%]+', ocr_res[3] or "")
        # else:
        #     ocr_ratio_text = []
        #     ocr_timestamp_text = []
        #     ocr_measurement_text = re.findall(r'\d+\.\d+\s+[A-Za-z%]+', (ocr_res[2] if len(ocr_res) > 2 else "") or "")

        ### 고정 문자 중 잘못된 문자 검증 ###
        ocr_fixed_text_counter = Counter(ocr_fixed_text)
        correct_answers_counter = Counter(correct_answers)

        ocr_error = list((ocr_fixed_text_counter - correct_answers_counter).elements())
        ocr_missing_item = list((correct_answers_counter - ocr_fixed_text_counter).elements())
        ####################
        
        all_meas_results = []
        all_modbus_results = []
        ratio_results = []
        timestamp_results = []
        meas_results = [] 
        meas_modbus_results = [] 

        ### 검사 test_step 개념: 
        ### RELAY:1, METER:2, 
        ### VOLTAGE:01, CURRENT:02, POWER:03, 
        ### RMS:001, FUND:002, 
        ### LL:0001 LN:0002,
        ### Min:00001 Max:00002
        if ocr_ratio_text and ocr_timestamp_text:
            ratio_error, ratio_results = validate_ratio(ocr_ratio_text, ratio_lower, ratio_upper)
            all_meas_results.append(ratio_error)
            timestamp_error, timestamp_results, timestamp_numeric_list = validate_timestamp(ocr_timestamp_text, reset_time)
            all_meas_results.append(timestamp_error)
            meas_error, meas_results, meas_numeric_list = validate_measurement(ocr_measurement_text, meas_rules)
            all_meas_results.append(meas_error)
            print(modbus_meas_value)
            meas_modbus_error, meas_modbus_results = validate_modbus(modbus_meas_value, meas_numeric_list)
            all_modbus_results.append(meas_modbus_error)

        elif not ocr_ratio_text and ocr_timestamp_text:
            timestamp_error, timestamp_results, timestamp_numeric_list = validate_timestamp(ocr_timestamp_text, reset_time)
            all_meas_results.append(timestamp_error)
            meas_error, meas_results, meas_numeric_list = validate_measurement(ocr_measurement_text, meas_rules)
            all_meas_results.append(meas_error)
            print(modbus_meas_value)
            meas_modbus_error, meas_modbus_results = validate_modbus(modbus_meas_value, meas_numeric_list)
            all_modbus_results.append(meas_modbus_error)
        
        elif not ocr_ratio_text and not ocr_timestamp_text:
            meas_error, meas_results, meas_numeric_list = validate_measurement(ocr_measurement_text, meas_rules)
            all_meas_results.append(meas_error)
            print(modbus_meas_value)
            meas_modbus_error, meas_modbus_results = validate_modbus(modbus_meas_value, meas_numeric_list)
            all_modbus_results.append(meas_modbus_error)
        
        
        
        elif not self.condition_met:
            print("Nothing matching word")

        for item in all_meas_results:
            if item == True:
                self.demo_test_result = True
        
        for item in all_modbus_results:
            if item == True:
                self.demo_test_result = True

        print(f"OCR - 정답: {ocr_error}")
        print(f"정답 - OCR: {ocr_missing_item}")

        return self.demo_test_result, ocr_error, ocr_missing_item, ocr_fixed_text, ratio_results, timestamp_results, meas_results, meas_modbus_results
    
    def test_mode_save_csv(self, base_save_path, img_path, ocr_fixed_text, ocr_error, right_error, meas_modbus_results, reset_time, test_result=False, ocr_meas_ratio=None, ocr_meas_timestamp=None, ocr_measurement=None,):
        """
        img_path: 이미지경로 + 이미지파일 제목 -> csv 파일 제목이 됨
        base_save_path: CSV/이미지 저장할 폴더
        img_path:   원본 이미지 파일 경로
        ocr_fixed_text: str, 고정 문자
        
        """

        if test_result or ocr_error or right_error:
            overall_result = "FAIL"
        else:
            overall_result = "PASS"
            
        results_dict = {
                        # "Overall Result": overall_result,
                        "Data View Fixed text": str(ocr_fixed_text),
                        "OCR Errors (Extra)": f"{ocr_error} ({'FAIL' if ocr_error else 'PASS'})",
                        "OCR Errors (Missing)": f"{right_error} ({'FAIL' if right_error else 'PASS'})",
                        "Meas Ratio Results": str(ocr_meas_ratio),
                        "Timestamp Results": f"{str(ocr_meas_timestamp)} / Timestamp Standard: {str(reset_time)}",
                        "Measurement Results": str(ocr_measurement),
                        "Modbus Measurement": str(meas_modbus_results)
                        # "Image Match": img_result,
                        # "Invalid Elements (H.Text)": str(invalid_elements)
                        }

        df = pd.DataFrame(list(results_dict.items()), columns=['Parameter', 'Value'])

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