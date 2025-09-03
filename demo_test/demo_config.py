
from types import coroutine
from enum import Enum


class ConfigROI(Enum):
    title_view = ["RMS Voltage L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    a_ab = "meas_a_phase_name"
    a_time_stamp = "meas_a_time_stamp"
    a_meas = "meas_a_measurement_value"
    b_bc = "meas_b_phase_name"
    b_time_stamp = "meas_b_time_stamp"
    b_meas = "meas_b_measurement_value"
    c_ca = "meas_c_phase_name"
    c_time_stamp = "meas_c_time_stamp"
    c_meas = "meas_c_measurement_value"
    aver = "meas_aver_phase_name"
    aver_time_stamp = "meas_aver_time_stamp"
    aver_meas = "meas_aver_measurement_value"
    curr_per_a = "meas_curr_percent_a"
    curr_per_b = "meas_curr_percent_b"
    curr_per_c = "meas_curr_percent_c"
    curr_per_aver = "meas_curr_percent_aver"
    
    phasor_img_cut = "phasor_img_cut"
    phasor_title = "phasor_title"
    phasor_title_2 = "phasor_title_2"
    phasor_view_2 = "phasor_view_2"
    phasor_vl_vn = "phasor_vl_vn"
    phasor_voltage = "phasor_voltage"
    phasor_a_c_vol = "phasor_a_c_vol"
    phasor_a_meas = "phasor_a_meas"
    phasor_a_angle = "phasor_a_angle"
    phasor_b_meas = "phasor_b_meas"
    phasor_b_angle = "phasor_b_angle"
    phasor_c_meas = "phasor_c_meas"
    phasor_c_angle = "phasor_c_angle"
    phasor_a_c_angle_vol = "phasor_a_c_angle_vol"
    phasor_current = "phasor_current"
    phasor_a_c_cur = "phasor_a_c_cur"
    phasor_a_meas_cur = "phasor_a_meas_cur"
    phasor_a_angle_cur = "phasor_a_angle_cur"
    phasor_b_meas_cur = "phasor_b_meas_cur"
    phasor_b_angle_cur = "phasor_b_angle_cur"
    phasor_c_meas_cur = "phasor_c_meas_cur"
    phasor_c_angle_cur = "phasor_c_angle_cur"
    phasor_a_c_angle_cur = "phasor_a_c_angle_cur"
    
    waveform_title = "waveform_title"
    waveform_all_img_cut = "waveform_img_cut"
    waveform_graph_img_cut = "waveform_graph_img_cut"
    
    harmonics_img_cut = "harmonics_img_cut"
    harmonics_title = "harmonics_title"
    harmonics_sub_title_1 = "harmonics_sub_title_1"
    harmonics_sub_title_2 = "harmonics_sub_title_2"
    harmonics_sub_title_3 = "harmonics_sub_title_3"
    harmonics_graph_img_cut = "harmonics_graph_img_cut"
    harmonics_chart_img_cut = "harmonics_graph_with_bar_img_cut"
    harmonics_graph_a = "harmonics_graph_a"
    harmonics_graph_b = "harmonics_graph_b"
    harmonics_graph_c = "harmonics_graph_c"
    harmonics_text_title = "harmonics_text_title"
    harmonics_text_img = "harmonics_text_image"
    harmonics_text_number_title_1 = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
    harmonics_text_number_meas_1 = "measurement result"
    harmonics_text_chart_img_cut_3 = ["6, 0.000, 15, 0.000, 24, 0.000, 33, 0.000, 42, 0.000, 7, 0.000, 16, 0.000, 25, 0.000, 34, 0.000, 43, 0.000, 8, 0.000, 17, 0.000, 26, 0.000, 35, 0.000, 44, 0.000"]
    harmonics_text_sub_title = "harmonics_text_sub_title"
    harmonics_text_sub_abc = "harmonics_text_sub_a"
    harmonics_thd_a = "harmonics_thd_a"
    harmonics_thd_b = "harmonics_thd_b"
    harmonics_thd_c = "harmonics_thd_c"
    harmonics_fund_a = "harmonics_fund_a"
    harmonics_fund_b = "harmonics_fund_b"
    harmonics_fund_c = "harmonics_fund_c"


    
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

class ConfigTextRef(Enum):
    rms_vol_ll =  ["RMS Voltage L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    rms_vol_ln = ["RMS Voltage L-L L-N Min Max", "A", "B", "C", "Average"]
    fund_vol_ll = ["Fund. Volt. L-L L-N Min Max", "AB", "BC", "CA", "Average"]
    fund_vol_ln = ["Fund. Volt. L-L L-N Min Max", "A", "B", "C", "Average"]
    thd_vol_ll = ["Total Harmonic Distortion L-L L-N Max", "AB", "BC", "CA"]
    thd_vol_ln = ["Total Harmonic Distortion L-L L-N Max", "A", "B", "C"]
    freq = ["Frequency Min Max", "Frequency"]
    residual_vol = ["Residual Voltage Min Max", "RMS", "Fund."]
    rms_curr = ["RMS Current Min Max", "A", "B", "C", "Average"]
    fund_curr = ["Fundamental Current Min Max", "A", "B", "C", "Average"]
    thd_curr = ["Total Harmonic Distortion Max", "A", "B", "C"]
    tdd_curr = ["Total Demand Distortion Max", "A", "B", "C"]
    cf_curr = ["Crest Factor Max", "A", "B", "C"]
    kf_curr = ["K-Factor Max", "A", "B", "C"]
    residual_curr = ["Residual Current Min Max", "RMS", "Fund."]
    active = ["Active Power Min Max", "A", "B", "C", "Total"]
    reactive = ["Reactive Power Min Max", "A", "B", "C", "Total"]
    apparent = ["Apparent Power Min Max", "A", "B", "C", "Total"]
    pf = ["Power Factor Min Max", "A", "B", "C", "Total"]
    phasor_ll = ["Phasor", "Voltage", "Current", "VLL", "VLN", "Voltage", "AB", "BC", "CA", "Current", "A", "B", "C"]
    phasor_ln = ["Phasor", "Voltage", "Current", "VLL", "VLN", "Voltage", "A", "B", "C", "Current", "A", "B", "C"]
    harmonics_for_img = ["Harmonics", "Voltage", "Current"]
    harmonics_vol_3p4w = ["Harmonics", "Voltage", "Current", "[v]", "Graph", "Fund.", "THD", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_curr = ["Harmonics", "Voltage", "Current", "[A]", "Graph", "Fund.", "THD", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_per_fund = ["Harmonics", "Voltage", "Current", "[%]Fund", "Graph", "THD", "Fund.", "Fund.", "A", "B", "C", "A", "B", "C"]
    harmonics_per_rms = ["Harmonics", "Voltage", "Current", "[%]RMS", "Graph", "THD", "Fund.", "Fund.", "A", "B", "C", "A", "B", "C"]
    waveform_3p4w = ["Waveform", "Voltage", "Current"]
    symm_vol_ll = ["Volt. Symm. Component L-L L-N Max", "Positive- Sequence", "Negative- Sequence"]
    symm_vol_ln = ["Volt. Symm. Component L-L L-N Max", "Positive- Sequence", "Negative- Sequence", "Zero- Sequence"]
    unbal_vol = ["Voltage Unbalance Max", "NEMA", "NEMA", "Negative- Sequence", "Zero- Sequence"]
    symm_curr = ["Curr. Symm. Component Max", "Positive- Sequence", "Negative- Sequence", "Zero- Sequence"]
    unbal_curr = ["Current Unbalance Max", "NEMA", "Negative- Sequence", "Zero- Sequence"]
    demand_current = ["Demand Current Peak", "A", "B", "C", "Average"]
    harmonics_text = ["Harmonics", "Voltage", "Current", "[v]", "Text", "A", "B", "C"]
    
class ConfigModbusMap(Enum):
    addr_reset_max_min = 12002
    addr_meas_setup_access = 6000
    addr_demand_sync_mode = 6028
    addr_demand_num_of_sub_interval = 6029
    addr_demand_sub_interval_time = 6030
    addr_reset_demand = 12000
    addr_reset_demand_peak = 12001
    addr_demand_sync = 12015
    
    addr_setup_lock = 2900
    addr_control_lock = 2901

class ConfigTouch(Enum):
    touch_main_menu_1 = [100, 85]
    touch_main_menu_2 = [260, 85]
    touch_main_menu_3 = [390, 85]
    touch_main_menu_4 = [560, 85]
    touch_main_menu_5 = [720, 85]
    touch_side_menu_1 = [80, 135]
    touch_side_menu_2 = [80, 180]
    touch_side_menu_3 = [80, 225]
    touch_side_menu_4 = [80, 270]
    touch_side_menu_5 = [80, 315]
    touch_side_menu_6 = [80, 360]
    touch_side_menu_7 = [80, 405]
    touch_side_menu_8 = [80, 450]

    touch_meas_ll = [410, 150]
    touch_meas_ln = [510, 150]
    touch_thd_ll = [520, 150]
    touch_thd_ln = [620, 150]
    touch_max = [720, 150]
    touch_min = [620, 150]
    touch_phasor_vll = [620, 210]
    touch_phasor_vln = [720, 210]
    touch_analysis_vol = [590, 150]
    touch_analysis_curr = [720, 150]
    touch_harmonics_fund = [510, 200]
    touch_harmonics_submenu_1 = [230, 200]
    touch_harmonics_submenu_2 = [360, 200]
    touch_wave_curr_a = [620, 200]
    touch_wave_curr_b = [680, 200]
    touch_wave_curr_c = [740, 200]
    touch_wave_vol_a = [360, 200]
    touch_wave_vol_b = [430, 200]
    touch_wave_vol_c = [490, 200]
    touch_harmonics_sub_v = [230, 240]
    touch_harmonics_sub_fund = [230, 285]
    touch_harmonics_sub_rms = [230, 330]
    touch_harmonics_sub_graph = [360, 240]
    touch_harmonics_sub_text = [360, 285]
    
    #touch_address
    touch_addr_ui_test_mode = 57100
    touch_addr_pos_x = 57110
    touch_addr_pos_y = 57111
    touch_addr_touch_mode = 57112
    touch_addr_screen_capture = 57101
    touch_addr_setup_button_bit = 57120
    touch_addr_setup_button = 57121


class ConfigColor(Enum):
    color_harmonics_vol_a = [313, 253, 411, 203, 0, 0, 0]

class ConfigImgRef(Enum):
    img_ref_phasor_all_vll = r".\image_ref\11.img_ref_phasor_all_vll.png"
    img_ref_phasor_all_vll_none = r".\image_ref\11.img_ref_phasor_all_vll_none.png"
    img_ref_phasor_all_vln = r".\image_ref\12.img_ref_phasor_all_vln.png"
    img_ref_phasor_all_vln_none = r".\image_ref\12.img_ref_phasor_all_vln_none.png"
    img_ref_phasor_vol_vll = r".\image_ref\13.img_ref_phasor_vol_vll.png"
    img_ref_phasor_vol_vll_none = r".\image_ref\13.img_ref_phasor_vol_vll_none.png"
    img_ref_phasor_vol_vln = r".\image_ref\14.img_ref_phasor_vol_vln.png"
    img_ref_phasor_vol_vln_none = r".\image_ref\14.img_ref_phasor_vol_vln_none.png"
    img_ref_phasor_curr_vll = r".\image_ref\15.img_ref_phasor_curr_vll.png"
    img_ref_phasor_curr_vll_none = r".\image_ref\15.img_ref_phasor_curr_vll_none.png"
    img_ref_phasor_curr_vln = r".\image_ref\16.img_ref_phasor_curr_vln.png"
    img_ref_phasor_curr_vln_none = r".\image_ref\16.img_ref_phasor_curr_vln_none.png"
    img_ref_phasor_na_vll = r".\image_ref\17.img_ref_phasor_na_vll.png"
    img_ref_phasor_na_vln = r".\image_ref\17.img_ref_phasor_na_vln.png"
    img_ref_harmonics_vol_3p4w = r".\image_ref\21.img_ref_harmonics_vol_3p4w.png"
    img_ref_harmonics_vol_3p4w_none = r".\image_ref\21.img_ref_harmonics_vol_3p4w_none.png"
    img_ref_harmonics_curr = r".\image_ref\22.img_ref_harmonics_curr.png"
    img_ref_harmonics_curr_none = r".\image_ref\22.img_ref_harmonics_curr_none.png"
    img_ref_harmonics_vol_fund = r".\image_ref\23.img_ref_harmonics_vol_fund.png"
    img_ref_harmonics_vol_fund_none = r".\image_ref\23.img_ref_harmonics_vol_fund_none.png"
    img_ref_harmonics_vol_rms = r".\image_ref\24.img_ref_harmonics_vol_rms.png"
    img_ref_harmonics_vol_rms_none = r".\image_ref\24.img_ref_harmonics_vol_rms_none.png"
    img_ref_harmonics_curr_fund = r".\image_ref\25.img_ref_harmonics_curr_fund.png"
    img_ref_harmonics_curr_fund_none = r".\image_ref\25.img_ref_harmonics_curr_fund_none.png"
    img_ref_harmonics_curr_rms = r".\image_ref\26.img_ref_harmonics_curr_rms.png"
    img_ref_harmonics_curr_rms_none = r".\image_ref\26.img_ref_harmonics_curr_rms_none.png"
    img_ref_waveform_all = r".\image_ref\41.img_ref_waveform_all.png"
    img_ref_waveform_all_none = r".\image_ref\42.img_ref_waveform_all_none.png"

class ConfigSetup():
    def __init__(self, n=3):
        self.n = n

    def update_n(self, new_n):
        self.n = new_n

    def roi_params(self):
        n = self.n
        params = {
            "1": [n*x for x in [176, 181, 298, 35]],
            "2": [n*x for x in [477, 181, 298, 35]],
            "3": [n*x for x in [176, 215, 298, 35]],
            "4": [n*x for x in [477, 215, 298, 35]],
            "5": [n*x for x in [176, 253, 298, 35]],
            "6": [n*x for x in [477, 253, 298, 35]],
            "7": [n*x for x in [176, 287, 298, 35]],
            "8": [n*x for x in [477, 287, 298, 35]],
            "9": [n*x for x in [176, 325, 298, 35]],
            "10": [n*x for x in [477, 325, 298, 35]],
            "11": [n*x for x in [176, 359, 298, 35]],
            "12": [n*x for x in [477, 359, 298, 35]],
            "13": [n*x for x in [176, 397, 298, 35]],
            "14": [n*x for x in [477, 397, 298, 35]],
            "15": [n*x for x in [176, 431, 298, 35]],
            "16": [n*x for x in [477, 431, 298, 35]],
            # popup title ~ popup button(enter, cancel)
            "17": [n*x for x in [250, 20, 300, 55]],
            "18": [n*x for x in [262, 88, 273, 44]],
            "19": [n*x for x in [250, 138, 273, 44]],
            # popup_number title ~ popup button(enter, cancel)
            "20": [n*x for x in [280, 30, 240, 40]],
            "21": [n*x for x in [280, 75, 240, 40]],

            # OCR 결과를 위한 좌표
            # rms voltage l-l l-m min max
            ConfigROI.title_view: [n*x for x in [160, 120, 620, 53]],
            ConfigROI.a_ab: [n*x for x in [175, 179, 135, 70]],  # AB
            ConfigROI.a_time_stamp: [n*x for x in [320, 220, 190, 25]], # time stamp
            ConfigROI.a_meas: [n*x for x in [540, 190, 230, 55]],  # 190.0 V
            ConfigROI.b_bc: [n*x for x in [165, 253, 135, 69]],  # BC
            ConfigROI.b_time_stamp: [n*x for x in [320, 293, 190, 25]], # time stamp
            ConfigROI.b_meas: [n*x for x in [540, 260, 230, 60]],  # 190.0 V
            ConfigROI.c_ca: [n*x for x in [165, 326, 135, 69]],  # CA
            ConfigROI.c_time_stamp: [n*x for x in [320, 365, 190, 25]], # time stamp
            ConfigROI.c_meas: [n*x for x in [540, 340, 230, 50]],  # 190.0 V
            ConfigROI.aver: [n*x for x in [165, 399, 135, 69]],  # Average
            ConfigROI.aver_time_stamp: [n*x for x in [320, 438, 190, 25]], # time stamp
            ConfigROI.aver_meas: [n*x for x in [540, 410, 230, 60]],  # 190.0

            ### 확인 후 제거 ###
            "main_view_5": [n*x for x in [720, 200, 35, 40]],  # V
            "main_view_9": [n*x for x in [720, 270, 35, 40]],  # V
            "main_view_13": [n*x for x in [720, 350, 35, 40]],  # V
            "main_view_17": [n*x for x in [720, 420, 35, 40]],  # V

            # current % meas 수치 해야됨
            ConfigROI.curr_per_a: [n*x for x in [360, 190, 120, 30]],
            ConfigROI.curr_per_b: [n*x for x in [360, 265, 120, 30]],
            ConfigROI.curr_per_c: [n*x for x in [360, 335, 120, 30]],
            ConfigROI.curr_per_aver: [n*x for x in [360, 405, 120, 35]],

            # test mode confirm
            "999": [n*x for x in [220, 105, 350, 40]],

            # Phasor
            ConfigROI.phasor_img_cut: [176, 179, 425, 295],
            ConfigROI.phasor_title: [n*x for x in [160, 130, 140, 40]], # Phasor
            ConfigROI.phasor_title_2: [n*x for x in [530, 130, 246, 40]], # [V]Voltage, [V]Current
            ConfigROI.phasor_view_2: [n*x for x in [480, 120, 310, 53]], # [V]Voltage, [V]Current
            ConfigROI.phasor_vl_vn: [n*x for x in [570, 190, 210, 39]],  # VLL VLN
            ConfigROI.phasor_voltage: [n*x for x in [465, 235, 80, 27]],  # Voltage
            ConfigROI.phasor_a_c_vol: [n*x for x in [550, 234, 55, 76]], # AB,BC,CA or A,B,C
            ConfigROI.phasor_a_meas: [n*x for x in [610, 236, 95, 23]],  # A-전압수치
            ConfigROI.phasor_a_angle: [n*x for x in [705, 236, 58, 23]],  # A-각도수치
            ConfigROI.phasor_b_meas: [n*x for x in [610, 260, 95, 23]],  # B-전압수치
            ConfigROI.phasor_b_angle: [n*x for x in [705, 260, 58, 23]],  # B-각도수치
            ConfigROI.phasor_c_meas: [n*x for x in [610, 284, 95, 23]],  # C-전압수치
            ConfigROI.phasor_c_angle: [n*x for x in [705, 284, 58, 23]],  # C-각도수치
            ConfigROI.phasor_a_c_angle_vol: [763, 236, 14, 66],  # A~C-각도기호
            ConfigROI.phasor_current: [n*x for x in [465, 345, 80, 24]],  # Current
            ConfigROI.phasor_a_c_cur: [n*x for x in [550, 345, 55, 76]],  # A,B,C
            ConfigROI.phasor_a_meas_cur: [n*x for x in [610, 346, 95, 23]],  # A-전류수치
            ConfigROI.phasor_a_angle_cur: [n*x for x in [705, 346, 58, 23]],  # A-각도수치
            ConfigROI.phasor_b_meas_cur: [n*x for x in [610, 370, 95, 23]],  # B-전류수치
            ConfigROI.phasor_b_angle_cur: [n*x for x in [705, 370, 58, 23]],  # B-각도수치
            ConfigROI.phasor_c_meas_cur: [n*x for x in [610, 394, 95, 23]],  # C-전류수치
            ConfigROI.phasor_c_angle_cur: [n*x for x in [705, 394, 58, 23]],  # C-각도수치
            ConfigROI.phasor_a_c_angle_cur: [763, 394, 14, 21], # A~C-각도기호

            # harmonics
            ConfigROI.harmonics_img_cut: [170, 260, 600, 213],
            ConfigROI.harmonics_text_img: [n*x for x in [165, 230, 620, 240]],
            ConfigROI.harmonics_title: [n*x for x in [160, 120, 630, 53]],
            ConfigROI.harmonics_sub_title_1: [n*x for x in [160, 180, 270, 80]], # dropdown 버튼 + THD Fund.
            ConfigROI.harmonics_sub_title_2: [n*x for x in [440, 180, 130, 40]], # Fund.
            ConfigROI.harmonics_sub_title_3: [n*x for x in [580, 180, 2000, 40]], # Fund.
            ConfigROI.harmonics_text_title: [n*x for x in [160, 180, 620, 40]],
            ConfigROI.harmonics_text_sub_title : [n*x for x in [160, 180, 270, 40]],
            ConfigROI.harmonics_text_sub_abc : [n*x for x in [590, 180, 190, 40]],
            ConfigROI.harmonics_graph_a : [n*x for x in [435, 220, 15, 21]],
            ConfigROI.harmonics_graph_b : [n*x for x in [555, 220, 15, 21]],
            ConfigROI.harmonics_graph_c : [n*x for x in [675, 220, 15, 21]],
            ConfigROI.harmonics_thd_a : [n*x for x in [465, 220, 70, 21]],
            ConfigROI.harmonics_thd_b : [n*x for x in [585, 220, 70, 21]],
            ConfigROI.harmonics_thd_c : [n*x for x in [705, 220, 70, 21]],
            ConfigROI.harmonics_fund_a : [n*x for x in [465, 241, 70, 23]],
            ConfigROI.harmonics_fund_b : [n*x for x in [585, 241, 70, 23]],
            ConfigROI.harmonics_fund_c : [n*x for x in [705, 241, 70, 23]],

            #Waveform
            ConfigROI.waveform_all_img_cut: [170, 179, 610, 286],
            ConfigROI.waveform_graph_img_cut: [313, 253, 411, 203],
            ConfigROI.waveform_title: [n*x for x in [160, 120, 630, 53]],
            ConfigROI.harmonics_graph_img_cut: [313, 283, 455, 173],
            ConfigROI.harmonics_chart_img_cut: [250, 260, 495, 214],
            ConfigROI.harmonics_text_number_title_1: [n*x for x in [175, 237, 30, 225]],
            ConfigROI.harmonics_text_number_meas_1: [n*x for x in [206, 238, 67, 232]],
            ConfigROI.harmonics_text_chart_img_cut_3: [n*x for x in [170, 389, 610, 240]]
        }
        return params
    
    def template_image_path(self):
        img_path ={
            
            
        }
        return img_path

    def match_m_setup_labels(self):
        m_home = {
            "L-N": ["A", "B", "c", "Average"],
            "L_Min": ["AB", "BC", "CA", "Average"],
            "L_Max": ["AB", "BC", "CA", "Average"],
            "N_Min": ["A", "B", "c", "Average"],
            "N_Max": ["A", "B", "c", "Average"],
                    }

        m_setup = {
            # voltage
            "1": ["Wiring", "Min. Meas. Secondary L-N Volt. [V]", "VT Primary L-L Voltage [V]", "VT Secondary L-L Voltage [V]",
                  "Primary Reference Voltage [V]", "Sliding Reference Voltage", "Rotating Sequence"],
            # current
            "2": ["CT Primary Current [A]", "CT Secondary Current [A]", "Reference Current [A]", "Min. Measured Current [mA]", "TDD Reference Selection", "TDD Nominal Current [A]"],
            # demand
            "3": ["Sub-Interval Time [min]", "Number of Sub-Intervals", "Power Type", "Sync Mode", "Thermal Response Index [%]"],
            # power
            "4": ["Phase Power Calculation", "Total Power Calculation", "PF Sign", "PF Value at No Load", "Reactive Power Sign"],
            # dip
            "5": ["Dip", "Threshold [%]", "Hysteresis [%]", "3-Phase Dip"],
            # swell
            "6": ["Swell", "Threshold [%]", "Hysteresis [%]"],
            # pqcurve
            "7": ["SEMI F47-0706", "IEC 61000-4-11/34 Class 3", "ITIC"],
            # Ethernet
            "8": ["IP Address", "Subnet Mask", "Gateway", "MAC Address", "DHCP", "USB IP Address"],
            # RS485
            "9": ["Device Address", "Bit Rate", "Parity", "Stop Bit"],
            # Advanced
            "10": ["Modbus TCP Timeout [sec]", "RSTP", "Storm Control", "Remote Control Lock Mode"],
            # test mode"
            "999": ["Password"]
        }
        return m_home, m_setup

    def match_pop_labels(self):

        pop_params = {
            "1": ["Wiring", "3P4W", "3P3W"],  # wiring
            # Min. Meas. Secondary L-N Volt. [V]
            "2": ["Min. Meas. Secondary L-N Volt. [V]", "Range 1 - 10"],
            # VT Primary L-L Voltage
            "3": ["VT Primary L-L Voltage", "Range 50.0 - 999999.0"],
            # VT Secondary L-L Voltage [V]
            "4": ["VT Secondary L-L Voltage [V]", "Range 50.0 - 220.0"],
            # Primary Reference Voltage [V]
            "5": ["Primary Reference Voltage [V]", "Line-to-Line", "Line-to-Neutral", "Range 50.0 - 999999.0"],
            # Sliding Reference Voltage
            "6": ["Sliding Reference Voltage", "Disable", "Enable"],
            # Rotating Sequence
            "7": ["Rotating Sequence", "Positive", "Negative"],
        }

        return pop_params

    def color_detection_data(self):

        coordinates = {
            "measurement": [5, 70, 10, 10, 47, 180, 139],
            
            "mea_demand": [110, 220, 10, 10, 255, 255, 255],
            "mea_power": [110, 270, 10, 10, 255, 255, 255],

        }

        return coordinates

    def touch_data(self):
        coordinates = {
            "data_view_1": [320, 210],
            "data_view_2": [620, 210],
            "data_view_3": [320, 280],
            "data_view_4": [620, 280],
            "data_view_5": [320, 360],
            "data_view_6": [620, 360],
            "data_view_7": [320, 430],
            "data_view_8": [620, 430],
            "btn_apply": [620, 150],
            "btn_cancel": [720, 150],
            "btn_popup_1": [400, 110],
            "btn_popup_2": [400, 160],
            "btn_popup_3": [400, 215],
            "btn_popup_4": [400, 265],
            "btn_popup_5": [400, 315],
            "btn_popup_enter": [340, 415],
            "btn_popup_cancel": [450, 430],
            "btn_number_1": [310, 200],
            "btn_number_2": [370, 200],
            "btn_number_3": [430, 200],
            "btn_number_4": [310, 255],
            "btn_number_5": [370, 255],
            "btn_number_6": [430, 255],
            "btn_number_7": [310, 310],
            "btn_number_8": [370, 310],
            "btn_number_9": [430, 310],
            "btn_number_0": [310, 370],
            "btn_number_dot": [370, 370],
            "btn_number_back": [490, 225],
            "btn_number_clear": [485, 340],
            "btn_num_pw_1": [255, 230],
            "btn_num_pw_2": [315, 230],
            "btn_num_pw_3": [370, 230],
            "btn_num_pw_4": [430, 230],
            "btn_num_pw_5": [485, 230],
            "btn_num_pw_6": [255, 290],
            "btn_num_pw_7": [315, 290],
            "btn_num_pw_8": [370, 290],
            "btn_num_pw_9": [430, 290],
            "btn_num_pw_0": [485, 290],
            "btn_num_pw_enter": [340, 345],
            "btn_testmode_1": [270, 100],
            "btn_testmode_2": [270, 160],
            "infinite": [490, 125],
            "cauiton_confirm": [340, 330],
            "cauiton_cancel": [450, 330],
        }
        return coordinates

    def meter_m_vol_mapping(self):

        # smartsheet의 address는 1-based
        # 아래의 address는 0-based
        meter_m_vol_mappings_value = {
            6001: {"description": "Wiring", "values": {0: "3P4W", 1: "3P3W"}},
            # 명칭 예외처리
            6009: {"description": "Reference voltage mode", "values": {0: "Line-to-Line", 1: "Line-to-Neutral"}},
            6040: {"description": "Rotating Sequence", "values": {0: "Auto", 1: "Positive", 2: "Negative"}},
            6051: {"description": "Sliding Reference Voltage", "values": {0: "Disable", 1: "Enable"}},
        }

        meter_m_vol_mappings_uint16 = {
            6007: {"description": "VT Secondary L-L Voltage[V]", "type": "uint16"},
            6008: {"description": "Min. Measured Secondary Voltage", "type": "uint16"},
        }

        meter_m_vol_mappings_uint32 = {
            6003: {"description": "Primary Reference Voltage[V]", "type": "uint32"},
            6005: {"description": "VT Primary L-L Voltage [V]", "type": "uint32"},
        }

        return meter_m_vol_mappings_value, meter_m_vol_mappings_uint16, meter_m_vol_mappings_uint32

    def meter_m_cur_mapping(self):

        meter_m_cur_mappings_value = {
            6023: {"description": "TDD Reference Selection", "values": {0: "Nominal Current", 1: "Peak Demand Current"}}
        }

        meter_m_cur_mappings_uint16 = {
            6021: {"description": "Min. Measured Current [mA]", "type": "uint16"},
        }

        meter_m_cur_mappings_uint32 = {
            6015: {"description": "Reference Current [A]", "type": "uint32"},
            6017: {"description": "CT Primary Current [A]", "type": "uint32"},
            6019: {"description": "CT Secondary Current [A]", "type": "uint32"},
            6021: {"description": "TDD Nominal current [A]", "type": "uint32"},
        }

        return meter_m_cur_mappings_value, meter_m_cur_mappings_uint16, meter_m_cur_mappings_uint32