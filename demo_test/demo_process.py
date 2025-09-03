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

	def meter_demo_test_balance(self, base_save_path, search_pattern):
		self.touch_manager.uitest_mode_start()

		self.touch_manager.btn_front_meter()
		
        ###

		### wiring -> Delta
		self.config_setup_action(
			main_menu=ConfigTouch.touch_main_menu_1.value,
			side_menu=ConfigTouch.touch_side_menu_1.value,
			data_view=None,
			password=None,
			popup_btn=None, 
			number_input=None,
			apply_btn=None,
			roi_keys=[ConfigROI.m_curr_rms_title],
			except_addr=None,
			access_address=None,
			setup_answer_key=None,
			modbus_answer_key=None,
			eval_type=None,
			modbus_unit=None,
			template_path=None,
			roi_mask=None,
			search_pattern=search_pattern,
			base_save_path=base_save_path)