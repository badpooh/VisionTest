from enum import Enum

class ConfigColor(Enum):
	
	color_main_menu_vol = [10, 70, 10, 10, 67, 136, 255]
	color_main_menu_curr = [170, 70, 10, 10, 67, 136, 255]
	color_rms_vol_ll = [380, 140, 10, 10, 67, 136, 255]
	color_rms_vol_ln = [480, 140, 10, 10, 67, 136, 255]
	color_vol_thd_ll = [480, 140, 10, 10, 67, 136, 255]
	color_vol_thd_ln = [580, 140, 10, 10, 67, 136, 255]
	color_phasor_vll = [580, 200, 10, 10, 67, 136, 255]
	color_phasor_vln = [680, 200, 10, 10, 67, 136, 255]
	color_symm_thd_vol_ll = [480, 140, 10, 10, 67, 136, 255]
	color_symm_thd_vol_ln = [580, 140, 10, 10, 67, 136, 255]
	### A상 버튼 눌러서 A상이 안보이는 지 확인 / 앞 4자리는 검사할 그래프 영역###
	### 뒤 3자리는 RGB ###
	color_waveform_vol_a = [313, 253, 411, 203, 0, 0, 0]
	color_waveform_vol_b = [313, 253, 411, 203, 255, 29, 37]
	color_waveform_vol_c = [313, 253, 411, 203, 0, 0, 255]
	color_waveform_curr_a = [313, 253, 411, 203, 153, 153, 153]
	color_waveform_curr_b = [313, 253, 411, 203, 255, 180, 245]
	color_waveform_curr_c = [313, 253, 411, 203, 54, 175, 255]
	color_harmonics_vol_a = [313, 283, 455, 173, 0, 0, 0]
	color_harmonics_vol_b = [313, 283, 455, 173, 255, 29, 37]
	color_harmonics_vol_c = [313, 283, 455, 173, 0, 0, 255]
	color_harmonics_curr_a = [313, 283, 455, 173, 153, 153, 153]
	color_harmonics_curr_b = [313, 283, 455, 173, 255, 180, 245]
	color_harmonics_curr_c = [313, 283, 455, 173, 54, 175, 255]

	### harmonics voltage, current 활성화 판별 ###
	### 앞 4자리는 색판별 영역 / 뒤 3자리는 RGB ###
	color_harmonics_vol = [540, 140, 10, 10, 67, 136, 255]
	color_harmonics_curr = [660, 140, 10, 10, 67, 136, 255]