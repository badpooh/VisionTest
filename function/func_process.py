from demo_test.demo_process import DemoTest
from setup_test.setup_process import SetupTest
from function.func_modbus import ConnectionManager

class TestProcess:
    
    def __init__(self, setup_test: SetupTest, connect_manager: ConnectionManager, score_callback=None, stop_callback=None):
        self.test_mode = None
        self.score_callback = score_callback
        self.stop_callback = stop_callback 
        self.demo_test = None
        self.setup_test = setup_test
        self.connect_manager = connect_manager
        # self.setup_test = None

    def get_demo_test_instance(self):
        if self.demo_test is None:
            self.demo_test = DemoTest(score_callback=self.score_callback, stop_callback=self.stop_callback)
        return self.demo_test
    
    # def get_setup_test_instance(self):
    #     if self.setup_test is None:
    #         self.setup_test = SetupTest()
    #     return self.setup_test
    
    def test_by_name(self, test_name, base_save_path, test_mode, search_pattern):
        demo_test = self.get_demo_test_instance()
        # setup_test = self.get_setup_test_instance()

        if test_name.strip().lower() == "tm_balance":
            demo_test.demo_test_mode()
        elif test_name.strip().lower() == "tm_noload":
            demo_test.noload_test_mode()
        
        if test_mode == "Demo" or "NoLoad":
            if test_name == "vol_all":
                demo_test.demo_mea_vol_all(base_save_path, test_mode, search_pattern)
            elif test_name == "vol_rms":
                demo_test.demo_mea_vol_rms(base_save_path, test_mode, search_pattern)
            elif test_name == "vol_fund":
                demo_test.demo_mea_vol_fund(base_save_path, test_mode, search_pattern)
            elif test_name == "vol_thd":
                demo_test.demo_mea_vol_thd(base_save_path, test_mode, search_pattern)
            elif test_name == "vol_freq":
                demo_test.demo_mea_vol_freq(base_save_path, test_mode, search_pattern)
            elif test_name == "vol_residual":
                demo_test.demo_mea_vol_residual(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_all":
                demo_test.demo_mea_curr_all(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_rms":
                demo_test.demo_mea_curr_rms(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_fund":
                demo_test.demo_mea_curr_fund(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_demand":
                demo_test.demo_mea_curr_demand(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_thd":
                demo_test.demo_mea_curr_thd(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_tdd":
                demo_test.demo_mea_curr_tdd(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_cf":
                demo_test.demo_mea_curr_cf(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_kf":
                demo_test.demo_mea_curr_kf(base_save_path, test_mode, search_pattern)
            elif test_name == "curr_residual":
                demo_test.demo_mea_curr_residual(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_all":
                demo_test.demo_mea_pow_all(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_p":
                demo_test.demo_mea_pow_active(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_q":
                demo_test.demo_mea_pow_reactive(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_s":
                demo_test.demo_mea_pow_apparent(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_pf":
                demo_test.demo_mea_pow_pf(base_save_path, test_mode, search_pattern)
            elif test_name == "pow_demand":
                pass
            elif test_name == "pow_energy":
                pass
            elif test_name == "anal_all":
                demo_test.demo_mea_anal_all(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_phasor":
                demo_test.demo_mea_anal_phasor(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_harmonics":
                demo_test.demo_mea_anal_harmonics(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_waveform":
                demo_test.demo_mea_anal_waveform(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_volt_sym":
                demo_test.demo_mea_anal_voltsym(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_volt_unbal":
                demo_test.demo_mea_anal_voltunbal(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_curr_sym":
                demo_test.demo_mea_anal_cursym(base_save_path, test_mode, search_pattern)
            elif test_name == "anal_curr_unbal":
                demo_test.demo_mea_anal_currunbal(base_save_path, test_mode, search_pattern)
            elif test_name == 'm_s_meas_all':
                self.setup_test.setup_m_s_meas_all(base_save_path, search_pattern)
            elif test_name == "m_s_vol":
                self.setup_test.setup_meter_s_m_vol(base_save_path, search_pattern)
            elif test_name == 'm_s_curr':
                self.setup_test.setup_meter_s_m_curr(base_save_path, search_pattern)
            elif test_name == 'm_s_demand':
                self.setup_test.m_s_meas_demand(base_save_path, search_pattern)
            elif test_name == 'm_s_power':
                self.setup_test.m_s_meas_power(base_save_path, search_pattern)
            elif test_name == 'm_s_event_all':
                self.setup_test.setup_m_s_event_all(base_save_path, search_pattern)
            elif test_name == 'm_s_dip':
                self.setup_test.m_s_event_dip(base_save_path, search_pattern)
            elif test_name == 'm_s_swell':
                self.setup_test.m_s_event_swell(base_save_path, search_pattern)
            elif test_name == 'm_s_pq_curve':
                self.setup_test.m_s_event_pq_curve(base_save_path, search_pattern)
            elif test_name == 'm_s_network_all':
                self.setup_test.setup_m_s_network_all(base_save_path, search_pattern)
            elif test_name == 'm_s_ethernet':
                self.setup_test.m_s_network_ethernet(base_save_path, search_pattern)
            elif test_name == 'm_s_rs485':
                self.setup_test.m_s_network_rs485(base_save_path, search_pattern)
            elif test_name == 'm_s_advanced':
                self.setup_test.m_s_network_advanced(base_save_path, search_pattern)
            elif test_name == 'm_s_test_mode':
                self.setup_test.m_s_control_test_mode(base_save_path, search_pattern)
            elif test_name == 'm_s_description':
                self.setup_test.m_s_system_description(base_save_path, search_pattern)
            elif test_name == 'm_s_locale':
                self.setup_test.m_s_system_locale(base_save_path, search_pattern)
            elif test_name == 'm_s_local_time':
                self.setup_test.m_s_system_local_time(base_save_path, search_pattern)
            elif test_name == 'm_s_summer_time':
                self.setup_test.m_s_system_summer_time(base_save_path, search_pattern)
            elif test_name == 'm_s_ntp':
                self.setup_test.m_s_system_ntp(base_save_path, search_pattern)
            elif test_name == 'm_s_lcd_buzzer':
                self.setup_test.m_s_system_lcd_buzzer(base_save_path, search_pattern)

                
            else:
                print(f"Unknown test name: {test_name}")
            
        
        
        else:
            print("demo_test_by_name Error")