import cv2
import numpy as np
import pyautogui
import time
import os
from function.func_modbus import ConnectionManager
from config.config_ref import ConfigImgRef

### 배율 100% 아닐시 동작 및 이미지 매칭 오류발생

class AutoGUI:

	connect_manager = ConnectionManager()

	def find_and_click(self, template_path, img_path, base_save_path, title, roi_mask=None, coordinates=None, save_statue=1, click=0):
		self.sm_condition = False
		
		file_name_with_extension = os.path.basename(img_path)  
		ip_to_remove = f"{self.connect_manager.SERVER_IP}_"    
		if file_name_with_extension.startswith(ip_to_remove):
			file_name_without_ip = file_name_with_extension[len(ip_to_remove):]
		else:
			file_name_without_ip = file_name_with_extension

		# 확장자 제거
		image_file_name = os.path.splitext(file_name_without_ip)[0]
		save_path = os.path.join(base_save_path, f'{image_file_name}_{title}.png')
		dest_image_path = os.path.join(base_save_path, file_name_without_ip)

		screenshot_pil = pyautogui.screenshot()
		screenshot = cv2.cvtColor(np.array(screenshot_pil), cv2.COLOR_RGB2BGR)
	
		template_full = cv2.imread(template_path, cv2.IMREAD_COLOR)
		if template_full is None:
			print(f"Failed to load template: {template_path}")
			return None, False
		
		if roi_mask is not None:
			x1, y1, x2, y2 = roi_mask
			# 좌표 보정 (0보다 작으면 0, 원본보다 크면 원본 크기로)
			h_full, w_full = template_full.shape[:2]
			x1, y1 = max(0, x1), max(0, y1)
			x2, y2 = min(w_full, x2), min(h_full, y2)

			# crop된 템플릿
			template = template_full[y1:y2, x1:x2]
	
		else:
			# template = cv2.imread(template_path, cv2.IMREAD_COLOR)
			# h, w, _ = template.shape
			template = template_full
			pass
		
		h, w = template.shape[:2]
		if h == 0 or w == 0:
			print("Cropped template is empty. Check roi_mask coordinates.")
			return None, False
		result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

		threshold = 0.95
		top_left = max_loc
		if max_val >= threshold and coordinates:
			w_1, h_1 = coordinates
			center_x = top_left[0] + w_1*w
			center_y = top_left[1] + h_1*h

			pyautogui.moveTo(center_x, center_y, duration=0.5)
			time.sleep(1)
			box_width, box_height = w, h
			screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
			if save_statue == 1:
				screenshot_region.save(save_path)
			else:
				pass
			pyautogui.click()
			sm_res = None

		else:
			box_width, box_height = w, h
			screenshot_region = pyautogui.screenshot(region=(top_left[0], top_left[1], box_width, box_height))
			screenshot_region.save(save_path)

			if max_val >= threshold:
				sm_res = f'PASS_{max_val:.3f}'
				sm_res_raw = f'PASS_{max_val:.3f}_{title}'
				self.sm_condition = True
			else:
				sm_res = f'FAIL_{max_val:.3f}'
				sm_res_raw = f'FAIL_{max_val:.3f}_{title}'

		# print(sm_res_raw)
			
		return sm_res, self.sm_condition
	
	def template_mask(self, template_path, roi_mask):
		x1, y1, x2, y2 = [*roi_mask]
		template = cv2.imread(template_path, cv2.IMREAD_COLOR)
		h, w = template.shape[:2]

		x1, y1 = max(0, x1), max(0, y1)
		x2, y2 = min(w, x2), min(h, y2)
		cropped_template = template[y1:y2, x1:x2]

		# mask = np.ones(template.shape[:2], dtype=np.uint8) * 255  # 255=사용, 0=무시
		# mask_result = cv2.rectangle(mask, (x1, y1), (x2, y2), 0, -1)
		return cropped_template

	def m_s_meas_refresh(self, img_path, base_save_path, title):
		template_path = ConfigImgRef.img_ref_meas_refresh.value
		coordinates = [0.93, 0.98]
		self.find_and_click(template_path, img_path, base_save_path, title, coordinates=coordinates, save_statue=0, click=1)
	
	def m_s_event_refresh(self, img_path, base_save_path, title):
		template_path = ConfigImgRef.img_ref_meter_setup_event_max.value
		coordinates = [0.93, 0.98]
		self.find_and_click(template_path, img_path, base_save_path, title, coordinates=coordinates, save_statue=0, click=1)


