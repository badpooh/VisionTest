import time
from function.func_ocr import PaddleOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation
from function.func_autogui import AutoGUI
from PySide6.QtCore import Qt, QObject

from config.config_touch import ConfigTouch
from config.config_demo_roi import ConfigROI
from config.config_map import ConfigMap
from config.config_map import ConfigInitialValue as civ
from config.config_ref import ConfigImgRef
from config.config_test_mode_value import TestModeBalance as tmb



image_directory = r"\\10.10.20.30\screenshot"
paddleocr_func = PaddleOCRManager()

class DemoTest(QObject):
	 
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()
	autogui_manager = AutoGUI()

	def __init__(self):
		super().__init__()
		self.accruasm_state = 2 # 초기 상태 설정

	def on_accurasm_checked(self, state):
		self.accruasm_state = state
		# print(f"SetupProcess: AccuraSM checked={state}")

	def test_mode_ocr_process(self, 
					   	base_save_path, 
						search_pattern,  
						roi_keys, 
						correct_answers, 
						addr_meas,
						aggre_selection,
						meas_lower,
						meas_upper,
						meas_unit,
						ratio_lower=None,
						ratio_upper=None,
						addr_timestamp=None,
						reset_time=None,
						modbus_unit=None,):
		"""
		Args:
			base_save_path (str): 결과 저장 디렉토리
			search_pattern (str): 스크린샷 파일 검색 패턴
			roi_keys (list): ROI 키 (길이 2 이상 가정)
			except_address (Enum): 검사에서 제외할 단일 주소 (ex: ecm.addr_wiring)
			access_address (tuple): 측정 접근 주소 (ex: (6000,1))
			template_path: AccuraSM 정답 png 파일
			roi_mask: 
			modbus_ref: 
			ref_select: default=0, List=1
			coordinates (list): 미정
		Returns:
			None
		"""
		time.sleep(0.6)
		self.touch_manager.screenshot()
		image_path = self.eval_manager.load_image_file(search_pattern)
		ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys)
		modbus_meas_result = self.modbus_label.read_float(address=addr_meas, aggre_selection=aggre_selection)
		if addr_timestamp:
			modbus_timestamp_result = self.modbus_label.read_float(address=addr_timestamp, aggre_selection=255)

		
		demo_test_result, ocr_error, ocr_missing_item, ocr_fixed_text, ocr_ratio_text, ocr_timestamp_text, ocr_measurement_text, modbus_results = self.eval_manager.eval_test_mode_balance(
			ocr_res=ocr_results, 
			correct_answers=correct_answers, 
			ratio_lower=ratio_lower,
			ratio_upper=ratio_upper,
			meas_lower=meas_lower,
			meas_upper=meas_upper,
			meas_unit=meas_unit,
			modbus_meas_value=modbus_meas_result,
			modbus_timestamp_value=None,
			reset_time=reset_time, 
			image_path=image_path,
			)
		self.eval_manager.test_mode_save_csv(
		base_save_path=base_save_path,
		img_path=image_path,
		ocr_fixed_text=ocr_fixed_text,
		ocr_error=ocr_error,
		right_error=ocr_missing_item,
		test_result=demo_test_result,
		ocr_measurement=ocr_measurement_text,
		ocr_meas_ratio=ocr_ratio_text,
		ocr_meas_timestamp=ocr_timestamp_text,
		meas_modbus_results=modbus_results,
		reset_time=reset_time
		)
		time.sleep(0.5)

	def config_setup_action(self,
					   main_menu=None,
					   side_menu=None,
					   data_view=None,
					   password=None,
					   popup_btn=None,
					   number_input=None,
					   apply_btn=True,
					   roi_keys=None,
					   correct_answers=None,
					   ratio_lower=None,
						ratio_upper=None,
						meas_lower=None,
						meas_upper=None,
						meas_unit=None,
						addr_meas=None,
						addr_timestamp=None,
						aggre_selection=None,
						reset_time=None,
						modbus_unit=None,
					   search_pattern=None,
					   base_save_path=None,
					   key_type=None,
					   ):
		"""
		예시 인자:
		- main_menu: ConfigTouch.touch_main_menu_1.value
		- side_menu: ConfigTouch.touch_side_menu_1.value
		- data_view: ConfigTouch.touch_data_view_1.value
		- password: True/False => 터치 패스워드
		- popup_btn: ConfigTouch.touch_btn_popup_2.value
		- number_input: '100000' (문자열)
		- apply_btn: True/False
		- roi_keys, except_addr, ref_value, template_path, roi_mask => setup_ocr_process에 필요
		- search_pattern, base_save_path => setup_ocr_process에 필요
		- eval_type: SELECTION, INTEGER, FLOAT
		- title_desc => 임의의 식별자 (setup_ocr_process 호출 시 구분)
		"""
		if main_menu is not None:
			self.touch_manager.touch_menu(main_menu)
		if side_menu is not None:
			self.touch_manager.touch_menu(side_menu)
		if data_view is not None:
			self.touch_manager.touch_menu(data_view)

		if password:
			self.touch_manager.touch_password() 

		if popup_btn is not None:
			self.touch_manager.touch_menu(popup_btn)
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)

		if number_input is not None:
			self.touch_manager.input_number(number_input, key_type=key_type)
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_popup_enter.value)

		if apply_btn:
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)

		if (roi_keys and base_save_path and search_pattern):
			self.test_mode_ocr_process(
						base_save_path=base_save_path, 
						search_pattern=search_pattern, 
						roi_keys=roi_keys, 
						correct_answers=correct_answers, 
						addr_meas=addr_meas,
						meas_lower=meas_lower,
						meas_upper=meas_upper,
						meas_unit=meas_unit,
						ratio_lower=ratio_lower,
						ratio_upper=ratio_upper,
						aggre_selection=aggre_selection,
						addr_timestamp=None,
						reset_time=reset_time,
						modbus_unit=None,
						)
		else:
			print(f"[DEBUG] Not calling setup_ocr_process for because some param is missing.")

	def meter_test_mode_balance(self, base_save_path, search_pattern):
		default_roi_keys = [ConfigROI.test_mode_balance_title, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas]

		self.touch_manager.uitest_mode_start()
		self.modbus_label.test_mode_balance_setting()
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()

		### VOLTAGE-RMS-LL
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_toggle_ll.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ll_fixed_text.value,
			meas_lower=tmb.voltage_rms_ll.value[0],
			meas_upper=tmb.voltage_rms_ll.value[1],
			meas_unit=tmb.voltage_rms_ll.value[2],
			addr_meas=[ConfigMap.addr_meas_vab.value, ConfigMap.addr_meas_vbc.value, ConfigMap.addr_meas_vca.value, ConfigMap.addr_meas_vavg_ll.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LL-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=21111,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ll_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_min_vab.value, ConfigMap.addr_meas_min_vbc.value, ConfigMap.addr_meas_min_vca.value, ConfigMap.addr_meas_min_vavg_ll.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LL-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=21111,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ll_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_max_vab.value, ConfigMap.addr_meas_max_vbc.value, ConfigMap.addr_meas_max_vca.value, ConfigMap.addr_meas_max_vavg_ll.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LN
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_ln.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=2112,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_van.value, ConfigMap.addr_meas_vbn.value, ConfigMap.addr_meas_vcn.value, ConfigMap.addr_meas_vavg_ln.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LN-Min
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=2112,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_min_van.value, ConfigMap.addr_meas_min_vbn.value, ConfigMap.addr_meas_min_vcn.value, ConfigMap.addr_meas_min_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LN-Max
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=2112,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_max_van.value, ConfigMap.addr_meas_max_vbn.value, ConfigMap.addr_meas_max_vcn.value, ConfigMap.addr_meas_max_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)

		### CURRENT-RMS-MAX
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			test_step=221,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_rms_fixed_text.value,
			addr_meas=[ConfigMap.addr_meas_max_ia.value, ConfigMap.addr_meas_max_ib.value, ConfigMap.addr_meas_max_ic.value, ConfigMap.addr_meas_max_iavg.value],
			addr_timestamp=None,
		  	aggre_selection=255,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)