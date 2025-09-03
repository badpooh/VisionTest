from enum import Enum

class ConfigMap(Enum):
    ### modbus map 에서 -1 값 ###
    addr_reset_max_min = (12002, 1)

    ### measurement setup ###
    ### UINT16 ###
    addr_measurement_setup_access = (6000, 1)
    addr_wiring = (6001, 1)
    addr_vt_secondary_ll_voltage = (6007, 1)
    addr_min_measured_secondary_ln_voltage = (6008, 1)
    addr_reference_voltage_mode = (6009, 1)
    addr_ct_secondary_current = (6019, 1)
    addr_min_measured_current = (6020, 1)
    addr_tdd_reference = (6023, 1)
    addr_demand_sync_mode = (6028, 1)
    addr_num_of_sub_interval = (6029, 1)
    addr_sub_interval_time = (6030, 1)
    addr_thermal_response_index = (6031, 1)
    addr_demand_power_type = (6032, 1)
    addr_phase_power_calculation = (6033, 1)
    addr_total_power_calculation = (6034, 1)
    addr_pf_value_at_no_load = (6035, 1)
    addr_pf_sign = (6036, 1)
    addr_reactive_power_sign = (6037, 1)
    # addr_default_frequency = (6038, 1)
    # addr_max_harmonic_order = (6039, 1)
    addr_rotating_sequence = (6040, 1)
    addr_sliding_reference_voltage_setup_access = (6050, 1)
    addr_sliding_reference_voltage_type = (6051, 1)
    ### UINT32 ###
    addr_reference_voltage = (6003, 2)
    addr_vt_primary_ll_voltage = (6005, 2)
    addr_reference_current = (6015, 2)
    addr_ct_primary_current = (6017, 2)
    addr_nominal_tdd_current = (6021, 2)

    ### meter event setup ###
    addr_dip_setup_access = (5100, 1)
    addr_dip = (5101, 1)
    addr_dip_threshold = (5102, 1)
    addr_dip_hysteresis = (5103, 1)
    addr_3phase_dip_setup_access = (5110, 1)
    addr_3phase_dip = (5111, 1)
    addr_swell_setup_access = (5120, 1)
    addr_swell = (5121, 1)
    addr_swell_threshold = (5122, 1)
    addr_swell_hysteresis = (5123, 1)
    addr_semi_event_setup_access = (5160, 1)
    addr_semi = (5161, 1)
    addr_itic_event_setup_access = (5190, 1)
    addr_itic = (5191, 1)
    addr_iec_event_setup_access = (5220, 1)
    addr_iec = (5221, 1)

    ### meter network setup ###
    addr_dhcp_setup_access = (3720, 1)
    addr_dhcp = (3721, 1)
    addr_rs485_setup_access = (3700, 1)
    addr_device_address = (3701, 1)
    addr_bit_rate = (3702, 1)
    addr_parity = (3703, 1)
    addr_stop_bit = (3704, 1)
    addr_modbus_timeout_setup_access = (3620, 1)
    addr_modbus_timeout = (3621, 1)
    addr_rstp_setup_access = (3640, 1)
    addr_rstp = (3641, 1)
    addr_storm_control_setup_access = (3680, 1)
    addr_storm_control = (3681, 1)
    addr_rs485_map_setup_access = (3630, 1)
    addr_rs485_map = (3631, 1)
    addr_remote_control_lock_mode_access = (3400, 1)
    addr_remote_control_lock_mode = (3401, 1)

    ### meter control ###
    addr_meter_test_mode = (4000, 1)
    addr_meter_demo_mode_timeout_setup_access = (4001, 1)
    addr_meter_demo_mode_timeout = (4002, 1)

    ### meter system ###
    addr_description_setup_access = (3300, 1)
    addr_installation_year = (3331, 1)
    addr_installation_month = (3332, 1)
    addr_installation_day = (3333, 1)
    addr_locale_setup_access = (3020, 1)
    addr_timezone_offset = (3021, 1)
    addr_temperature_unit = (3022, 1)
    addr_energy_unit = (3023, 1)
    addr_date_display_format = (3024, 1)
    addr_system_time_setup_access = (3060, 1)
    addr_summer_time_setup_access = (3000, 1)
    addr_summer_time = (3001, 1)
    addr_start_month = (3003, 1)
    addr_start_nth_weekday = (3004, 1)
    addr_start_weekday = (3005, 1)
    addr_start_minute = (3006, 1)
    addr_end_month = (3007, 1)
    addr_end_nth_weekday = (3008, 1)
    addr_end_weekday = (3009, 1)
    addr_end_minute = (3010, 1)
    addr_summer_time_offset = (3002, 1)
    addr_ntp_setup_access = (3040, 1)
    addr_ntp_ip = (3041, 1)
    addr_sync_mode = (3043, 1)
    addr_sync_period = (3044, 1)
    addr_sync_max_drift = (3045, 1)
    addr_lcd_buzzer_setup_access = (3800, 1)
    addr_lcd_backlight_timeout = (3801, 1)
    addr_lcd_backlight_low_level = (3802, 1)
    addr_buzzer_for_button = (3803, 1)
    ### UINT32 ###
    addr_system_time_sec = (3061, 2)
    addr_system_time_usec = (3063, 2)
    
    addr_reset_demand = (12000, 1)
    addr_reset_demand_peak = (12001, 1)
    addr_demand_sync = (12015, 1)
    
    addr_setup_lock = (2900, 1)
    addr_control_lock = (2901, 1)


class ConfigInitialValue(Enum):
    initial_setup_values = {
        # modbus map - -1 값
        ConfigMap.addr_reset_max_min: None,
        
        # measurement setup - UINT16
        ConfigMap.addr_measurement_setup_access: None,
        ConfigMap.addr_wiring: 0,
        ConfigMap.addr_vt_secondary_ll_voltage: 1900,
        ConfigMap.addr_min_measured_secondary_ln_voltage: 5,
        ConfigMap.addr_reference_voltage_mode: 0,
        ConfigMap.addr_ct_secondary_current: 5,
        ConfigMap.addr_min_measured_current: 5,
        ConfigMap.addr_tdd_reference: 1,
        ConfigMap.addr_demand_sync_mode: 0,
        ConfigMap.addr_num_of_sub_interval: 1,
        ConfigMap.addr_sub_interval_time: 15,
        ConfigMap.addr_thermal_response_index: 90,
        ConfigMap.addr_demand_power_type: 0,
        ConfigMap.addr_phase_power_calculation: 1,
        ConfigMap.addr_total_power_calculation: 0,
        ConfigMap.addr_pf_value_at_no_load: 1,
        ConfigMap.addr_pf_sign: 1,
        ConfigMap.addr_reactive_power_sign: 1,
        # ConfigModbusMap.addr_default_frequency: 1,
        # ConfigModbusMap.addr_max_harmonic_order: 50,
        ConfigMap.addr_rotating_sequence: 1,
        ConfigMap.addr_sliding_reference_voltage_setup_access: None,
        ConfigMap.addr_sliding_reference_voltage_type: 0,
        
        # measurement setup - UINT32
        ConfigMap.addr_reference_voltage: 1900,
        ConfigMap.addr_vt_primary_ll_voltage: 1900,
        ConfigMap.addr_reference_current: 50,
        ConfigMap.addr_ct_primary_current: 50,
        ConfigMap.addr_nominal_tdd_current: 0,
        
        # meter event setup
        ConfigMap.addr_dip_setup_access: None,
        ConfigMap.addr_dip: 0,
        ConfigMap.addr_dip_threshold: 900,
        ConfigMap.addr_dip_hysteresis: 20,
        ConfigMap.addr_3phase_dip_setup_access: None,
        ConfigMap.addr_3phase_dip: 0,
        ConfigMap.addr_swell_setup_access: None,
        ConfigMap.addr_swell: 0,
        ConfigMap.addr_swell_threshold: 1100,
        ConfigMap.addr_swell_hysteresis: 20,
        ConfigMap.addr_semi_event_setup_access: None,
        ConfigMap.addr_semi: 0,
        ConfigMap.addr_itic_event_setup_access: None,
        ConfigMap.addr_itic: 0,
        ConfigMap.addr_iec_event_setup_access: None,
        ConfigMap.addr_iec: 0,
        
        # meter network setup
        ConfigMap.addr_dhcp_setup_access: None,
        ConfigMap.addr_dhcp: 0,
        ConfigMap.addr_rs485_setup_access: None,
        ConfigMap.addr_device_address: 0,
        ConfigMap.addr_bit_rate: 3,
        ConfigMap.addr_parity: 2,
        ConfigMap.addr_stop_bit: 0,
        ConfigMap.addr_modbus_timeout_setup_access: None,
        ConfigMap.addr_modbus_timeout: 600,
        ConfigMap.addr_rstp_setup_access: None,
        ConfigMap.addr_rstp: 0,
        ConfigMap.addr_storm_control_setup_access: None,
        ConfigMap.addr_storm_control: 1,
        ConfigMap.addr_rs485_map_setup_access: None,
        ConfigMap.addr_rs485_map: 0,
        ConfigMap.addr_remote_control_lock_mode_access: None,
        ConfigMap.addr_remote_control_lock_mode: 0,
        
        # meter control
        ConfigMap.addr_meter_test_mode: 0,
        ConfigMap.addr_meter_demo_mode_timeout_setup_access: None,
        ConfigMap.addr_meter_demo_mode_timeout: 60,
        
        # meter system - UINT16
        ConfigMap.addr_description_setup_access: None,
        ConfigMap.addr_installation_year: 1970,
        ConfigMap.addr_installation_month: 1,
        ConfigMap.addr_installation_day: 1,
        ConfigMap.addr_locale_setup_access: None,
        ConfigMap.addr_timezone_offset: 540,
        ConfigMap.addr_temperature_unit: 0,
        ConfigMap.addr_energy_unit: 0,
        ConfigMap.addr_date_display_format: 0,
        ConfigMap.addr_system_time_setup_access: None,
        ConfigMap.addr_summer_time_setup_access: None,
        ConfigMap.addr_summer_time: 0,
        ConfigMap.addr_start_month: 3,
        ConfigMap.addr_start_nth_weekday: 2,
        ConfigMap.addr_start_weekday: 0,
        ConfigMap.addr_start_minute: 120,
        ConfigMap.addr_end_month: 11,
        ConfigMap.addr_end_nth_weekday: 1,
        ConfigMap.addr_end_weekday: 0,
        ConfigMap.addr_end_minute: 120,
        ConfigMap.addr_summer_time_offset: 60,
        ConfigMap.addr_ntp_setup_access: None,
        ConfigMap.addr_ntp_ip: None,
        ConfigMap.addr_sync_mode: 1,
        ConfigMap.addr_sync_period: 600,
        ConfigMap.addr_sync_max_drift: 1,
        ConfigMap.addr_lcd_buzzer_setup_access: None,
        ConfigMap.addr_lcd_backlight_timeout: 300,
        ConfigMap.addr_lcd_backlight_low_level: 10,
        ConfigMap.addr_buzzer_for_button: 1,
        
        # meter system - UINT32
        ConfigMap.addr_system_time_sec: None,
        ConfigMap.addr_system_time_usec: None,
        
        # 기타
        ConfigMap.addr_reset_demand: None,
        ConfigMap.addr_reset_demand_peak: None,
        ConfigMap.addr_demand_sync: None,
        ConfigMap.addr_setup_lock: None,
        ConfigMap.addr_control_lock: None,
    }
