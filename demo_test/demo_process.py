import numpy as np
import os
import glob
from datetime import datetime

from function.func_connection import ConnectionManager
from function.func_evaluation import Evaluation
from function.func_ocr import PaddleOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels

from config.config_roi import ConfigROI as ecroi
from config.config_ref import ConfigTextRef as cftr
from config.config_ref import ConfigImgRef as cfir
from config.config_touch import ConfigTouch as ConfigTouch

from demo_test.demo_interface import Interface

image_directory = r"\\10.10.20.30\screenshot"
ocr_func = PaddleOCRManager()

class DemoProcess:

    touch_manager = TouchManager()
    connect_manager = ConnectionManager()
    evaluation = Evaluation()
    now = datetime.now()
    file_time_diff = {}
    
    def __init__(self, score_callback=None, stop_callback=None):
        self.test_mode = None
        self.score_callback = score_callback
        self.stop_callback = stop_callback 

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

    def ocr_process(self, image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys=None, reset_time=None, base_save_path=None, test_mode=None):
        """
        Args:
            image_path (str): The path to the image file.
            roi_keys (list): List of ROI keys for general OCR processing.
            roi_keys_meas (list): List of ROI keys for measurement OCR processing.
            ocr_ref (str): The OCR type to be selected for evaluation.
            time_keys (list): Min, Max time
            reset_time (time): Min, Max reset time
            img_result (str): image match curculation result
        Returns:
            None
        """
        self.test_mode = test_mode
        ocr_res = None
        setup = 0
        ocr_img = ocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)
        ocr_img_meas = ocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys_meas, test_type=setup)
        if self.test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
            if time_keys:
                time_results = self.evaluation.check_time_diff(image=image_path, roi_keys=time_keys, reset_time=reset_time, test_mode=test_mode)
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, time_results=time_results, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
            else:
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)

        elif self.test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path)
            if time_keys is not None:
                time_results = self.evaluation.check_time_diff(image=image_path, roi_keys=time_keys, reset_time=reset_time, test_mode=test_mode)
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, time_results=time_results, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
            else:
                self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, img_path=image_path, base_save_path=base_save_path, all_meas_results=all_meas_results)
        
        else:
            print("self.test_mode type error")

        return ocr_res

    def ocr_4phase(self, ref, base_save_path, test_mode, search_pattern):  # A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)

    def ocr_curr_4phase(self, ref, base_save_path, test_mode, search_pattern):  # A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.curr_per_aver, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)

    def ocr_4phase_time(self, ref, reset_time, base_save_path, test_mode, search_pattern):  # A,B,C,Aver + time stamp ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp,
                     ecroi.c_time_stamp, ecroi.aver_time_stamp]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys,
                         roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)

    def ocr_curr_4phase_time(self, ref, reset_time, base_save_path, test_mode, search_pattern):  # A,B,C,Aver ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca, ecroi.aver]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.curr_per_aver, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas, ecroi.aver_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp,
                     ecroi.c_time_stamp, ecroi.aver_time_stamp]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys,
                         roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)

    def ocr_3phase(self, ref, base_save_path, test_mode, search_pattern):  # A,B,C ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)

    def ocr_3phase_time(self, ref, reset_time, base_save_path, test_mode, search_pattern):  # A,B,C + time stamp ###
        """
        Args:
            ref (str): The OCR type to be selected for evaluation.
        Returns:
            None
        """
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = ref
        self.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)

    def ocr_phaosr_process(self, img_ref, ref, img_cut1, img_cut2, img_cut3, base_save_path, test_mode, search_pattern):
        self.touch_manager.screenshot()
        image_path = self.load_image_file(search_pattern)
        roi_keys = [ecroi.phasor_title, ecroi.phasor_title_2, ecroi.phasor_vl_vn, ecroi.phasor_voltage, ecroi.phasor_a_c_vol, ecroi.phasor_current, ecroi.phasor_a_c_cur]
        roi_keys_meas = [ecroi.phasor_a_meas, ecroi.phasor_b_meas, ecroi.phasor_c_meas, ecroi.phasor_a_meas_cur, ecroi.phasor_b_meas_cur, ecroi.phasor_c_meas_cur,
                        ecroi.phasor_a_angle, ecroi.phasor_b_angle, ecroi.phasor_c_angle, ecroi.phasor_a_angle_cur, ecroi.phasor_b_angle_cur, ecroi.phasor_c_angle_cur]
        ocr_ref = ref
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = []
        image_results.append(self.evaluation.img_match(image_path, img_cut1, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut2, img_ref))
        image_results.append(self.evaluation.img_match(image_path, img_cut3, img_ref))

        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, all_meas_results=all_meas_results, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        elif test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path, image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, ocr_img_meas, all_meas_results=all_meas_results, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        else :
            print("ocr phasor process error")

    def ocr_graph_detection(self, roi_keys, ocr_ref, roi_keys_meas, value, base_save_path, test_mode, search_pattern):
        self.touch_manager.screenshot()
        image_path = self.load_image_file(search_pattern)
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results, csv_result = self.evaluation.img_detection(image_path, value, 2)

        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=csv_result, base_save_path=base_save_path)
        if test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=csv_result, base_save_path=base_save_path)
        else :
            print("ocr phasor process error")

    def ocr_waveform_detection(self, roi_keys, ocr_ref, value, base_save_path, test_mode, search_pattern):
        self.touch_manager.screenshot()
        image_path = self.load_image_file(search_pattern)
        roi_keys = roi_keys
        ocr_ref = ocr_ref
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = None
        image_results = self.evaluation.img_detection(image_path, value, 2)

        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        else :
            print("ocr phasor process error")

class DemoTest:

    touch_manager = TouchManager()
    modbus_manager = ConnectionManager()
    modbus_label = ModbusLabels()
    sp = DemoProcess()
    interface = Interface()
    now = datetime.now()
    file_time_diff = {}

    def __init__(self, score_callback=None, stop_callback=None):
        self.evaluation = Evaluation()
        self.score_callback = score_callback
        self.stop_callback = stop_callback

    def demo_test_mode(self):
        self.test_mode = self.modbus_label.demo_test_setting()
        # print(f"test_mode={self.test_mode}")
        return self.test_mode
    
    def noload_test_mode(self):
        self.test_mode = self.modbus_label.noload_test_setting()
        print(f"test_mode={self.test_mode}")
        return self.test_mode
        
    def mea_demo_mode(self):
        ### Timeout을 infinite로 변경 후 Test Mode > Balance로 실행 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_setup()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_3.value)
        self.touch_manager.touch_menu("data_view_2")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["999"]
        cutted_image = ocr_func.ocr_basic(
            image=image_path, roi_keys=roi_keys)
        if "Password" in cutted_image:
            for _ in range(4):
                self.touch_manager.touch_menu("btn_num_pw_0")
            self.touch_manager.touch_menu("btn_num_pw_enter")
            self.touch_manager.touch_menu("infinite")
            self.touch_manager.touch_menu("btn_popup_enter")
            self.touch_manager.touch_menu("btn_apply")
        else:
            print("error")
            self.touch_manager.touch_menu("btn_popup_cencel")
        self.touch_manager.touch_menu("data_view_1")
        self.touch_manager.touch_menu("btn_testmode_2")
        self.touch_manager.touch_menu("btn_popup_enter")
        self.touch_manager.touch_menu("btn_apply")
        print("Demo Mode Start")

    def reset_max_min(self):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_setup()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
        self.touch_manager.touch_menu("data_view_3")
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = ["999"]
        cutted_image = ocr_func.ocr_basic(
            image=image_path, roi_keys=roi_keys)
        if "Password" in cutted_image:
            for _ in range(4):
                self.touch_manager.touch_menu("btn_num_pw_0")
            self.touch_manager.touch_menu("btn_num_pw_enter")
            self.touch_manager.touch_menu("cauiton_confirm")
            self.touch_manager.touch_menu("btn_apply")
        else:
            print("error")
            self.touch_manager.touch_menu("btn_popup_cencel")
        self.reset_time = datetime.now()
        print(self.reset_time)
        return self.reset_time
    
    def demo_mea_vol_all(self, base_save_path, test_mode, search_pattern):
        self.demo_mea_vol_rms(base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.demo_mea_vol_fund(base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.demo_mea_vol_thd(base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.demo_mea_vol_freq(base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.demo_mea_vol_residual(base_save_path, test_mode, search_pattern)

    def demo_mea_vol_rms(self, base_save_path, test_mode, search_pattern):
        ### 아래 추가적인 설명이 있는 코드 ###
        # start_time = self.modbus_label.device_current_time()
    
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(ecroi.title_view.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-L min 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.rms_vol_ll.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-L max 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.rms_vol_ll.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N 만 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(cftr.rms_vol_ln.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N min 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.rms_vol_ln.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N max 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.rms_vol_ln.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### 총 계산 전에 각각의 메서드에서 할 예정이였던 기존코드 ###
        # end_time = self.modbus_label.device_current_time()
        # folder_path = base_save_path
        # total_csv_files, fail_count = self.evaluation.count_csv_and_failures(folder_path, start_time, end_time)

        # # 콜백으로 점수 전달
        # if self.score_callback:
        #     score = f"{fail_count}/{total_csv_files}"
        #     self.score_callback(score)
        # else:
        #     print("Score callback is not set")

    def demo_mea_vol_fund(self, base_save_path, test_mode, search_pattern):
        start_time = self.modbus_label.device_current_time()
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(cftr.fund_vol_ll.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-L min 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.fund_vol_ll.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-L max 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.fund_vol_ll.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N 만 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase(cftr.fund_vol_ln.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N min 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.fund_vol_ln.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N max 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_4phase_time(cftr.fund_vol_ln.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        print("Voltage_Fund_Done")

    def demo_mea_vol_thd(self, base_save_path, test_mode, search_pattern):
        ### L-L 만 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_3.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_thd_ll.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.thd_vol_ll.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-L max 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.thd_vol_ll.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N 만 검사 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_thd_ln.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.thd_vol_ln.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### L-N max 검사 ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.thd_vol_ln.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_vol_freq(self, base_save_path, test_mode, search_pattern):

        ### 기본주파수 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = cftr.freq.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### 주파수 Min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = cftr.freq.value
        time_keys = [ecroi.a_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### 주파수 Max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab]
        roi_keys_meas = [ecroi.a_meas]
        ocr_ref = cftr.freq.value
        time_keys = [ecroi.a_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_vol_residual(self, base_save_path, test_mode, search_pattern):

        ### 기본 검사 ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_1.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_vol.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### 잔류전압 Min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_vol.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### 잔류전압 Max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_vol.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_all(self, base_save_path, test_mode, search_pattern):
        self.demo_mea_curr_rms(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_fund(base_save_path, test_mode, search_pattern)
        # self.demo_mea_curr_demand(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_thd(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_tdd(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_cf(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_kf(base_save_path, test_mode, search_pattern)
        self.demo_mea_curr_residual(base_save_path, test_mode, search_pattern)

    def demo_mea_curr_rms(self, base_save_path, test_mode, search_pattern):
        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.rms_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current Min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.rms_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current Max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.rms_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_fund(self, base_save_path, test_mode, search_pattern):
        ### Current ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.fund_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current Min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.fund_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current Max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.fund_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_thd(self, base_save_path, test_mode, search_pattern):
        ### Current thd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.thd_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current thd Max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.thd_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_tdd(self, base_save_path, test_mode, search_pattern):
        ### Current tdd ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.tdd_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current tdd Max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.tdd_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_cf(self, base_save_path, test_mode, search_pattern):
        ### Current crest factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_6.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.cf_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current crest factor Max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.cf_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_kf(self, base_save_path, test_mode, search_pattern):
        ### Current k-factor ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_7.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase(cftr.kf_curr.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current k-factor Max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_3phase_time(cftr.kf_curr.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_curr_residual(self, base_save_path, test_mode, search_pattern):
        ### Current residual ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_8.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current residual Min###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_curr.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### Current residual Max###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.residual_curr.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys,
                            roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_pow_all(self, base_save_path, test_mode, search_pattern):
        self.demo_mea_pow_active(base_save_path, test_mode, search_pattern)
        self.demo_mea_pow_reactive(base_save_path, test_mode, search_pattern)
        self.demo_mea_pow_apparent(base_save_path, test_mode, search_pattern)
        self.demo_mea_pow_pf(base_save_path, test_mode, search_pattern)

    def demo_mea_pow_active(self, base_save_path, test_mode, search_pattern):
        ### active power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_3.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.active.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.active.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.active.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_pow_reactive(self, base_save_path, test_mode, search_pattern):
        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_3.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.reactive.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.reactive.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.reactive.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
    
    def demo_mea_pow_apparent(self, base_save_path, test_mode, search_pattern):
        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_3.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_3.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.apparent.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.apparent.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.apparent.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_pow_pf(self, base_save_path, test_mode, search_pattern):
        ### reactive power ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_3.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.pf.value, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power min ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_min.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.pf.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### power max ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.pf.value, reset_time, base_save_path, test_mode, search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
    
    def demo_mea_anal_all(self, base_save_path, test_mode, search_pattern):
        self.demo_mea_anal_phasor(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_harmonics(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_waveform(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_voltsym(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_voltunbal(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_cursym(base_save_path, test_mode, search_pattern)
        self.demo_mea_anal_currunbal(base_save_path, test_mode, search_pattern)
    
    def demo_mea_anal_phasor(self, base_save_path, test_mode, search_pattern):
        ocr_func.update_phasor_condition(1)
        ### voltage+current vll ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_1.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_all_vll.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_all_vll_none.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ## voltage+current vln ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vln.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_all_vln.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_all_vln_none.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### voltage vll ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vll.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_vol_vll.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_vol_vll_none.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### voltage vln ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vln.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_vol_vln.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_vol_vln_none.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### current vll ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_vol.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vll.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_curr_vll.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_curr_vll_none.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### current vln ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vln.value)
        if test_mode == "Demo":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_curr_vln.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        elif test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_curr_vln_none.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### nothing vll ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vll.value)
        if test_mode == "Demo" or test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_na_vll.value, ref=cftr.phasor_ll.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### nothing vln ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_phasor_vln.value)
        if test_mode == "Demo" or test_mode == "NoLoad":
            self.sp.ocr_phaosr_process(img_ref=cfir.img_ref_phasor_na_vln.value, ref=cftr.phasor_ln.value, img_cut1=ecroi.phasor_img_cut, img_cut2=ecroi.phasor_a_c_angle_vol, img_cut3=ecroi.phasor_a_c_angle_cur, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        ocr_func.update_phasor_condition(0)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_anal_harmonics(self, base_save_path, test_mode, search_pattern):
        self.test_mode = test_mode
        ocr_func.update_phasor_condition(1)
        roi_keys = [ecroi.harmonics_title, ecroi.harmonics_sub_title_1, ecroi.harmonics_sub_title_2, ecroi.harmonics_sub_title_3,
                    ecroi.harmonics_graph_a, ecroi.harmonics_graph_b, ecroi.harmonics_graph_c]
        roi_keys_meas = [ecroi.harmonics_thd_a, ecroi.harmonics_thd_b, ecroi.harmonics_thd_c,
                         ecroi.harmonics_fund_a, ecroi.harmonics_fund_b, ecroi.harmonics_fund_c]
        ### voltage ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        ocr_ref = cftr.harmonics_vol_3p4w.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        if test_mode == "Demo":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, cfir.img_ref_harmonics_vol_3p4w.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        elif test_mode == "NoLoad":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, cfir.img_ref_harmonics_vol_3p4w_none.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
            self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### current ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        ocr_ref = cftr.harmonics_curr.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        if test_mode == "Demo":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, cfir.img_ref_harmonics_curr.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_graph_img_cut, cfir.img_ref_harmonics_curr_none.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### vol_a-phase X / 색이 없어야되는 걸 찾는 것으로 Demo와 None 둘다 동일###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_vol.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.harmonics_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### vol_b-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### vol_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### curr_a-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### curr_b-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### curr_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### fund(v체크박스) 버튼 후 vol_a ~ curr_c 반복 ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_vol.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_fund.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_curr_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_fund.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### [v], fund, rms 그래프 변화 확인 ###
        ### voltage [%]fund ###
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_v.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_fund.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        ocr_ref = cftr.harmonics_per_fund.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        if test_mode == "Demo":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, cfir.img_ref_harmonics_vol_fund.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, cfir.img_ref_harmonics_vol_fund_none.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### [%]Fund 일때 vol_a-phase X / 색이 없어야되는 걸 찾는 것으로 Demo와 None 둘다 동일###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### voltage [%]RMS ###
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_v.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_rms.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        ocr_ref = cftr.harmonics_per_rms.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, cfir.img_ref_harmonics_vol_rms_none.value)
        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### [%]RMS 일때 vol_a-phase X / 색이 없어야되는 걸 찾는 것으로 Demo와 None 둘다 동일###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        

        ### current [%]Fund ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_analysis_curr.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_v.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_fund.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        ocr_ref = cftr.harmonics_per_fund.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, cfir.img_ref_harmonics_curr_fund_none.value)
        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### [%]Fund 일때 vol_a-phase X / 색이 없어야되는 걸 찾는 것으로 Demo와 None 둘다 동일###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### current [%]RMS ###
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_v.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_rms.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        ocr_ref = cftr.harmonics_per_rms.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        image_results = self.evaluation.img_match(image_path, ecroi.harmonics_chart_img_cut, cfir.img_ref_harmonics_curr_rms_none.value)
        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
        ### [%]RMS 일때 vol_a-phase X / 색이 없어야되는 걸 찾는 것으로 Demo와 None 둘다 동일###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_graph_detection([ecroi.waveform_title], cftr.harmonics_for_img.value, roi_keys_meas, value=ecroi.color_harmonics_vol_a.value, base_save_path=base_save_path, test_mode=test_mode)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        ocr_func.update_phasor_condition(0)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_meter_harmonics_text(self, base_save_path, test_mode, search_pattern):
        ### voltage ### -> 추후 구현
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_dropdown_harmonics_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_harmonics_sub_text.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        image_path = r"C:\Users\jscho\Desktop\123.png"
        roi_key = [ecroi.harmonics_title, ecroi.harmonics_text_sub_title, ecroi.harmonics_text_sub_abc, ecroi.harmonics_text_number_title_1]
        roi_keys = [ecroi.harmonics_text_number_title_1]
        roi_keys_meas = [ecroi.harmonics_text_number_meas_1]
        ocr_ref = cftr.harmonics_text.value, ecroi.harmonics_text_number_title_1.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_key)
        ocr_img_meas = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys_meas)
        if test_mode == "Demo":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path)
            validate_ocr_results = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
            invalid_elements = self.evaluation.validate_ocr(validate_ocr_results)
            self.evaluation.save_csv(ocr_img=ocr_img, ocr_error=ocr_error, right_error=right_error, meas_error=meas_error, img_path=image_path,base_save_path=base_save_path, invalid_elements=invalid_elements)
        elif test_mode == "NoLoad":
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, ocr_img_meas, image_path=image_path)
            self.evaluation.save_csv(ocr_img=ocr_img, ocr_error=ocr_error, right_error=right_error, meas_error=meas_error, ocr_img_meas=ocr_img_meas, img_path=image_path,base_save_path=base_save_path)
        
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_anal_waveform(self, base_save_path, test_mode, search_pattern):
        ocr_func.update_phasor_condition(1)
        ### waveform basic ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_3.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.waveform_title]
        ocr_ref = cftr.waveform_3p4w.value
        ocr_img = ocr_func.ocr_basic(image=image_path, roi_keys=roi_keys)
        if test_mode == "Demo":
            image_results = self.evaluation.img_match(image_path, ecroi.waveform_all_img_cut, cfir.img_ref_waveform_all.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_demo_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        elif test_mode == "NoLoad":
            image_results = self.evaluation.img_match(image_path, ecroi.waveform_all_img_cut, cfir.img_ref_waveform_all_none.value)
            ocr_error, right_error, meas_error, ocr_res, all_meas_results = self.evaluation.eval_none_test(ocr_img, ocr_ref, image_path=image_path, img_result=image_results)
        self.evaluation.save_csv(ocr_img, ocr_error, right_error, meas_error, img_path=image_path, img_result=image_results, base_save_path=base_save_path)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_c.value)
        self.sp.ocr_waveform_detection(roi_keys=[ecroi.waveform_title], ocr_ref=cftr.waveform_3p4w.value, value=ecroi.color_waveform_curr_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_b_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_b.value)
        self.sp.ocr_waveform_detection([ecroi.waveform_title], cftr.waveform_3p4w.value, ecroi.color_waveform_curr_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_a_b_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_waveform_curr_a.value)
        self.sp.ocr_waveform_detection([ecroi.waveform_title], cftr.waveform_3p4w.value, ecroi.color_waveform_curr_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_all_vol_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_wave_vol_c.value)
        self.sp.ocr_waveform_detection([ecroi.waveform_title], cftr.waveform_3p4w.value, ecroi.color_waveform_vol_c.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_all_vol_b_c-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_wave_vol_b.value)
        self.sp.ocr_waveform_detection([ecroi.waveform_title], cftr.waveform_3p4w.value, ecroi.color_waveform_vol_b.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### waveform curr_all_vol_all-phase X ###
        self.touch_manager.touch_menu(ConfigTouch.touch_wave_vol_a.value)
        self.sp.ocr_waveform_detection([ecroi.waveform_title], cftr.waveform_3p4w.value, ecroi.color_waveform_vol_a.value, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        ocr_func.update_phasor_condition(0)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_anal_voltsym(self, base_save_path, test_mode, search_pattern):
        ### LL ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_4.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.symm_vol_ll.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### LL Max###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.a_meas, ecroi.b_meas]
        ocr_ref = cftr.symm_vol_ll.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### LN ###
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_thd_ln.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = cftr.symm_vol_ln.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### LN Max###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c, ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = cftr.symm_vol_ln.value
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp]
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_anal_voltunbal(self, base_save_path, test_mode, search_pattern):
        ### vol unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_5.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase(cftr.unbal_vol.value, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### vol unbalance max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        self.sp.ocr_curr_4phase_time(cftr.unbal_vol.value, reset_time, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_anal_cursym(self, base_save_path, test_mode, search_pattern):
        ### symm ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_6.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = cftr.symm_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### symm max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file(search_pattern)
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = cftr.symm_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode=test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

    def demo_mea_anal_currunbal(self, base_save_path, test_mode, search_pattern):
        ### current unbalance ###
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_4.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_7.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        ocr_ref = cftr.unbal_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, base_save_path=base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return

        ### symm max ###
        reset_time = self.modbus_label.reset_max_min()
        self.touch_manager.touch_menu(ConfigTouch.touch_toggle_max.value)
        self.touch_manager.screenshot()
        image_path = self.sp.load_image_file()
        roi_keys = [ecroi.title_view, ecroi.a_ab, ecroi.b_bc, ecroi.c_ca]
        roi_keys_meas = [ecroi.curr_per_a, ecroi.curr_per_b, ecroi.curr_per_c,
                         ecroi.a_meas, ecroi.b_meas, ecroi.c_meas]
        time_keys = [ecroi.a_time_stamp, ecroi.b_time_stamp, ecroi.c_time_stamp]
        ocr_ref = cftr.unbal_curr.value
        self.sp.ocr_process(image_path, roi_keys, roi_keys_meas, ocr_ref, time_keys, reset_time, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_mea_curr_demand(self, base_save_path, test_mode, search_pattern):
        self.touch_manager.btn_front_meter()
        self.touch_manager.btn_front_home()
        self.touch_manager.touch_menu(ConfigTouch.touch_main_menu_2.value)
        self.touch_manager.touch_menu(ConfigTouch.touch_side_menu_3.value)
        self.modbus_label.reset_demand()
        self.modbus_label.reset_demand_peak()
        self.modbus_label.demo_test_demand()
        self.interface.show_interface(130)
        reset_time = self.modbus_label.reset_max_min()
        self.sp.ocr_curr_4phase_time(cftr.demand_current.value, reset_time, base_save_path, test_mode=test_mode, search_pattern=search_pattern)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return
        
    def demo_test_demand(self, base_save_path, test_mode):
        self.demo_mea_curr_demand(base_save_path, test_mode)
        if self.stop_callback and self.stop_callback():
            print("test_stop")
            return