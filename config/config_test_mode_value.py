from enum import Enum

class TestModeBalance(Enum):

	vol_rms_ll = (189.0, 191.0, "V")
	vol_rms_ln = (109.0, 111.0, "V")
	vol_fund_ll = (189.0, 191.0, "V")
	vol_fund_ln = (109.0, 111.0, "V")
	vol_thd_ll = (2.0, 3.0, "%")
	vol_thd_ln = (3.0, 4.0, "%")
	vol_freq = (59.800, 60.100, "Hz")
	vol_residual = [
					{'low': 6.000, 'high': 7.000, 'unit': 'V'},
					{'low': 0.700, 'high': 2.000, 'unit': 'V'},
					]
	vol_rms_residual = (6.000, 7.000, "V")
	vol_fund_residual = (0.700, 2.000, "V")
	curr_rms = (24.00, 26.00, "A")
	curr_rms_ratio = (49.0, 51.0, "%")
	curr_fund = (24.00, 26.00, "A")
	curr_fund_ratio = (49.0, 51.0, "%")
	curr_demand = (24.00, 26.00, "A")
	curr_demand_ratio = (49.0, 51.0, "%")
	curr_thd = (1.5, 2.5, "%")
	curr_tdd = (1.5, 2.5, "%")
	curr_cf = (1.400, 1.500, "")
	curr_kf = (1.200, 1.500, "")
	curr_rms_residaul = (0.500, 1.000, "A")
	curr_fund_residual = (0.100, 0.500, "A")


	