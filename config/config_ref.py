from enum import Enum

class ConfigTextRef(Enum):
    ### measuremnet ###
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

    ### setup ###
    wiring = ["Wye", "Delta"]

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

    ### AccuraSM
    img_ref_meas_refresh = r'.\vision\image_ref\101.meter_setup_meas_min.png'
    img_ref_meter_setup_meas_min = r'.\vision\image_ref\101.meter_setup_meas_min.png'
    img_ref_meter_setup_meas_max = r'.\vision\image_ref\102.meter_setup_meas_max.png'
    img_ref_meter_setup_meas_exc = r'.\vision\image_ref\103.meter_setup_meas_exc.png'
    img_ref_meter_setup_event_min = r'.\vision\image_ref\104.meter_setup_event_min.png'
    img_ref_meter_setup_event_max = r'.\vision\image_ref\105.meter_setup_event_max.png'


    # img_ref_wiring_wye = r'.\vision\image_ref\102.wiring_wye.png'
    # img_ref_wiring_delta = r'.\vision\image_ref\103.wiring_delta.png'
    # img_ref_min_meas_secondary_ln_vol_0 = r'.\vision\image_ref\104.min_meas_secondary_ln_vol_0.png'
    # img_ref_min_meas_secondary_ln_vol_10 = r'.\vision\image_ref\105.min_meas_secondary_ln_vol_10.png'
    # img_ref_vt_primary_ll_vol_50 = r'.\vision\image_ref\106.vt_primary_ll_vol_50.0.png'
    # img_ref_vt_primary_ll_vol_999999 = r'.\vision\image_ref\107.vt_primary_ll_vol_999999.0.png'
    # img_ref_vt_secondary_ll_vol_50 = r'.\vision\image_ref\108.vt_secondary_ll_vol_50.png'
    # img_ref_vt_secondary_ll_vol_220 = r'.\vision\image_ref\109.vt_secondary_ll_vol_220.png'
    # img_ref_primary_reference_vol_mode_ll = r'.\vision\image_ref\110.primary_reference_vol_mode_ll.png'
    # img_ref_primary_reference_vol_mode_ln = r'.\vision\image_ref\111.primary_reference_vol_mode_ln.png'
    # img_ref_primary_reference_vol_50 = r'.\vision\image_ref\112.primary_reference_vol_50.png'
    # img_ref_primary_reference_vol_999999 = r'.\vision\image_ref\112.primary_reference_vol_999999.png'
    # img_ref_sliding_reference_vol_disable = r'.\vision\image_ref\113.sliding_reference_vol_disable.png'
    # img_ref_sliding_reference_vol_enable = r'.\vision\image_ref\114.sliding_reference_vol_enable.png'
    # img_ref_rotating_sequence_positive = r'.\vision\image_ref\115.rotating_sequence_positive.png'
    # img_ref_rotating_sequence_negative = r'.\vision\image_ref\116.rotating_sequence_negative.png'
    # img_ref_ct_primary_curr_5 = r'.\vision\image_ref\117.ct_primary_current_5.png'
    # img_ref_ct_primary_curr_99999 = r'.\vision\image_ref\118.ct_primary_current_99999.png'
    # img_ref_ct_secondary_curr_5 = r'.\vision\image_ref\119.ct_secondary_current_5.png'
    # img_ref_ct_secondary_curr_10 = r'.\vision\image_ref\120.ct_secondary_current_10.png'
    # img_ref_reference_curr_5 = r'.\vision\image_ref\121.reference_current_5.png'
    # img_ref_reference_curr_99999 = r'.\vision\image_ref\122.reference_current_99999.png'
    # img_ref_min_measured_curr_0 = r'.\vision\image_ref\123.min_measured_current_0.png'
    # img_ref_min_measured_curr_100 = r'.\vision\image_ref\124.min_measured_current_100.png'
    # img_ref_tdd_reference_selection_peak = r'.\vision\image_ref\125.tdd_reference_selection_peak.png'
    # img_ref_tdd_reference_selection_tdd = r'.\vision\image_ref\126.tdd_reference_selection_tdd.png'
    # img_ref_tdd_nominal_curr_0 = r'.\vision\image_ref\127.tdd_nominal_current_0.png'
    # img_ref_tdd_nominal_curr_99999 = r'.\vision\image_ref\128.tdd_nominal_current_99999.png'
    




