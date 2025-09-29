from enum import Enum

class TestModeBalance(Enum):
	### Voltage
	vol_rms_ll = [
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"}]
	vol_rms_ln = [
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"}]
	vol_fund_ll = [
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"},
				{'low': 189.0, 'high': 191.0, 'unit': "V"}]
	vol_fund_ln = [
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"},
				{'low': 109.0, 'high': 111.0, 'unit': "V"}]
	vol_thd_ll = [
				{'low': 2.0, 'high': 3.0, 'unit': "%"},
				{'low': 2.0, 'high': 3.0, 'unit': "%"},
				{'low': 2.0, 'high': 3.0, 'unit': "%"}]
	vol_thd_ln = [
				{'low': 3.0, 'high': 4.0, 'unit': "%"},
				{'low': 3.0, 'high': 4.0, 'unit': "%"},
				{'low': 3.0, 'high': 4.0, 'unit': "%"}]
	vol_freq = [{'low': 59.800, 'high': 60.100, 'unit': "Hz"}]
	vol_residual = [
					{'low': 6.000, 'high': 7.000, 'unit': 'V'},
					{'low': 0.700, 'high': 2.000, 'unit': 'V'},]
	### Current
	curr_rms = [
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"}]
	curr_rms_ratio = [
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"}]
	curr_fund = [
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"}]
	curr_fund_ratio = [
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"}]
	curr_demand = [
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"},
				{'low': 24.00, 'high': 26.00, 'unit': "A"}]
	curr_demand_ratio = [
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"}]
	curr_thd = [
				{'low': 1.5, 'high': 2.5, 'unit': "%"},
				{'low': 1.5, 'high': 2.5, 'unit': "%"},
				{'low': 1.5, 'high': 2.5, 'unit': "%"}]
	curr_tdd = [
				{'low': 1.5, 'high': 2.5, 'unit': "%"},
				{'low': 1.5, 'high': 2.5, 'unit': "%"},
				{'low': 1.5, 'high': 2.5, 'unit': "%"}]
	curr_cf = [
				{'low': 1.400, 'high': 1.500},
				{'low': 1.400, 'high': 1.500},
				{'low': 1.400, 'high': 1.500}]
	curr_kf = [
				{'low': 1.200, 'high': 1.500, 'unit': ""},
				{'low': 1.200, 'high': 1.500, 'unit': ""},
				{'low': 1.200, 'high': 1.500, 'unit': ""}]
	curr_residual = [
					{'low': 0.500, 'high': 1.000, 'unit': 'A'},
					{'low': 0.100, 'high': 0.500, 'unit': 'A'},]
	
	### Power
	pow_p = [
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 6.900, 'high': 7.200, 'unit': "kW"}]
	pow_p_ratio = [
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"}]
	pow_q = [
				{'low': 1.300, 'high': 1.400, 'unit': "kVAR"},
				{'low': 1.300, 'high': 1.400, 'unit': "kVAR"},
				{'low': 1.300, 'high': 1.400, 'unit': "kVAR"},
				{'low': 3.900, 'high': 4.200, 'unit': "kVAR"}]
	pow_q_ratio = [
				{'low': 20.0, 'high': 30.0, 'unit': "%"},
				{'low': 20.0, 'high': 30.0, 'unit': "%"},
				{'low': 20.0, 'high': 30.0, 'unit': "%"},
				{'low': 20.0, 'high': 30.0, 'unit': "%"}]
	pow_s = [
				{'low': 2.500, 'high': 2.900, 'unit': "kVAR"},
				{'low': 2.500, 'high': 2.900, 'unit': "kVAR"},
				{'low': 2.500, 'high': 2.900, 'unit': "kVAR"},
				{'low': 7.500, 'high': 8.700, 'unit': "kVAR"}]
	pow_s_ratio = [
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"},
				{'low': 49.0, 'high': 51.0, 'unit': "%"}]
	pow_pf = [
				{'low': 0.850, 'high': 0.900, 'unit': ""},
				{'low': 0.850, 'high': 0.900, 'unit': ""},
				{'low': 0.850, 'high': 0.900, 'unit': ""},
				{'low': 0.850, 'high': 0.900, 'unit': ""}]
	pow_pf_ratio = [
				{'text': "Lag"},
				{'text': "Lag"},
				{'text': "Lag"},
				{'text': "Lag"}]
	pow_demand = [
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 2.300, 'high': 2.400, 'unit': "kW"},
				{'low': 6.900, 'high': 7.200, 'unit': "kW"}]
	pow_demand_ratio = [
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"},
				{'low': 40.0, 'high': 45.0, 'unit': "%"}]


	