import time
from function.func_ocr import PaddleOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation
from PySide6.QtCore import QObject

from config.config_touch import ConfigTouch
from config.config_demo_roi import ConfigROI
from config.config_map import ConfigMap
from config.config_map import ConfigInitialValue as civ
from config.config_test_mode_value import TestModeBalance as tmb

image_directory = r"\\10.10.20.30\screenshot"
paddleocr_func = PaddleOCRManager()

class DemoTest(QObject):
	 
	touch_manager = TouchManager()
	modbus_label = ModbusLabels()
	eval_manager = Evaluation()

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
						meas_rules,
						ratio_rules,
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
		start_time = self.modbus_label.system_time_read()
		self.touch_manager.screenshot()
		image_path = self.eval_manager.load_image_file(search_pattern, start_time)
		ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys)
		modbus_meas_result = self.modbus_label.read_float(address=addr_meas, aggre_selection=aggre_selection)
		if addr_timestamp:
			modbus_timestamp_result = self.modbus_label.read_float(address=addr_timestamp, aggre_selection=255)

		
		demo_test_result, ocr_error, ocr_missing_item, ocr_fixed_text, ocr_ratio_text, ocr_timestamp_text, ocr_measurement_text, modbus_results = self.eval_manager.eval_test_mode_balance(
			ocr_res=ocr_results, 
			correct_answers=correct_answers, 
			ratio_rules=ratio_rules,
			meas_rules=meas_rules,
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
					   ratio_rules=None,
						meas_rules=None,
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
						meas_rules=meas_rules,
						ratio_rules=ratio_rules,
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
			meas_rules=tmb.vol_rms_ll.value, 
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
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ll_fixed_text.value,
			meas_rules=tmb.vol_rms_ll.value,
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
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ll_fixed_text.value,
			meas_rules=tmb.vol_rms_ll.value,
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
			data_view=[ConfigTouch.touch_toggle_ln.value, ConfigTouch.touch_toggle_max.value],
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			meas_rules=tmb.vol_rms_ln.value,
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
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			meas_rules=tmb.vol_rms_ln.value,
			addr_meas=[ConfigMap.addr_meas_min_van.value, ConfigMap.addr_meas_min_vbn.value, ConfigMap.addr_meas_min_vcn.value, ConfigMap.addr_meas_min_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-RMS-LN-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_rms_ln_fixed_text.value,
			meas_rules=tmb.vol_rms_ln.value,
			addr_meas=[ConfigMap.addr_meas_max_van.value, ConfigMap.addr_meas_max_vbn.value, ConfigMap.addr_meas_max_vcn.value, ConfigMap.addr_meas_max_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LL
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ll_fixed_text.value,
			meas_rules=tmb.vol_fund_ll.value,
			addr_meas=[ConfigMap.addr_meas_fund_vab.value, ConfigMap.addr_meas_fund_vbc.value, ConfigMap.addr_meas_fund_vca.value, ConfigMap.addr_meas_fund_vavg_ll.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LL-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ll_fixed_text.value,
			meas_rules=tmb.vol_fund_ll.value,
			addr_meas=[ConfigMap.addr_meas_fund_min_vab.value, ConfigMap.addr_meas_fund_min_vbc.value, ConfigMap.addr_meas_fund_min_vca.value, ConfigMap.addr_meas_fund_min_vavg_ll.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LL-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ll_fixed_text.value,
			meas_rules=tmb.vol_fund_ll.value,
			addr_meas=[ConfigMap.addr_meas_fund_max_vab.value, ConfigMap.addr_meas_fund_max_vbc.value, ConfigMap.addr_meas_fund_max_vca.value, ConfigMap.addr_meas_fund_max_vavg_ll.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LN
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=[ConfigTouch.touch_toggle_ln.value, ConfigTouch.touch_toggle_max.value],
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ln_fixed_text.value,
			meas_rules=tmb.vol_fund_ln.value,
			addr_meas=[ConfigMap.addr_meas_fund_van.value, ConfigMap.addr_meas_fund_vbn.value, ConfigMap.addr_meas_fund_vcn.value, ConfigMap.addr_meas_fund_vavg_ln.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LN-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ln_fixed_text.value,
			meas_rules=tmb.vol_fund_ln.value,
			addr_meas=[ConfigMap.addr_meas_fund_min_van.value, ConfigMap.addr_meas_fund_min_vbn.value, ConfigMap.addr_meas_fund_min_vcn.value, ConfigMap.addr_meas_fund_min_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Fundamental-LN-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_fund_ln_fixed_text.value,
			meas_rules=tmb.vol_fund_ln.value,
			addr_meas=[ConfigMap.addr_meas_fund_max_van.value, ConfigMap.addr_meas_fund_max_vbn.value, ConfigMap.addr_meas_fund_max_vcn.value, ConfigMap.addr_meas_fund_max_vavg_ln.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-THD-LL
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_thd_ll_fixed_text.value,
			meas_rules=tmb.vol_thd_ll.value,
			addr_meas=[ConfigMap.addr_meas_thd_vab.value, ConfigMap.addr_meas_thd_vbc.value, ConfigMap.addr_meas_thd_vca.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-THD-LL-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_thd_ll_fixed_text.value,
			meas_rules=tmb.vol_thd_ll.value,
			addr_meas=[ConfigMap.addr_meas_thd_max_vab.value, ConfigMap.addr_meas_thd_max_vbc.value, ConfigMap.addr_meas_thd_max_vca.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-THD-LN
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=[ConfigTouch.touch_toggle_thd_ln.value, ConfigTouch.touch_toggle_max.value],
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_thd_ln_fixed_text.value,
			meas_rules=tmb.vol_thd_ln.value,
			addr_meas=[ConfigMap.addr_meas_thd_van.value, ConfigMap.addr_meas_thd_vbn.value, ConfigMap.addr_meas_thd_vcn.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-THD-LN-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_thd_ln_fixed_text.value,
			meas_rules=tmb.vol_thd_ln.value,
			addr_meas=[ConfigMap.addr_meas_thd_max_van.value, ConfigMap.addr_meas_thd_max_vbn.value, ConfigMap.addr_meas_thd_max_vcn.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Frequency
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_freq_fixed_text.value,
			meas_rules=tmb.vol_freq.value,
			addr_meas=[ConfigMap.addr_meas_frequency.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Frequency-min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_freq_fixed_text.value,
			meas_rules=tmb.vol_freq.value,
			addr_meas=[ConfigMap.addr_meas_freq_min.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Frequency-max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_vol_freq_fixed_text.value,
			meas_rules=tmb.vol_freq.value,
			addr_meas=[ConfigMap.addr_meas_freq_max.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Residual
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_5.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_vol_residual_fixed_text.value,
			meas_rules=tmb.vol_residual.value, 
			addr_meas=[ConfigMap.addr_meas_vrsd.value, ConfigMap.addr_meas_fund_vrsd.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Residual-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_vol_residual_fixed_text.value,
			meas_rules=tmb.vol_residual.value, 
			addr_meas=[ConfigMap.addr_meas_min_vrsd.value, ConfigMap.addr_meas_fund_min_vrsd.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### VOLTAGE-Residual-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_vol_residual_fixed_text.value,
			meas_rules=tmb.vol_residual.value, 
			addr_meas=[ConfigMap.addr_meas_max_vrsd.value, ConfigMap.addr_meas_fund_max_vrsd.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()

		### CURRENT-RMS
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_rms_fixed_text.value,
			ratio_rules=tmb.curr_rms_ratio.value,
			meas_rules=tmb.curr_rms.value,
			addr_meas=[ConfigMap.addr_meas_ia.value, ConfigMap.addr_meas_ib.value, ConfigMap.addr_meas_ic.value, ConfigMap.addr_meas_iavg.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)

		### CURRENT-RMS-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_rms_fixed_text.value,
			ratio_rules=tmb.curr_rms_ratio.value,
			meas_rules=tmb.curr_rms.value,
			addr_meas=[ConfigMap.addr_meas_min_ia.value, ConfigMap.addr_meas_min_ib.value, ConfigMap.addr_meas_min_ic.value, ConfigMap.addr_meas_min_iavg.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-RMS-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_rms_fixed_text.value,
			ratio_rules=tmb.curr_rms_ratio.value,
			meas_rules=tmb.curr_rms.value,
			addr_meas=[ConfigMap.addr_meas_max_ia.value, ConfigMap.addr_meas_max_ib.value, ConfigMap.addr_meas_max_ic.value, ConfigMap.addr_meas_max_iavg.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Fund
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_fund_fixed_text.value,
			ratio_rules=tmb.curr_fund_ratio.value,
			meas_rules=tmb.curr_fund.value,
			addr_meas=[ConfigMap.addr_meas_fund_ia.value, ConfigMap.addr_meas_fund_ib.value, ConfigMap.addr_meas_fund_ic.value, ConfigMap.addr_meas_max_iavg.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Fund-min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_fund_fixed_text.value,
			ratio_rules=tmb.curr_fund_ratio.value,
			meas_rules=tmb.curr_fund.value,
			addr_meas=[ConfigMap.addr_meas_fund_min_ia.value, ConfigMap.addr_meas_fund_min_ib.value, ConfigMap.addr_meas_fund_min_ic.value, ConfigMap.addr_meas_fund_min_iavg.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Fund-min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_fund_fixed_text.value,
			ratio_rules=tmb.curr_fund_ratio.value,
			meas_rules=tmb.curr_fund.value,
			addr_meas=[ConfigMap.addr_meas_fund_max_ia.value, ConfigMap.addr_meas_fund_max_ib.value, ConfigMap.addr_meas_fund_max_ic.value, ConfigMap.addr_meas_fund_max_iavg.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-demand
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_demand_fixed_text.value,
			ratio_rules=tmb.curr_demand_ratio.value,
			meas_rules=tmb.curr_demand.value,
			addr_meas=[ConfigMap.addr_meas_demand_ia.value, ConfigMap.addr_meas_demand_ib.value, ConfigMap.addr_meas_demand_ic.value, ConfigMap.addr_meas_demand_iavg.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-demand-peak
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_demand_fixed_text.value,
			ratio_rules=tmb.curr_demand_ratio.value,
			meas_rules=tmb.curr_demand.value,
			addr_meas=[ConfigMap.addr_meas_demand_max_ia.value, ConfigMap.addr_meas_demand_max_ib.value, ConfigMap.addr_meas_demand_max_ic.value, ConfigMap.addr_meas_demand_max_iavg.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-THD
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_thd_fixed_text.value,
			meas_rules=tmb.curr_thd.value,
			addr_meas=[ConfigMap.addr_meas_thd_ia.value, ConfigMap.addr_meas_thd_ib.value, ConfigMap.addr_meas_thd_ic.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-THD-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_thd_fixed_text.value,
			meas_rules=tmb.curr_thd.value,
			addr_meas=[ConfigMap.addr_meas_thd_max_ia.value, ConfigMap.addr_meas_thd_max_ib.value, ConfigMap.addr_meas_thd_max_ic.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-TDD
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_5.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_tdd_fixed_text.value,
			meas_rules=tmb.curr_tdd.value,
			addr_meas=[ConfigMap.addr_meas_tdd_ia.value, ConfigMap.addr_meas_tdd_ib.value, ConfigMap.addr_meas_tdd_ic.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-TDD-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_tdd_fixed_text.value,
			meas_rules=tmb.curr_tdd.value,
			addr_meas=[ConfigMap.addr_meas_tdd_max_ia.value, ConfigMap.addr_meas_tdd_max_ib.value, ConfigMap.addr_meas_tdd_max_ic.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Crest Factor
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_6.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_cf_fixed_text.value,
			meas_rules=tmb.curr_cf.value,
			addr_meas=[ConfigMap.addr_meas_cf_ia.value, ConfigMap.addr_meas_cf_ib.value, ConfigMap.addr_meas_cf_ic.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Crest Factor-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_cf_fixed_text.value,
			meas_rules=tmb.curr_cf.value,
			addr_meas=[ConfigMap.addr_meas_cf_max_ia.value, ConfigMap.addr_meas_cf_max_ib.value, ConfigMap.addr_meas_cf_max_ic.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-K Factor
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_7.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_kf_fixed_text.value,
			meas_rules=tmb.curr_kf.value,
			addr_meas=[ConfigMap.addr_meas_kf_ia.value, ConfigMap.addr_meas_kf_ib.value, ConfigMap.addr_meas_kf_ic.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-K Factor-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_curr_kf_fixed_text.value,
			meas_rules=tmb.curr_kf.value,
			addr_meas=[ConfigMap.addr_meas_kf_max_ia.value, ConfigMap.addr_meas_kf_max_ib.value, ConfigMap.addr_meas_kf_max_ic.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Residual
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_8.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_curr_residual_fixed_text.value,
			meas_rules=tmb.curr_residual.value,
			addr_meas=[ConfigMap.addr_meas_irsd.value, ConfigMap.addr_meas_fund_irsd.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Residual-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_curr_residual_fixed_text.value,
			meas_rules=tmb.curr_residual.value,
			addr_meas=[ConfigMap.addr_meas_min_irsd.value, ConfigMap.addr_meas_fund_min_irsd.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### CURRENT-Residual-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.tmb_title_residual_1, ConfigROI.tmb_title_residual_2, ConfigROI.test_mode_balance_phase, ConfigROI.test_mode_balance_ratio, ConfigROI.test_mode_balance_meas],
			correct_answers=ConfigROI.m_curr_residual_fixed_text.value,
			meas_rules=tmb.curr_residual.value,
			addr_meas=[ConfigMap.addr_meas_max_irsd.value, ConfigMap.addr_meas_fund_max_irsd.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Active
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_3.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_p_fixed_text.value,
			ratio_rules=tmb.pow_p_ratio.value,
			meas_rules=tmb.pow_p.value,
			addr_meas=[ConfigMap.addr_meas_pa.value, ConfigMap.addr_meas_pb.value, ConfigMap.addr_meas_pc.value, ConfigMap.addr_meas_p_total.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Active-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_p_fixed_text.value,
			ratio_rules=tmb.pow_p_ratio.value,
			meas_rules=tmb.pow_p.value,
			addr_meas=[ConfigMap.addr_meas_min_pa.value, ConfigMap.addr_meas_min_pb.value, ConfigMap.addr_meas_min_pc.value, ConfigMap.addr_meas_min_ptotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Active-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_p_fixed_text.value,
			ratio_rules=tmb.pow_p_ratio.value,
			meas_rules=tmb.pow_p.value,
			addr_meas=[ConfigMap.addr_meas_max_pa.value, ConfigMap.addr_meas_max_pb.value, ConfigMap.addr_meas_max_pc.value, ConfigMap.addr_meas_max_ptotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Reactive
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_q_fixed_text.value,
			ratio_rules=tmb.pow_q_ratio.value,
			meas_rules=tmb.pow_q.value,
			addr_meas=[ConfigMap.addr_meas_qa.value, ConfigMap.addr_meas_qb.value, ConfigMap.addr_meas_qc.value, ConfigMap.addr_meas_q_total.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Reactive-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_q_fixed_text.value,
			ratio_rules=tmb.pow_q_ratio.value,
			meas_rules=tmb.pow_q.value,
			addr_meas=[ConfigMap.addr_meas_min_qa.value, ConfigMap.addr_meas_min_qb.value, ConfigMap.addr_meas_min_qc.value, ConfigMap.addr_meas_min_qtotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Active-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_q_fixed_text.value,
			ratio_rules=tmb.pow_q_ratio.value,
			meas_rules=tmb.pow_q.value,
			addr_meas=[ConfigMap.addr_meas_max_qa.value, ConfigMap.addr_meas_max_qb.value, ConfigMap.addr_meas_max_qc.value, ConfigMap.addr_meas_max_qtotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Apparent
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_s_fixed_text.value,
			ratio_rules=tmb.pow_s_ratio.value,
			meas_rules=tmb.pow_s.value,
			addr_meas=[ConfigMap.addr_meas_sa.value, ConfigMap.addr_meas_sb.value, ConfigMap.addr_meas_sc.value, ConfigMap.addr_meas_s_total.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Apparent-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_s_fixed_text.value,
			ratio_rules=tmb.pow_s_ratio.value,
			meas_rules=tmb.pow_s.value,
			addr_meas=[ConfigMap.addr_meas_min_sa.value, ConfigMap.addr_meas_min_sb.value, ConfigMap.addr_meas_min_sc.value, ConfigMap.addr_meas_min_stotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Apparent-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_s_fixed_text.value,
			ratio_rules=tmb.pow_s_ratio.value,
			meas_rules=tmb.pow_s.value,
			addr_meas=[ConfigMap.addr_meas_max_sa.value, ConfigMap.addr_meas_max_sb.value, ConfigMap.addr_meas_max_sc.value, ConfigMap.addr_meas_max_stotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-PF
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_pf_fixed_text.value,
			ratio_rules=tmb.pow_pf_ratio.value,
			meas_rules=tmb.pow_pf.value,
			addr_meas=[ConfigMap.addr_meas_pfa.value, ConfigMap.addr_meas_pfb.value, ConfigMap.addr_meas_pfc.value, ConfigMap.addr_meas_pf_total.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-PF-Min
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_min.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_pf_fixed_text.value,
			ratio_rules=tmb.pow_pf_ratio.value,
			meas_rules=tmb.pow_pf.value,
			addr_meas=[ConfigMap.addr_meas_min_pfa.value, ConfigMap.addr_meas_min_pfb.value, ConfigMap.addr_meas_min_pfc.value, ConfigMap.addr_meas_min_pftotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-PF-Max
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_pf_fixed_text.value,
			ratio_rules=tmb.pow_pf_ratio.value,
			meas_rules=tmb.pow_pf.value,
			addr_meas=[ConfigMap.addr_meas_max_pfa.value, ConfigMap.addr_meas_max_pfb.value, ConfigMap.addr_meas_max_pfc.value, ConfigMap.addr_meas_max_pftotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Demand
		self.config_setup_action(
			main_menu=None,
			side_menu=ConfigTouch.touch_side_menu_5.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_demand_fixed_text.value,
			ratio_rules=tmb.pow_demand_ratio.value,
			meas_rules=tmb.pow_demand.value,
			addr_meas=[ConfigMap.addr_meas_demand_pa.value, ConfigMap.addr_meas_demand_pb.value, ConfigMap.addr_meas_demand_pc.value, ConfigMap.addr_meas_demand_ptotal.value],
			aggre_selection=1,
			addr_timestamp=None,
			reset_time=None,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		### POWER-Demand-Peak
		reset_time = self.modbus_label.reset_max_min()
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_toggle_max.value,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=default_roi_keys,
			correct_answers=ConfigROI.m_pow_demand_fixed_text.value,
			ratio_rules=tmb.pow_demand_ratio.value,
			meas_rules=tmb.pow_demand.value,
			addr_meas=[ConfigMap.addr_meas_demand_max_pa.value, ConfigMap.addr_meas_demand_max_pb.value, ConfigMap.addr_meas_demand_max_pc.value, ConfigMap.addr_mea_demand_max_ptotal.value],
			aggre_selection=255,
			addr_timestamp=None,
			reset_time=reset_time,
			modbus_unit=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			key_type=None,
			)
		
		self.modbus_label.test_mode_off()
