import time
from function.func_ocr import PaddleOCRManager
from function.func_touch import TouchManager
from function.func_modbus import ModbusLabels
from function.func_evaluation import Evaluation
from function.func_autogui import AutoGUI
from PySide6.QtCore import Qt, QObject

from config.config_touch import ConfigTouch
from config.config_roi import ConfigROI, SelectType
from config.config_map import ConfigMap
from config.config_map import ConfigInitialValue as civ
from config.config_ref import ConfigImgRef

image_directory = r"\\10.10.20.30\screenshot"
paddleocr_func = PaddleOCRManager()

class SetupTest(QObject):
     
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

	def setup_ocr_process(self, base_save_path, search_pattern, roi_keys, except_address, access_address, setup_answer_key, template_path, roi_mask, modbus_ref, eval_type=0, refresh=None, coordinates=None, modbus_unit=None, compare_exc=None):
		sm_condition = False
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
		setup = 1
		ocr_results = paddleocr_func.paddleocr_basic(image=image_path, roi_keys=roi_keys, test_type=setup)
		except_addr = {except_address}
		target_address = except_address
		setup_expected_value = setup_answer_key
		if compare_exc == 1:
			compare_title = roi_keys[0].value[1][0]
		else:
			compare_title = roi_keys[0].value[0]
		
		if roi_keys[1] == ConfigROI.s_primary_reference_vol_3:
			parts = setup_answer_key.split(',')
			numeric_part_with_space = parts[0]
			setup_expected_value = numeric_part_with_space.strip()

			ocr_1 = ocr_results[1]
			parts_ocr = ocr_1.split(',')
			numeric_part_with_space4 = parts_ocr[0]
			ocr_1 = numeric_part_with_space4.strip()
			ocr_results[1] = ocr_1

		if roi_keys[1] == ConfigROI.s_primary_reference_vol_4:
			parts = setup_answer_key.split(',')
			numeric_part_with_space = parts[-1]
			setup_expected_value = numeric_part_with_space.strip()

			ocr_1 = ocr_results[1]
			parts_ocr = ocr_1.split(',')
			numeric_part_with_space4 = parts_ocr[-1]
			ocr_1 = numeric_part_with_space4.strip()
			ocr_results[1] = ocr_1
			
		if self.accruasm_state == 2 and refresh == 'event':
			self.autogui_manager.m_s_event_refresh(image_path, base_save_path, compare_title)
			time.sleep(2.0)
			sm_res, sm_condition = self.autogui_manager.find_and_click(template_path, image_path, base_save_path, compare_title, roi_mask=roi_mask)

		elif self.accruasm_state == 2:
			self.autogui_manager.m_s_meas_refresh(image_path, base_save_path, compare_title)
			time.sleep(2.0)
			sm_res, sm_condition = self.autogui_manager.find_and_click(template_path, image_path, base_save_path, compare_title, roi_mask=roi_mask)

		else:
			sm_res = None
			self.accruasm_state = None
		title, setup_result, modbus_result, overall_result = self.eval_manager.eval_setup_test(
			ocr_res=ocr_results,
			setup_expected_value=setup_expected_value,
			title=compare_title,
			ecm_access_address=access_address,
			ecm_address=target_address,
			except_addr=except_addr,
			sm_res=sm_res,
			sm_condition = sm_condition,
			modbus_ref=modbus_ref,
			modbus_unit=modbus_unit,
			eval_type=eval_type,
			)
		self.eval_manager.setup_save_csv(setup_result, modbus_result, image_path, base_save_path, overall_result, title)
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
                       except_addr=None,
					   access_address=None,
                       setup_answer_key=None,
					   modbus_answer_key=None,
					   modbus_unit=None,
                       template_path=None,
                       roi_mask=None,
                       search_pattern=None,
                       base_save_path=None,
					   refresh=None,
					   eval_type=None,
					   key_type=None,
					   compare_exc=None,
                       title_desc=None):
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

		if (roi_keys and except_addr and setup_answer_key and template_path and roi_mask
			and base_save_path and search_pattern):
			self.setup_ocr_process(
				base_save_path,
				search_pattern,
				roi_keys=roi_keys,
				except_address=except_addr,
				access_address=access_address,
				setup_answer_key=setup_answer_key,
				template_path=template_path,
				roi_mask=roi_mask,
				refresh=refresh,
				modbus_ref=modbus_answer_key,
				modbus_unit=modbus_unit,
				eval_type=eval_type,
				compare_exc=compare_exc
			)
		else:
			print(f"[DEBUG] Not calling setup_ocr_process for {title_desc} because some param is missing.")

	def setup_m_s_meas_all(self, base_save_path, search_pattern):
		self.setup_meter_s_m_vol(base_save_path, search_pattern)
		self.setup_meter_s_m_curr(base_save_path, search_pattern)
		self.m_s_meas_demand(base_save_path, search_pattern)
		self.m_s_meas_power(base_save_path, search_pattern)

	def setup_meter_s_m_vol(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()

		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### wiring -> Delta
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_wiring_1, ConfigROI.s_wiring_2],
			except_addr=ConfigMap.addr_wiring,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_wiring_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_wiring_2.value[1]['Delta'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### wiring -> Wye
		self.config_setup_action(
			main_menu=None,
			side_menu=None, 
			data_view=ConfigTouch.touch_data_view_1.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_wiring_1, ConfigROI.s_wiring_2],
			except_addr=ConfigMap.addr_wiring,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_wiring_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_wiring_2.value[1]['Wye'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### min.meas.secondary l-n volt 5-> 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=False,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2],
			except_addr=ConfigMap.addr_min_measured_secondary_ln_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][0],
			modbus_answer_key=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### min.meas.secondary l-n volt 0-> 11
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=False,
			popup_btn=None,
			number_input='11',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_sec_ln_vol_1, ConfigROI.s_min_meas_sec_ln_vol_2],
			except_addr=ConfigMap.addr_min_measured_secondary_ln_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][1],
			modbus_answer_key=ConfigROI.s_min_meas_sec_ln_vol_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_min_measured_secondary_ln_voltage, bit16=5)

		### VT Primary L-L Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=False,
			popup_btn=None,
			number_input='49',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_primary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_vt_primary_ll_vol_2.value[1][0],
			modbus_answer_key=ConfigROI.s_vt_primary_ll_vol_2.value[1][0],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### VT Primary L-L Voltage 1000000
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=False,
			popup_btn=None,
			number_input='1000000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_primary_ll_vol_1, ConfigROI.s_vt_primary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_primary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_vt_primary_ll_vol_2.value[1][1],
			modbus_answer_key=ConfigROI.s_vt_primary_ll_vol_2.value[1][1],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### VT Primary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_primary_ll_voltage, bit32=1900)

		### VT Secondary L-L Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=False,
			popup_btn=None,
			number_input='49',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_secondary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_vt_secondary_ll_vol_2.value[1][0],
			modbus_answer_key=ConfigROI.s_vt_secondary_ll_vol_2.value[1][0],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### VT Secondary L-L Voltage 221
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=False,
			popup_btn=None,
			number_input='221',
			apply_btn=True,
			roi_keys=[ConfigROI.s_vt_secondary_ll_vol_1, ConfigROI.s_vt_secondary_ll_vol_2],
			except_addr=ConfigMap.addr_vt_secondary_ll_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_vt_secondary_ll_vol_2.value[1][1],
			modbus_answer_key=ConfigROI.s_vt_secondary_ll_vol_2.value[1][1],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_vt_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### VT Secondary L-L Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_vt_secondary_ll_voltage, bit16=1900)

		### Primary Reference Voltage L-L -> L-N
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_ref_ln.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3],
			except_addr=ConfigMap.addr_reference_voltage_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_primary_reference_vol_3.value[1])[1],
			modbus_answer_key=ConfigROI.s_primary_reference_vol_3.value[1]['Line-to-Neutral, 190.0'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage L-N -> L-L
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_ref_ll.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_3],
			except_addr=ConfigMap.addr_reference_voltage_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_primary_reference_vol_3.value[1])[0],
			modbus_answer_key=ConfigROI.s_primary_reference_vol_3.value[1]['Line-to-Line, 190.0'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage 49
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=None,
			number_input='49', key_type='ref',
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_4],
			except_addr=ConfigMap.addr_reference_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_primary_reference_vol_4.value[1][0],
			modbus_answer_key=ConfigROI.s_primary_reference_vol_4.value[1][0],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Primary Reference Voltage 1000000
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=False,
			popup_btn=None,
			number_input='1000000', key_type='ref',
			apply_btn=True,
			roi_keys=[ConfigROI.s_primary_reference_vol_1, ConfigROI.s_primary_reference_vol_4],
			except_addr=ConfigMap.addr_reference_voltage,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_primary_reference_vol_4.value[1][1],
			modbus_answer_key=ConfigROI.s_primary_reference_vol_4.value[1][1],
			eval_type=SelectType.type_float.value,
			modbus_unit=1,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_primary_reference_voltage_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		###  Primary Reference Voltage 초기화
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_reference_voltage, bit32=1900)

		### Sliding Reference Voltage Disable -> Enable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2],
			except_addr=ConfigMap.addr_sliding_reference_voltage_type,
			access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sliding_reference_vol_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_sliding_reference_vol_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_sliding_reference_voltage.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Sliding Reference Voltage Enable -> Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sliding_reference_vol_1, ConfigROI.s_sliding_reference_vol_2],
			except_addr=ConfigMap.addr_sliding_reference_voltage_type,
			access_address=ConfigMap.addr_sliding_reference_voltage_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sliding_reference_vol_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_sliding_reference_vol_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_sliding_reference_voltage.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Rotating Sequence Positive -> Negative
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_7.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_2],
			except_addr=ConfigMap.addr_rotating_sequence,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rotation_sequence_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_rotation_sequence_2.value[1]['Negative'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_rotating_sequence.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Rotating Sequence Negative -> Positive
		self.config_setup_action(
			main_menu=None, 
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_7.value,
			password=False,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rotation_sequence_1, ConfigROI.s_rotation_sequence_2],
			except_addr=ConfigMap.addr_rotating_sequence,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rotation_sequence_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_rotation_sequence_2.value[1]['Positive'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_rotating_sequence.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

	def setup_meter_s_m_curr(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### CT Primary Current 50 -> 5 (4로 변경)
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2],
			except_addr=ConfigMap.addr_ct_primary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_ct_primary_curr_2.value[1][0],
			modbus_answer_key=ConfigROI.s_ct_primary_curr_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,)
		
		### CT Primary Current 5 -> 99999 (100000로 변경) ---> 여기 부터 변경 필요
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='100000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_primary_curr_1, ConfigROI.s_ct_primary_curr_2],
			except_addr=ConfigMap.addr_ct_primary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_ct_primary_curr_2.value[1][1],
			modbus_answer_key=ConfigROI.s_ct_primary_curr_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_primary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### CT Primary Current 초기화(50)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_ct_primary_current, bit32=50)

		## CT Secondary Current 5-> 10 (11로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='11',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2],
			except_addr=ConfigMap.addr_ct_secondary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_ct_secondary_curr_2.value[1][1],
			modbus_answer_key=ConfigROI.s_ct_secondary_curr_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### CT Secondary Current 10-> 5 (4로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_ct_secondary_curr_1, ConfigROI.s_ct_secondary_curr_2],
			except_addr=ConfigMap.addr_ct_secondary_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_ct_secondary_curr_2.value[1][0],
			modbus_answer_key=ConfigROI.s_ct_secondary_curr_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_ct_secondary.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Reference Current 50 > 5 (4로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_reference_curr_1, ConfigROI.s_reference_curr_2],
			except_addr=ConfigMap.addr_reference_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_reference_curr_2.value[1][0],
			modbus_answer_key=ConfigROI.s_reference_curr_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_reference_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Reference Current 50 > 99999 (100000로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='100000',
			apply_btn=True,
			roi_keys=[ConfigROI.s_reference_curr_1, ConfigROI.s_reference_curr_2],
			except_addr=ConfigMap.addr_reference_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_reference_curr_2.value[1][1],
			modbus_answer_key=ConfigROI.s_reference_curr_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_reference_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### Reference Current 초기화(50)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_reference_current, bit32=50)
		
		### min measured current 5 > 0 (0으로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_curr_1, ConfigROI.s_min_meas_curr_2],
			except_addr=ConfigMap.addr_min_measured_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_min_meas_curr_2.value[1][0],
			modbus_answer_key=ConfigROI.s_min_meas_curr_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### min measured current 0 > 100 (101으로 변경)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='101',
			apply_btn=True,
			roi_keys=[ConfigROI.s_min_meas_curr_1, ConfigROI.s_min_meas_curr_2],
			except_addr=ConfigMap.addr_min_measured_current,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_min_meas_curr_2.value[1][1],
			modbus_answer_key=ConfigROI.s_min_meas_curr_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_curr.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### min measured current 초기화(5)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_min_measured_current, bit16=5)
		
		### tdd reference selection / peak demand > tdd nominal
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_tdd_reference_selection_1, ConfigROI.s_tdd_reference_selection_2],
			except_addr=ConfigMap.addr_tdd_reference,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_tdd_reference_selection_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_tdd_reference_selection_2.value[1]['TDD Nominal Current'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_tdd_reference_selection.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### tdd reference selection / tdd nominal > peak demand
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_tdd_reference_selection_1, ConfigROI.s_tdd_reference_selection_2],
			except_addr=ConfigMap.addr_tdd_reference,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_tdd_reference_selection_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_tdd_reference_selection_2.value[1]['Peak Demand Current'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_tdd_reference_selection.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### tdd nominal current 0 > 1 (reference current 체크 해제 후 0)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		setup_answer_key = roi_keys[1].value[1][1]
		eval_type=SelectType.type_float.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

		### tdd nominal current 1 > 99999 (100000으로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_1.value)
		for i in range(5):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		setup_answer_key = roi_keys[1].value[1][2]
		eval_type=SelectType.type_float.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_max.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

		### tdd nominal current 9999 > 0 (reference current로 변경)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_6.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys = [ConfigROI.s_tdd_nominal_curr_1, ConfigROI.s_tdd_nominal_curr_2]
		except_addr = ConfigMap.addr_nominal_tdd_current
		setup_answer_key = roi_keys[1].value[1][0]
		eval_type=SelectType.type_integer.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_measurement_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

	def m_s_meas_demand(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Sub-interval time 15 > 1 (input 0)
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sub_interval_time_1, ConfigROI.s_sub_interval_time_2],
			except_addr=ConfigMap.addr_sub_interval_time,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_sub_interval_time_2.value[1][0],
			modbus_answer_key=ConfigROI.s_sub_interval_time_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_subinterval_time.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sub-interval time 1 > 60 (input 61)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='61',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sub_interval_time_1, ConfigROI.s_sub_interval_time_2],
			except_addr=ConfigMap.addr_sub_interval_time,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_sub_interval_time_2.value[1][1],
			modbus_answer_key=ConfigROI.s_sub_interval_time_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_subinterval_time.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### min measured current 초기화(15)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_sub_interval_time, bit16=15)
		
		### Number of Sub-Intervals 1 > 12 (input 13)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='61',
			apply_btn=True,
			roi_keys=[ConfigROI.s_number_of_sub_intervals_1, ConfigROI.s_number_of_sub_intervals_2],
			except_addr=ConfigMap.addr_num_of_sub_interval,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_number_of_sub_intervals_2.value[1][1],
			modbus_answer_key=ConfigROI.s_number_of_sub_intervals_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_number_of_subintervals.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Number of Sub-Intervals 12 > 1 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_number_of_sub_intervals_1, ConfigROI.s_number_of_sub_intervals_2],
			except_addr=ConfigMap.addr_num_of_sub_interval,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_number_of_sub_intervals_2.value[1][0],
			modbus_answer_key=ConfigROI.s_number_of_sub_intervals_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_number_of_subintervals.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Power Type 0 > 1 (input 1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_power_type_1, ConfigROI.s_demand_power_type_2],
			except_addr=ConfigMap.addr_demand_power_type,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_demand_power_type_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_demand_power_type_2.value[1]['Net'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_power_type.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Power Type 1 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_power_type_1, ConfigROI.s_demand_power_type_2],
			except_addr=ConfigMap.addr_demand_power_type,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_demand_power_type_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_demand_power_type_2.value[1]['Received'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_power_type.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Sync Mode 0 > 1 (input 1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_sync_mode_1, ConfigROI.s_demand_sync_mode_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_demand_sync_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_demand_sync_mode_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_demand_sync_mode_2.value[1]['Manual Sync'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_sync_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Demand Sync Mode 1 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_demand_sync_mode_1, ConfigROI.s_demand_sync_mode_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_demand_sync_mode,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_demand_sync_mode_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_demand_sync_mode_2.value[1]['Hourly Auto Sync'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_demand_sync_mode.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Thermal Response Index 90 > 0 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_thermal_response_index_1, ConfigROI.s_thermal_response_index_2],
			except_addr=ConfigMap.addr_thermal_response_index,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_thermal_response_index_2.value[1][0],
			modbus_answer_key=ConfigROI.s_thermal_response_index_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_thermal_response_index.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Thermal Response Index 0 > 100 (input 101)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='101',
			apply_btn=True,
			roi_keys=[ConfigROI.s_thermal_response_index_1, ConfigROI.s_thermal_response_index_2],
			except_addr=ConfigMap.addr_thermal_response_index,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=ConfigROI.s_thermal_response_index_2.value[1][1],
			modbus_answer_key=ConfigROI.s_thermal_response_index_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_thermal_response_index.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### Thermal Response Index 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_measurement_setup_access, ConfigMap.addr_thermal_response_index, bit16=90)

	def m_s_meas_power(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Phase Power Calculation 1 > 0 (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_phase_power_calculation_1, ConfigROI.s_phase_power_calculation_2],
			except_addr=ConfigMap.addr_phase_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_phase_power_calculation_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_phase_power_calculation_2.value[1]['Fundamental'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_phase_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Phase Power Calculation 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_phase_power_calculation_1, ConfigROI.s_phase_power_calculation_2],
			except_addr=ConfigMap.addr_phase_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_phase_power_calculation_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_phase_power_calculation_2.value[1]['RMS'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_phase_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

		### Total Power Calculation 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_total_power_calculation_1, ConfigROI.s_total_power_calculation_2],
			except_addr=ConfigMap.addr_total_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_total_power_calculation_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_total_power_calculation_2.value[1]['Arithmetic Sum'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_total_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Total Power Calculation 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_total_power_calculation_1, ConfigROI.s_total_power_calculation_2],
			except_addr=ConfigMap.addr_total_power_calculation,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_total_power_calculation_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_total_power_calculation_2.value[1]['Vector Sum'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_total_power_calculation.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Sign 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_sign_1, ConfigROI.s_pf_sign_2],
			except_addr=ConfigMap.addr_pf_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pf_sign_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_pf_sign_2.value[1]['Unsigned'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Sign 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_sign_1, ConfigROI.s_pf_sign_2],
			except_addr=ConfigMap.addr_pf_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pf_sign_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_pf_sign_2.value[1]['Signed'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Value at No-Load 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_value_at_noload_1, ConfigROI.s_pf_value_at_noload_2],
			except_addr=ConfigMap.addr_pf_value_at_no_load,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pf_value_at_noload_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_pf_value_at_noload_2.value[1]['PF = 0'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_value_at_noload.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### PF Value at No-Load 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pf_value_at_noload_1, ConfigROI.s_pf_value_at_noload_2],
			except_addr=ConfigMap.addr_pf_value_at_no_load,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pf_value_at_noload_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_pf_value_at_noload_2.value[1]['PF = 1'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_pf_value_at_noload.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Reactive Power Sign 1 > 0 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_reactive_power_sign_1, ConfigROI.s_reactive_power_sign_2],
			except_addr=ConfigMap.addr_reactive_power_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_reactive_power_sign_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_reactive_power_sign_2.value[1]['Unsigned'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_reactive_power_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Reactive Power Sign 0 > 1 (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_reactive_power_sign_1, ConfigROI.s_reactive_power_sign_2],
			except_addr=ConfigMap.addr_reactive_power_sign,
			access_address=ConfigMap.addr_measurement_setup_access.value,
			setup_answer_key=list(ConfigROI.s_reactive_power_sign_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_reactive_power_sign_2.value[1]['Signed'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_reactive_power_sign.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
	
	def setup_m_s_event_all(self, base_save_path, search_pattern):
		self.m_s_event_dip(self, base_save_path, search_pattern)
		self.m_s_event_swell(self, base_save_path, search_pattern)
		self.m_s_event_pq_curve(self, base_save_path, search_pattern)
	
	def m_s_event_dip(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		### Dip Trigger Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_trigger_1, ConfigROI.s_dip_trigger_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_trigger_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_dip_trigger_2.value[1][1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Trigger Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_trigger_1, ConfigROI.s_dip_trigger_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_trigger_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_dip_trigger_2.value[1][1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Threshold 90 > 10 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_threshold_1, ConfigROI.s_dip_threshold_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip_threshold,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_threshold_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_dip_threshold_2.value[1][1][0],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip Threshold 10 > 99 (input 100)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='100',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_threshold_1, ConfigROI.s_dip_threshold_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip_threshold,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_threshold_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_dip_threshold_2.value[1][1][1],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### min measured current 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_dip_setup_access, ConfigMap.addr_dip_threshold, bit16=900)
		
		### Dip hysteresis 2 > 1 (input 0)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_hysteresis_1, ConfigROI.s_dip_hysteresis_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip_hysteresis,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_hysteresis_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_dip_hysteresis_2.value[1][1][0],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Dip hysteresis 1 > 99 (input 100)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='100',
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_hysteresis_1, ConfigROI.s_dip_hysteresis_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_dip_hysteresis,
			access_address=ConfigMap.addr_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_hysteresis_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_dip_hysteresis_2.value[1][1][1],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_dip_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### min measured current 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_dip_setup_access, ConfigMap.addr_dip_hysteresis, bit16=20)

		### 3-Phase Dip Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_3phase_dip_1, ConfigROI.s_dip_3phase_dip_2],
			except_addr=ConfigMap.addr_3phase_dip,
			access_address=ConfigMap.addr_3phase_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_3phase_dip_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_dip_3phase_dip_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_3dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### 3-Phase Dip Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_dip_3phase_dip_1, ConfigROI.s_dip_3phase_dip_2],
			except_addr=ConfigMap.addr_3phase_dip,
			access_address=ConfigMap.addr_3phase_dip_setup_access.value,
			setup_answer_key=list(ConfigROI.s_dip_3phase_dip_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_dip_3phase_dip_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_3dip_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
	def m_s_event_swell(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		
		### Swell Trigger Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_trigger_1, ConfigROI.s_swell_trigger_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_trigger_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_swell_trigger_2.value[1][1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Trigger Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_trigger_1, ConfigROI.s_swell_trigger_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_trigger_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_swell_trigger_2.value[1][1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_trigger.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Threshold 110 > 101 (input 100.9)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='100.9',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_threshold_1, ConfigROI.s_swell_threshold_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell_threshold,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_threshold_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_swell_threshold_2.value[1][1][0],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Threshold 101 > 999 (input 999.1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='999.1',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_threshold_1, ConfigROI.s_swell_threshold_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell_threshold,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_threshold_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_swell_threshold_2.value[1][1][1],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_threshold.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### Swell Threshold 초기화(110)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_swell_setup_access, ConfigMap.addr_swell_threshold, bit16=1100)

		### Swell Hysteresis 2 > 1 (input 0.9)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='0.9',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_hysteresis_1, ConfigROI.s_swell_hysteresis_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell_hysteresis,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_hysteresis_2.value[1][1])[0],
			modbus_answer_key=ConfigROI.s_swell_hysteresis_2.value[1][1][0],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### Swell Hysteresis 1 > 99 (input 99.1)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='99.1',
			apply_btn=True,
			roi_keys=[ConfigROI.s_swell_hysteresis_1, ConfigROI.s_swell_hysteresis_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_swell_hysteresis,
			access_address=ConfigMap.addr_swell_setup_access.value,
			setup_answer_key=list(ConfigROI.s_swell_hysteresis_2.value[1][1])[1],
			modbus_answer_key=ConfigROI.s_swell_hysteresis_2.value[1][1][1],
			eval_type=SelectType.type_float.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_swell_hysteresis.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		### Swell Hysteresis 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_swell_setup_access, ConfigMap.addr_swell_hysteresis, bit16=20)

	def m_s_event_pq_curve(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()
		
		### SEMI F47-0706 Disable > Enable (input )
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_2.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_semi_1, ConfigROI.s_pq_curve_semi_2],
			except_addr=ConfigMap.addr_semi,
			access_address=ConfigMap.addr_semi_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_semi_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_pq_curve_semi_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_semi.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### SEMI F47-0706 Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_semi_1, ConfigROI.s_pq_curve_semi_2],
			except_addr=ConfigMap.addr_semi,
			access_address=ConfigMap.addr_semi_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_semi_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_pq_curve_semi_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_semi.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### IEC 61000-4-11/34 Class 3 Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_iec_1, ConfigROI.s_pq_curve_iec_2],
			except_addr=ConfigMap.addr_iec,
			access_address=ConfigMap.addr_iec_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_iec_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_pq_curve_iec_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_iec.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### IEC 61000-4-11/34 Class 3 Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_iec_1, ConfigROI.s_pq_curve_iec_2],
			except_addr=ConfigMap.addr_iec,
			access_address=ConfigMap.addr_iec_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_iec_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_pq_curve_iec_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_iec.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### ITIC Disable > Enable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_itic_1, ConfigROI.s_pq_curve_itic_2],
			except_addr=ConfigMap.addr_itic,
			access_address=ConfigMap.addr_itic_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_itic_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_pq_curve_itic_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_itic.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
		
		### ITIC Enable > Disable (input )
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_pq_curve_itic_1, ConfigROI.s_pq_curve_itic_2],
			except_addr=ConfigMap.addr_itic,
			access_address=ConfigMap.addr_itic_event_setup_access.value,
			setup_answer_key=list(ConfigROI.s_pq_curve_itic_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_pq_curve_itic_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
			roi_mask=ConfigROI.mask_m_s_event_pq_curve_itic.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path,
			refresh='event')
	
	def setup_m_s_network_all(self, base_save_path, search_pattern):
		self.m_s_network_ethernet(self, base_save_path, search_pattern)
		self.m_s_network_rs485(self, base_save_path, search_pattern)
		self.m_s_network_advanced(self, base_save_path, search_pattern)

	def m_s_network_ethernet(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_setup()

		# ### Ethernet DHCP Disable > Enable ip가 변경되는 상황이라 주석처리
		# self.config_setup_action(
		# 	main_menu=ConfigTouch.touch_main_menu_3.value,
		# 	side_menu=ConfigTouch.touch_side_menu_1.value,
		# 	data_view=ConfigTouch.touch_data_view_5.value,
		# 	password=True,
		# 	popup_btn=ConfigTouch.touch_btn_popup_2.value,
		# 	number_input=None,
		# 	apply_btn=True,
		# 	roi_keys=[ConfigROI.s_dhcp_1, ConfigROI.s_dhcp_2],
		# 	except_addr=ConfigMap.addr_dhcp,
		# 	access_address=ConfigMap.addr_dhcp_setup_access.value,
		# 	ref_value=list(ConfigROI.s_dhcp_2.value[1])[1],
		# 	ref_select=1,
		# 	modbus_ref=ConfigROI.s_dhcp_2.value[1]['Enable'],
		# 	template_path=ConfigImgRef.img_ref_meter_setup_event_max.value,
		# 	roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
		# 	search_pattern=search_pattern,
		# 	base_save_path=base_save_path,
		# 	refresh='event')
		
		# ### Ethernet DHCP Enable > Disable
		# self.config_setup_action(
		# 	main_menu=None,
		# 	side_menu=None,
		# 	data_view=ConfigTouch.touch_data_view_5.value,
		# 	password=None,
		# 	popup_btn=ConfigTouch.touch_btn_popup_1.value,
		# 	number_input=None,
		# 	apply_btn=True,
		# 	roi_keys=[ConfigROI.s_dhcp_1, ConfigROI.s_dhcp_2],
		# 	except_addr=ConfigMap.addr_dhcp,
		# 	access_address=ConfigMap.addr_dhcp_setup_access.value,
		# 	ref_value=list(ConfigROI.s_dhcp_2.value[1])[0],
		# 	ref_select=1,
		# 	modbus_ref=ConfigROI.s_dhcp_2.value[1]['Disable'],
		# 	template_path=ConfigImgRef.img_ref_meter_setup_event_min.value,
		# 	roi_mask=ConfigROI.mask_m_s_event_dip_trigger.value,
		# 	search_pattern=search_pattern,
		# 	base_save_path=base_save_path,
		# 	refresh='event')
		
	def m_s_network_rs485(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### device address 0 > 247
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_3.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='248',
			apply_btn=True,
			roi_keys=[ConfigROI.s_device_address_1, ConfigROI.s_device_address_2],
			except_addr=ConfigMap.addr_device_address,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=ConfigROI.s_device_address_2.value[1][1],
			modbus_answer_key=ConfigROI.s_device_address_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### device address 247 > 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_device_address_1, ConfigROI.s_device_address_2],
			except_addr=ConfigMap.addr_device_address,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=ConfigROI.s_device_address_2.value[1][0],
			modbus_answer_key=ConfigROI.s_device_address_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 1200
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['1200'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 2400
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['2400'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 4800
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['4800'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 9600
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_7.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['9600'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 19200
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_9.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['19200'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 38400
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_11.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[5],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['38400'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 57600
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[6],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['57600'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### bit rate 115200
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_4.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_bit_rate_1, ConfigROI.s_bit_rate_2],
			except_addr=ConfigMap.addr_bit_rate,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_bit_rate_2.value[1])[7],
			modbus_answer_key=ConfigROI.s_bit_rate_2.value[1]['115200'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		### Swell Hysteresis 초기화(90)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_rs485_setup_access, ConfigMap.addr_bit_rate, bit16=3)
		
		### parity even > none
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_parity_1, ConfigROI.s_parity_2],
			except_addr=ConfigMap.addr_parity,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_parity_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_parity_2.value[1]['None'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### parity none > odd
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_parity_1, ConfigROI.s_parity_2],
			except_addr=ConfigMap.addr_parity,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_parity_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_parity_2.value[1]['Odd'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### parity odd > even
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_parity_1, ConfigROI.s_parity_2],
			except_addr=ConfigMap.addr_parity,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_parity_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_parity_2.value[1]['Even'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### stop bit 1 > 2
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_stop_bit_1, ConfigROI.s_stop_bit_2],
			except_addr=ConfigMap.addr_stop_bit,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_stop_bit_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_stop_bit_2.value[1]['2'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### stop bit 2 > 1
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_stop_bit_1, ConfigROI.s_stop_bit_2],
			except_addr=ConfigMap.addr_stop_bit,
			access_address=ConfigMap.addr_rs485_setup_access.value,
			setup_answer_key=list(ConfigROI.s_stop_bit_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_stop_bit_2.value[1]['1'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)

	def m_s_network_advanced(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### modbus timeout 600 > 5
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_3.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='4',
			apply_btn=True,
			roi_keys=[ConfigROI.s_modbus_timeout_1, ConfigROI.s_modbus_timeout_2],
			except_addr=ConfigMap.addr_modbus_timeout,
			access_address=ConfigMap.addr_modbus_timeout_setup_access.value,
			setup_answer_key=ConfigROI.s_modbus_timeout_2.value[1][0],
			modbus_answer_key=ConfigROI.s_modbus_timeout_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### modbus timeout 5 > 600
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='601',
			apply_btn=True,
			roi_keys=[ConfigROI.s_modbus_timeout_1, ConfigROI.s_modbus_timeout_2],
			except_addr=ConfigMap.addr_modbus_timeout,
			access_address=ConfigMap.addr_modbus_timeout_setup_access.value,
			setup_answer_key=ConfigROI.s_modbus_timeout_2.value[1][1],
			modbus_answer_key=ConfigROI.s_modbus_timeout_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### rstp Disable > Enable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rstp_1, ConfigROI.s_rstp_2],
			except_addr=ConfigMap.addr_rstp,
			access_address=ConfigMap.addr_rstp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rstp_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_rstp_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### rstp Enable > Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rstp_1, ConfigROI.s_rstp_2],
			except_addr=ConfigMap.addr_rstp,
			access_address=ConfigMap.addr_rstp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rstp_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_rstp_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### storm control Enable > Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_storm_control_1, ConfigROI.s_storm_control_2],
			except_addr=ConfigMap.addr_storm_control,
			access_address=ConfigMap.addr_storm_control_setup_access.value,
			setup_answer_key=list(ConfigROI.s_storm_control_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_storm_control_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### storm control Disable > Enable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_storm_control_1, ConfigROI.s_storm_control_2],
			except_addr=ConfigMap.addr_storm_control,
			access_address=ConfigMap.addr_storm_control_setup_access.value,
			setup_answer_key=list(ConfigROI.s_storm_control_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_storm_control_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### rs485 map 7300 map > 7500 map
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rs485_map_1, ConfigROI.s_rs485_map_2],
			except_addr=ConfigMap.addr_rs485_map,
			access_address=ConfigMap.addr_rs485_map_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rs485_map_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_rs485_map_2.value[1]['Accura 7500'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### rs485 map 7500 map > 7300 map
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_rs485_map_1, ConfigROI.s_rs485_map_2],
			except_addr=ConfigMap.addr_rs485_map,
			access_address=ConfigMap.addr_rs485_map_setup_access.value,
			setup_answer_key=list(ConfigROI.s_rs485_map_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_rs485_map_2.value[1]['Accura 7300'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### remote control lock mode / each > always
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_remote_control_lock_mode_1, ConfigROI.s_remote_control_lock_mode_2],
			except_addr=ConfigMap.addr_remote_control_lock_mode,
			access_address=ConfigMap.addr_remote_control_lock_mode_access.value,
			setup_answer_key=list(ConfigROI.s_remote_control_lock_mode_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_remote_control_lock_mode_2.value[1]['Always Unlock'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### remote control lock mode / always > each
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value, 
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_remote_control_lock_mode_1, ConfigROI.s_remote_control_lock_mode_2],
			except_addr=ConfigMap.addr_remote_control_lock_mode,
			access_address=ConfigMap.addr_remote_control_lock_mode_access.value,
			setup_answer_key=list(ConfigROI.s_remote_control_lock_mode_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_remote_control_lock_mode_2.value[1]['Each Connection Lock'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_max.value,
			roi_mask=ConfigROI.mask_m_s_meas_wiring.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
	def m_s_control_test_mode(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### test mode off > balance
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_4.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_wide_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Balance'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### test mode balance > unbalance
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Unbalance'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### test mode unbalance > dip short
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_7.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Dip Short'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### test mode dip short > dip long
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_9.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Dip Long'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### test mode dip long > swell short
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_11.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[5],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Swell Short'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### test mode dip long > swell long
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_test_mode_1, ConfigROI.s_test_mode_2],
			except_addr=ConfigMap.addr_meter_test_mode,
			access_address=None,
			setup_answer_key=list(ConfigROI.s_test_mode_2.value[1])[6],
			modbus_answer_key=ConfigROI.s_test_mode_2.value[1]['Swell Long'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(None, ConfigMap.addr_meter_test_mode, bit16=0)
		
		### timeout 60 > 1
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys=[ConfigROI.s_test_mode_timeout_1, ConfigROI.s_test_mode_timeout_2]
		except_addr = ConfigMap.addr_meter_demo_mode_timeout
		setup_answer_key = roi_keys[1].value[1][1]
		eval_type=SelectType.type_integer.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_meter_demo_mode_timeout_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)

		### timeout 1 > 0(Infinite)
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys=[ConfigROI.s_test_mode_timeout_1, ConfigROI.s_test_mode_timeout_2]
		except_addr = ConfigMap.addr_meter_demo_mode_timeout
		setup_answer_key = roi_keys[1].value[1][0]
		eval_type=SelectType.type_integer.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_meter_demo_mode_timeout_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)
		
		### timeout 0(Infinite) > 1440
		self.touch_manager.touch_menu(ConfigTouch.touch_data_view_2.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_ref_curr.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_1.value)
		for i in range(2):
			self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_4.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_num_0.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_tdd_enter.value)
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_apply.value)
		roi_keys=[ConfigROI.s_test_mode_timeout_1, ConfigROI.s_test_mode_timeout_2]
		except_addr = ConfigMap.addr_meter_demo_mode_timeout
		setup_answer_key = roi_keys[1].value[1][2]
		eval_type=SelectType.type_integer.value
		modbus_ref = setup_answer_key
		template_path = ConfigImgRef.img_ref_meter_setup_meas_exc.value
		roi_mask = ConfigROI.mask_m_s_meas_tdd_nominal_curr.value
		self.setup_ocr_process(base_save_path, search_pattern, roi_keys, except_addr, access_address=ConfigMap.addr_meter_demo_mode_timeout_setup_access.value, setup_answer_key=setup_answer_key, eval_type=eval_type, modbus_ref=modbus_ref, template_path=template_path, roi_mask=roi_mask)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_meter_demo_mode_timeout_setup_access, ConfigMap.addr_meter_demo_mode_timeout, bit16=60)

	def m_s_system_description(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### installation year 1970 > 9999
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=True,
			popup_btn=None,
			number_input='9999',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_year_1, ConfigROI.s_installation_year_2],
			except_addr=ConfigMap.addr_installation_year,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_year_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_installation_year_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### installation year 9999 > 1970
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='1969',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_year_1, ConfigROI.s_installation_year_2],
			except_addr=ConfigMap.addr_installation_year,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_year_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_installation_year_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### installation month 1 > 12
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='13',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_month_1, ConfigROI.s_installation_month_2],
			except_addr=ConfigMap.addr_installation_month,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_month_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_installation_month_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### installation month 12 > 1
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_month_1, ConfigROI.s_installation_month_2],
			except_addr=ConfigMap.addr_installation_month,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_month_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_installation_month_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### installation day 1 > 31
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=None,
			popup_btn=None,
			number_input='32',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_day_1, ConfigROI.s_installation_day_2],
			except_addr=ConfigMap.addr_installation_day,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_day_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_installation_day_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### installation day 31 > 1
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_installation_day_1, ConfigROI.s_installation_day_2],
			except_addr=ConfigMap.addr_installation_day,
			access_address=ConfigMap.addr_description_setup_access.value,
			setup_answer_key=list(ConfigROI.s_installation_day_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_installation_day_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
	def m_s_system_locale(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### timezone offset [min] 540 > -720
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_2.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='-721',
			apply_btn=True,
			roi_keys=[ConfigROI.s_timezone_offset_1, ConfigROI.s_timezone_offset_2],
			except_addr=ConfigMap.addr_timezone_offset,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_timezone_offset_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_timezone_offset_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### timezone offset [min] -720 > 840
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='840',
			apply_btn=True,
			roi_keys=[ConfigROI.s_timezone_offset_1, ConfigROI.s_timezone_offset_2],
			except_addr=ConfigMap.addr_timezone_offset,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_timezone_offset_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_timezone_offset_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_locale_setup_access, ConfigMap.addr_timezone_offset, bit16=540)
		
		### temperature unit celsius > fahrenheit
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_temperature_unit_1, ConfigROI.s_temperature_unit_2],
			except_addr=ConfigMap.addr_temperature_unit,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_temperature_unit_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_temperature_unit_2.value[1]['Fahrenheit'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### temperature unit fahrenheit > celsius
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_temperature_unit_1, ConfigROI.s_temperature_unit_2],
			except_addr=ConfigMap.addr_temperature_unit,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_temperature_unit_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_temperature_unit_2.value[1]['Celsius'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Energy unit kWh > Wh
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_energy_unit_1, ConfigROI.s_energy_unit_2],
			except_addr=ConfigMap.addr_energy_unit,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_energy_unit_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_energy_unit_2.value[1]['Wh'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Energy unit Wh > kWh
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_energy_unit_1, ConfigROI.s_energy_unit_2],
			except_addr=ConfigMap.addr_energy_unit,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_energy_unit_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_energy_unit_2.value[1]['kWh'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format yyyy-mm-dd > yyyy-dd-mm
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['YYYY-DD-MM'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format yyyy-dd-mm > yyyy/dd/mm
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['YYYY/DD/MM'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format yyyy/dd/mm > mm.dd.yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_7.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['MM.DD.YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format mm.dd.yyyy > mm/dd/yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_9.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['MM/DD/YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format mm/dd/yyyy > mm-dd-yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_11.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[5],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['MM-DD-YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format mm-dd-yyyy > dd.mm.yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[6],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['DD.MM.YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format dd.mm.yyyy > dd/mm/yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_4.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[7],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['DD/MM/YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format dd/mm/yyyy > dd-mm-yyyy
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_6.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[8],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['DD-MM-YYYY'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### date format dd-mm-yyyy > yyyy-mm-dd 
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_date_format_1, ConfigROI.s_date_format_2],
			except_addr=ConfigMap.addr_date_display_format,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_date_format_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_date_format_2.value[1]['YYYY-MM-DD'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		

	def m_s_system_local_time(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### local time  540 > -720   --- 주소를 모름
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_3.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='1999',
			apply_btn=True,
			roi_keys=[ConfigROI.s_year_1, ConfigROI.s_year_2],
			except_addr=ConfigMap.addr_locale_setup_access,
			access_address=ConfigMap.addr_locale_setup_access.value,
			setup_answer_key=list(ConfigROI.s_timezone_offset_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_timezone_offset_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
	def m_s_system_summer_time(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		## summer time disable > enable
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_4.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_summer_time_mode_1, ConfigROI.s_summer_time_mode_2],
			except_addr=ConfigMap.addr_summer_time,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_summer_time_mode_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_summer_time_mode_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### summer time enable > disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_summer_time_mode_1, ConfigROI.s_summer_time_mode_2],
			except_addr=ConfigMap.addr_summer_time,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_summer_time_mode_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_summer_time_mode_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### time offset 60 > 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_summer_time_time_offset_1, ConfigROI.s_summer_time_time_offset_2],
			except_addr=ConfigMap.addr_summer_time_offset,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_summer_time_time_offset_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_summer_time_time_offset_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### time offset 0 > 1439
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='1440',
			apply_btn=True,
			roi_keys=[ConfigROI.s_summer_time_time_offset_1, ConfigROI.s_summer_time_time_offset_2],
			except_addr=ConfigMap.addr_summer_time_offset,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_summer_time_time_offset_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_summer_time_time_offset_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_summer_time_setup_access, ConfigMap.addr_summer_time_offset, bit16=60)

		####### Summer Time / Start Month 
		key_options = ConfigROI.s_start_month_2.value[1]
		key_sequence = list(key_options.keys())
		popup_numbers = [1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 12]

		# 주석에 표시될 'from' 월 시퀀스
		log_source_sequence = ['March'] + key_sequence[:-1]  # ['March', 'January', 'February', ...]

		for i, (from_key, popup_num) in enumerate(zip(log_source_sequence, popup_numbers)):
			to_key = key_sequence[i] 

			print(f"### Summer Time / Start Month {from_key} > {to_key}")

			popup_btn_name = f'touch_btn_popup_wide_{popup_num}'
			popup_btn_value = getattr(ConfigTouch, popup_btn_name).value

			# 공통 함수 호출
			self.config_setup_action(
				main_menu=None,
				side_menu=None,
				data_view=ConfigTouch.touch_data_view_3.value,
				password=None,
				popup_btn=popup_btn_value,  # 동적으로 설정된 값
				number_input=None,
				apply_btn=True,
				roi_keys=[ConfigROI.s_start_month_1, ConfigROI.s_start_month_2],
				except_addr=ConfigMap.addr_start_month,
				access_address=ConfigMap.addr_summer_time_setup_access.value,
				setup_answer_key=to_key,  # list(month_options)[i]와 동일
				modbus_answer_key=key_options[to_key], # 딕셔너리에서 월 이름으로 값 조회
				eval_type=SelectType.type_selection.value,
				modbus_unit=None,
				template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
				roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
				search_pattern=search_pattern,
				base_save_path=base_save_path
			)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_summer_time_setup_access, ConfigMap.addr_start_month, bit16=3)
		############

		### start nth weekday 2nd > 3rd
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_nth_weekday_1, ConfigROI.s_start_nth_weekday_2],
			except_addr=ConfigMap.addr_start_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_nth_weekday_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_start_nth_weekday_2.value[1]['3rd'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start nth weekday 3rd > 4th
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_4.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_nth_weekday_1, ConfigROI.s_start_nth_weekday_2],
			except_addr=ConfigMap.addr_start_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_nth_weekday_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_start_nth_weekday_2.value[1]['4th'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start nth weekday 4th > 5th
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_nth_weekday_1, ConfigROI.s_start_nth_weekday_2],
			except_addr=ConfigMap.addr_start_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_nth_weekday_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_start_nth_weekday_2.value[1]['5th'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start nth weekday 5th > 1st
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_nth_weekday_1, ConfigROI.s_start_nth_weekday_2],
			except_addr=ConfigMap.addr_start_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_nth_weekday_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_start_nth_weekday_2.value[1]['1st'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start nth weekday 1st > 2nd
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_nth_weekday_1, ConfigROI.s_start_nth_weekday_2],
			except_addr=ConfigMap.addr_start_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_nth_weekday_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_start_nth_weekday_2.value[1]['2nd'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Sunday > Monday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Monday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Monday > Tuesday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Tuesday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Tuesday > Wednesday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_7.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Wednesday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Wednesday > Thursday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_9.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Thursday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Thursday > Friday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_11.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[5],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Friday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Friday > Saturday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[6],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Saturday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start weekday Saturday > Sunday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_5.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_weekday_1, ConfigROI.s_start_weekday_2],
			except_addr=ConfigMap.addr_start_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_weekday_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_start_weekday_2.value[1]['Sunday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start minute 120 > 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_minute_1, ConfigROI.s_start_minute_2],
			except_addr=ConfigMap.addr_start_minute,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_minute_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_start_minute_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### start minute 0 > 1439
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_6.value,
			password=None,
			popup_btn=None,
			number_input='1440',
			apply_btn=True,
			roi_keys=[ConfigROI.s_start_minute_1, ConfigROI.s_start_minute_2],
			except_addr=ConfigMap.addr_start_minute,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_start_minute_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_start_minute_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_summer_time_setup_access, ConfigMap.addr_start_minute, bit16=120)
		
		####### Summer Time / End Month 
		key_options = ConfigROI.s_end_month_2.value[1]
		key_sequence = list(key_options.keys())
		popup_numbers = [1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 12]

		# 주석에 표시될 'from' 월 시퀀스
		log_source_sequence = ['March'] + key_sequence[:-1]  # ['March', 'January', 'February', ...]

		for i, (from_key, popup_num) in enumerate(zip(log_source_sequence, popup_numbers)):
			to_key = key_sequence[i] 

			print(f"### Summer Time / Start Month {from_key} > {to_key}")

			popup_btn_name = f'touch_btn_popup_wide_{popup_num}'
			popup_btn_value = getattr(ConfigTouch, popup_btn_name).value

			# 공통 함수 호출
			self.config_setup_action(
				main_menu=None,
				side_menu=None,
				data_view=ConfigTouch.touch_data_view_7.value,
				password=None,
				popup_btn=popup_btn_value,  # 동적으로 설정된 값
				number_input=None,
				apply_btn=True,
				roi_keys=[ConfigROI.s_end_month_1, ConfigROI.s_end_month_2],
				except_addr=ConfigMap.addr_end_month,
				access_address=ConfigMap.addr_summer_time_setup_access.value,
				setup_answer_key=to_key,  # list(month_options)[i]와 동일
				modbus_answer_key=key_options[to_key], # 딕셔너리에서 월 이름으로 값 조회
				eval_type=SelectType.type_selection.value,
				modbus_unit=None,
				template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
				roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
				search_pattern=search_pattern,
				base_save_path=base_save_path
			)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_summer_time_setup_access, ConfigMap.addr_end_month, bit16=11)
		############

		### end nth weekday 1st > 2nd
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_8.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_nth_weekday_1, ConfigROI.s_end_nth_weekday_2],
			except_addr=ConfigMap.addr_end_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_nth_weekday_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_end_nth_weekday_2.value[1]['2nd'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end nth weekday 2nd > 3rd
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_8.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_nth_weekday_1, ConfigROI.s_end_nth_weekday_2],
			except_addr=ConfigMap.addr_end_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_nth_weekday_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_end_nth_weekday_2.value[1]['3rd'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end nth weekday 3rd > 4th
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_8.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_4.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_nth_weekday_1, ConfigROI.s_end_nth_weekday_2],
			except_addr=ConfigMap.addr_end_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_nth_weekday_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_end_nth_weekday_2.value[1]['4th'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end nth weekday 4th > 5th
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_8.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_nth_weekday_1, ConfigROI.s_end_nth_weekday_2],
			except_addr=ConfigMap.addr_end_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_nth_weekday_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_end_nth_weekday_2.value[1]['5th'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end nth weekday 5th > 1st
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_8.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_nth_weekday_1, ConfigROI.s_end_nth_weekday_2],
			except_addr=ConfigMap.addr_end_nth_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_nth_weekday_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_end_nth_weekday_2.value[1]['1st'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Sunday > Monday
		self.touch_manager.touch_menu(ConfigTouch.touch_btn_scroll_down.value)
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Monday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Monday > Tuesday 
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_5.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Tuesday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Tuesday > Wednesday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_7.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[3],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Wednesday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Wednesday > Thursday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_9.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[4],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Thursday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Thursday > Friday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_11.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[5],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Friday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Friday > Saturday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[6],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Saturday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end weekday Saturday > Sunday
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_wide_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_weekday_1, ConfigROI.s_end_weekday_2],
			except_addr=ConfigMap.addr_end_weekday,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_weekday_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_end_weekday_2.value[1]['Sunday'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end minute 120 > 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_minute_1, ConfigROI.s_end_minute_2],
			except_addr=ConfigMap.addr_end_minute,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_minute_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_end_minute_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### end minute 0 > 1439
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='1440',
			apply_btn=True,
			roi_keys=[ConfigROI.s_end_minute_1, ConfigROI.s_end_minute_2],
			except_addr=ConfigMap.addr_end_minute,
			access_address=ConfigMap.addr_summer_time_setup_access.value,
			setup_answer_key=list(ConfigROI.s_end_minute_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_end_minute_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_summer_time_setup_access, ConfigMap.addr_end_minute, bit16=120)
		
	def m_s_system_ntp(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### Sync Mode Auto > Periodic
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_5.value,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=True,
			popup_btn=ConfigTouch.touch_btn_popup_3.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_mode_1, ConfigROI.s_sync_mode_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_sync_mode,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_mode_2.value[1])[2],
			modbus_answer_key=ConfigROI.s_sync_mode_2.value[1]['Periodic'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sync Mode Periodic > Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_mode_1, ConfigROI.s_sync_mode_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_sync_mode,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_mode_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_sync_mode_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sync Mode Disable > Auto
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_mode_1, ConfigROI.s_sync_mode_2],
			compare_exc=1,
			except_addr=ConfigMap.addr_sync_mode,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_mode_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_sync_mode_2.value[1]['Auto'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sync Period 600 > 60
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='59',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_period_1, ConfigROI.s_sync_period_2],
			except_addr=ConfigMap.addr_sync_period,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_period_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_sync_period_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sync Period 60 > 999
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=None,
			number_input='999',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_period_1, ConfigROI.s_sync_period_2],
			except_addr=ConfigMap.addr_sync_period,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_period_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_sync_period_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_ntp_setup_access, ConfigMap.addr_sync_period, bit16=600)
		
		### Sync MAx. Drift 1 > 1001
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='1001',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_max_drift_1, ConfigROI.s_sync_max_drift_2],
			except_addr=ConfigMap.addr_sync_max_drift,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_max_drift_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_sync_max_drift_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### Sync MAx. Drift 1000 > 1
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_4.value,
			password=None,
			popup_btn=None,
			number_input='1',
			apply_btn=True,
			roi_keys=[ConfigROI.s_sync_max_drift_1, ConfigROI.s_sync_max_drift_2],
			except_addr=ConfigMap.addr_sync_max_drift,
			access_address=ConfigMap.addr_ntp_setup_access.value,
			setup_answer_key=list(ConfigROI.s_sync_max_drift_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_sync_max_drift_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
	def m_s_system_lcd_buzzer(self, base_save_path, search_pattern):
		### 모두 AccuraSR은 변경해야됨
		self.touch_manager.uitest_mode_start() 
		
		self.touch_manager.btn_front_meter()
		self.touch_manager.btn_front_home()
		self.touch_manager.btn_front_setup()

		### lcd backlight timeout 300 > 999
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_5.value,
			side_menu=ConfigTouch.touch_side_menu_6.value,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=True,
			popup_btn=None,
			number_input='1001',
			apply_btn=True,
			roi_keys=[ConfigROI.s_lcd_backlight_timeout_1, ConfigROI.s_lcd_backlight_timeout_2],
			except_addr=ConfigMap.addr_lcd_backlight_timeout,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_lcd_backlight_timeout_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_lcd_backlight_timeout_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### lcd backlight timeout 999 > 10
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_1.value,
			password=None,
			popup_btn=None,
			number_input='9',
			apply_btn=True,
			roi_keys=[ConfigROI.s_lcd_backlight_timeout_1, ConfigROI.s_lcd_backlight_timeout_2],
			except_addr=ConfigMap.addr_lcd_backlight_timeout,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_lcd_backlight_timeout_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_lcd_backlight_timeout_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_lcd_buzzer_setup_access, ConfigMap.addr_lcd_backlight_timeout, bit16=300)

		### lcd backlight low level 10 > 30
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='31',
			apply_btn=True,
			roi_keys=[ConfigROI.s_lcd_backlight_low_level_1, ConfigROI.s_lcd_backlight_low_level_2],
			except_addr=ConfigMap.addr_lcd_backlight_low_level,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_lcd_backlight_low_level_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_lcd_backlight_low_level_2.value[1][1],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### lcd backlight low level 30 > 0
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_2.value,
			password=None,
			popup_btn=None,
			number_input='0',
			apply_btn=True,
			roi_keys=[ConfigROI.s_lcd_backlight_low_level_1, ConfigROI.s_lcd_backlight_low_level_2],
			except_addr=ConfigMap.addr_lcd_backlight_low_level,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_lcd_backlight_low_level_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_lcd_backlight_low_level_2.value[1][0],
			eval_type=SelectType.type_integer.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		self.modbus_label.setup_target_initialize(ConfigMap.addr_lcd_buzzer_setup_access, ConfigMap.addr_lcd_backlight_low_level, bit16=10)

		### buzzer for button Enable > Disable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_1.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_buzzer_for_button_1, ConfigROI.s_buzzer_for_button_2],
			except_addr=ConfigMap.addr_buzzer_for_button,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_buzzer_for_button_2.value[1])[0],
			modbus_answer_key=ConfigROI.s_buzzer_for_button_2.value[1]['Disable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)
		
		### buzzer for button Disable > Enable
		self.config_setup_action(
			main_menu=None,
			side_menu=None,
			data_view=ConfigTouch.touch_data_view_3.value,
			password=None,
			popup_btn=ConfigTouch.touch_btn_popup_2.value,
			number_input=None,
			apply_btn=True,
			roi_keys=[ConfigROI.s_buzzer_for_button_1, ConfigROI.s_buzzer_for_button_2],
			except_addr=ConfigMap.addr_buzzer_for_button,
			access_address=ConfigMap.addr_lcd_buzzer_setup_access.value,
			setup_answer_key=list(ConfigROI.s_buzzer_for_button_2.value[1])[1],
			modbus_answer_key=ConfigROI.s_buzzer_for_button_2.value[1]['Enable'],
			eval_type=SelectType.type_selection.value,
			modbus_unit=None,
			template_path=ConfigImgRef.img_ref_meter_setup_meas_min.value,
			roi_mask=ConfigROI.mask_m_s_meas_min_meas_secondary_vol.value,
			search_pattern=search_pattern,
			base_save_path=base_save_path)