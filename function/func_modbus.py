import time
from datetime import datetime, timezone, timedelta
import time

from function.func_connection import ConnectionManager
from function.func_touch import TouchManager

from config.config_map import ConfigMap as ConfigMap

class ModbusLabels:

    touch_manager = TouchManager()
    # connect_manager = ConnectionManager()

    def __init__(self):
        self.connect_manager = ConnectionManager()

    def demo_test_setting(self):
        test_mode = "Demo"
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client is not None: 
            for value in values:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_setup_lock.value[0], value)
                time.sleep(0.6)
            vol_value_32bit = 1900
            high_word = (vol_value_32bit >> 16) & 0xFFFF
            low_word = vol_value_32bit & 0xFFFF
            self.response = self.connect_manager.setup_client.read_holding_registers(6000, 100)
            self.response = self.connect_manager.setup_client.read_holding_registers(6100, 100)
            self.response = self.connect_manager.setup_client.read_holding_registers(6200, 3)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.connect_manager.setup_client.write_register(6001, 0)
            self.response = self.connect_manager.setup_client.write_registers(6003, [high_word, low_word])
            self.response = self.connect_manager.setup_client.write_registers(6005, [high_word, low_word])
            self.response = self.connect_manager.setup_client.write_registers(6007, 1900)
            self.response = self.connect_manager.setup_client.write_register(6009, 0)
            self.response = self.connect_manager.setup_client.write_register(6000, 1)
            time.sleep(0.6)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(4002, 0)
            self.response = self.connect_manager.setup_client.write_register(4000, 1)
            self.response = self.connect_manager.setup_client.write_register(4001, 1)
            print("Demo mode setting Done")
        else:
            # print(self.response.isError())
            print("setup_client가 연결되어 있지 않습니다.")
        return test_mode

    def noload_test_setting(self):
        test_mode = "NoLoad"
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value in values:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_setup_lock.value[0], value)
                time.sleep(0.6)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(4000, 0)
            self.response = self.connect_manager.setup_client.write_register(4001, 1)
            print("Noload Demo mode setting Done")
        return test_mode
    
    def setup_initialization(self):
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]

        def value_32bit(value):
            return (value >> 16) & 0xFFFF, value & 0xFFFF

        if self.connect_manager.setup_client:
            for value in values:
                self.connect_manager.setup_client.write_register(ConfigMap.addr_setup_lock.value[0], value)
                time.sleep(0.6)
            for value_control in values_control:
                self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            
            ### measurement setup ###
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_measurement_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_wiring.value[0], 0)
            self.connect_manager.setup_client.write_registers(ConfigMap.addr_reference_voltage.value[0], [*value_32bit(1900)])
            self.connect_manager.setup_client.write_registers(ConfigMap.addr_vt_primary_ll_voltage.value[0], [*value_32bit(1900)])
            self.connect_manager.setup_client.write_register(ConfigMap.addr_vt_secondary_ll_voltage.value[0], 1900)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_min_measured_secondary_ln_voltage.value[0], 5)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_reference_voltage_mode.value[0], 0)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_sliding_reference_voltage_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sliding_reference_voltage_type.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sliding_reference_voltage_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rotating_sequence.value[0], 1)
            self.connect_manager.setup_client.write_registers(ConfigMap.addr_ct_primary_current.value[0], [*value_32bit(50)])
            self.connect_manager.setup_client.write_register(ConfigMap.addr_ct_secondary_current.value[0], 5)
            self.connect_manager.setup_client.write_registers(ConfigMap.addr_reference_current.value[0], [*value_32bit(50)])
            self.connect_manager.setup_client.write_register(ConfigMap.addr_min_measured_current.value[0], 5)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_tdd_reference.value[0], 1)
            self.connect_manager.setup_client.write_registers(ConfigMap.addr_nominal_tdd_current.value[0], [*value_32bit(0)])
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sub_interval_time.value[0], 15)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_num_of_sub_interval.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_power_type.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_sync_mode.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_thermal_response_index.value[0], 90)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_phase_power_calculation.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_total_power_calculation.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_pf_sign.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_pf_value_at_no_load.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_reactive_power_sign.value[0], 1)

            self.connect_manager.setup_client.write_register(ConfigMap.addr_measurement_setup_access.value[0], 1)

            ### meter event setup ###
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_dip_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_3phase_dip_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_swell_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_semi_event_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_itic_event_setup_access.value, 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_iec_event_setup_access.value, 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dip.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dip_threshold.value[0], 900)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dip_hysteresis.value[0], 20)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_3phase_dip.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dip_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_3phase_dip_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_swell.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_swell_threshold.value[0], 1100)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_swell_hysteresis.value[0], 20)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_swell_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_semi.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_semi_event_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_itic.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_itic_event_setup_access.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_iec.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_iec_event_setup_access.value[0], 1)

            ### meter network setup ###
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_dhcp_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dhcp.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_dhcp_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_rs485_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_device_address.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_bit_rate.value[0], 3)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_parity.value[0], 2)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_stop_bit.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rs485_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_modbus_timeout_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_modbus_timeout.value[0], 600)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_modbus_timeout_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_rstp_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rstp.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rstp_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_storm_control_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_storm_control.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_storm_control_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_rs485_map_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rs485_map.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_rs485_map_setup_access.value[0], 1)

            ### meter control setup ###
            self.connect_manager.setup_client.write_register(ConfigMap.addr_meter_test_mode.value[0], 0)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_meter_demo_mode_timeout_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_meter_demo_mode_timeout.value[0], 60)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_meter_demo_mode_timeout_setup_access.value[0], 1)

            ### meter system setup / local time 제외 ###
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_description_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_installation_year.value[0], 1970)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_installation_month.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_installation_day.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_description_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_locale_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_timezone_offset.value[0], 540)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_temperature_unit.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_energy_unit.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_date_display_format.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_locale_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_summer_time_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_summer_time.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_start_month.value[0], 3)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_start_nth_weekday.value[0], 2)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_start_weekday.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_start_minute.value[0], 120)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_end_month.value[0], 11)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_end_nth_weekday.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_end_weekday.value[0], 0)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_end_minute.value[0], 120)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_summer_time_offset.value[0], 60)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_summer_time_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_ntp_setup_access.value)
            # self.connect_manager.setup_client.write_register(ecm.addr_ntp_ip.value[0], 0A0A0A01) 값 변경 필요
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sync_mode.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sync_period.value[0], 600)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_sync_max_drift.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_ntp_setup_access.value[0], 1)
            self.connect_manager.setup_client.read_holding_registers(*ConfigMap.addr_lcd_buzzer_setup_access.value)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_lcd_backlight_timeout.value[0], 300)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_lcd_backlight_low_level.value[0], 10)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_buzzer_for_button.value[0], 1)
            self.connect_manager.setup_client.write_register(ConfigMap.addr_lcd_buzzer_setup_access.value[0], 1)
    
    def setup_target_initialize(self, access_addr, target_addr, bit16=None, bit32=None):
        self.touch_manager.uitest_mode_start()
        values = [2300, 0, 700, 1]
        values_control = [2300, 0, 1600, 1]

        def value_32bit(value):
            return (value >> 16) & 0xFFFF, value & 0xFFFF

        if self.connect_manager.setup_client:
            for value in values:
                self.connect_manager.setup_client.write_register(ConfigMap.addr_setup_lock.value[0], value)
                time.sleep(0.6)
            for value_control in values_control:
                self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            
            ### measurement setup ###
            address, words = target_addr.value
            if access_addr:
                self.connect_manager.setup_client.read_holding_registers(*access_addr.value)
            if words == 1:
                self.connect_manager.setup_client.write_register(target_addr.value[0], bit16)
            elif words == 2:
                self.connect_manager.setup_client.write_registers(target_addr.value[0], [*value_32bit(bit32)])
            else:
                print('words error?')
                return
            if access_addr:
                self.connect_manager.setup_client.write_register(access_addr.value[0], 1)
                                                                                                        
    def device_current_time(self):
        self.response = self.connect_manager.setup_client.read_holding_registers(3060, 3)
        high_word = self.connect_manager.setup_client.read_holding_registers(3061, 1).registers[0]
        low_word = self.connect_manager.setup_client.read_holding_registers(3062, 1).registers[0]
        unix_timestamp = (high_word << 16) | low_word

        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        kst_time = utc_time + timedelta(minutes=540)
        device_current_time = kst_time
        return device_current_time

    def reset_max_min(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            self.response = self.connect_manager.setup_client.read_holding_registers(3060, 3)
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_reset_max_min.value[0], 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())

        high_word = self.connect_manager.setup_client.read_holding_registers(3061, 1).registers[0]
        low_word = self.connect_manager.setup_client.read_holding_registers(3062, 1).registers[0]
        unix_timestamp = (high_word << 16) | low_word

        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
        kst_time = utc_time + timedelta(minutes=540)
        self.reset_time = kst_time
        print(kst_time)
        return self.reset_time
    
    def reset_demand(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_reset_demand.value[0], 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
    
    def reset_demand_peak(self):
        self.touch_manager.uitest_mode_start()
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_control_lock.value[0], value_control)
                time.sleep(0.6)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_reset_demand_peak.value[0], 1)
            print("Max/Min Reset")
        else:
            print(self.response.isError())
        self.reset_time = datetime.now()
        return self.reset_time
    
    def demo_test_demand(self):
        self.touch_manager.uitest_mode_start()
        addr_control_lock = 2901
        values_control = [2300, 0, 1600, 1]
        if self.connect_manager.setup_client:
            for value_control in values_control:
                self.response = self.connect_manager.setup_client.write_register(addr_control_lock, value_control)
                time.sleep(0.6)
            if self.response.isError():
                print(f"Error reading registers: {self.response}")
                return
            self.response = self.connect_manager.setup_client.read_holding_registers(ConfigMap.addr_meas_setup_access.value[0], 1)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_sync_mode.value[0], 1)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_sub_interval_time.value[0], 2)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_num_of_sub_interval.value[0], 3)
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_meas_setup_access.value[0], 1)
            demand_reset_time = self.reset_demand_peak()
            self.reset_demand()
            self.response = self.connect_manager.setup_client.write_register(ConfigMap.addr_demand_sync.value[0], 1)
        else:
            print(self.response.isError())
            
        return demand_reset_time