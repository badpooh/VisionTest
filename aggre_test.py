from pymodbus.client import ModbusTcpClient as ModbusClient
import threading
import re, time
import win32com.client
import datetime
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ConnectionException

class ConnectionManager:

	def __init__(self):
		self.SERVER_IP = '10.10.26.155'  # 장치 IP 주소
		self.TOUCH_PORT = 5100  # 터치 포트
		self.SETUP_PORT = 502  # 설정 포트
		self.is_connected = False
		self.monitoring_thread = None 
		self.lock = threading.Lock() 
		self.touch_client = None
		self.setup_client = None
		
	def tcp_connect(self):
		if not self.SERVER_IP or not self.TOUCH_PORT or not self.SETUP_PORT:
			print("Cannot connect: IP or PORT is missing.")
			return
		
		self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
		self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

		touch_ok = self.touch_client.connect()
		setup_ok = self.setup_client.connect()

		if touch_ok and setup_ok:
			self.is_connected = True
			print("is connected")
			print(setup_ok)
			print(touch_ok)
			return True
		else:
			if not touch_ok:
				print("Failed to connect touch_client")
			if not setup_ok:
				print("Failed to connect setup_client")
			print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Connection failed. touch_ok={touch_ok}, setup_ok={setup_ok}")
			self.is_connected = False
			return False

	def check_connection(self):
		while self.is_connected:
			if not self.touch_client.is_socket_open():
				print("Touch client disconnected, reconnecting...")
				if self.touch_client.connect():
					print("touch_client connected")
			if not self.setup_client.is_socket_open():
				print("Setup client disconnected, reconnecting...")
				if self.setup_client.connect():
					print("setup_client connected")
			time.sleep(1)

	def heartbeat(self):
		"""백그라운드에서 실행될 스레드의 메인 로직"""
		while self.is_connected:
			time.sleep(300) # 30초에 한번씩만 체크
			
			with self.lock:
				if not self.is_connected:
					break
				
				client_to_check = self.setup_client
			
			if client_to_check:
				try:
					response = client_to_check.read_holding_registers(1, count=1)
					if response.isError():
						raise ConnectionException("Keep-alive read failed")
					else:
						# ★★★ 추가된 부분: 읽기 성공 시 값 출력 ★★★
						# uint16 값이므로 registers 리스트의 첫 번째 요소를 바로 사용
						value = response.registers[0]
						timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
						print(f"[{timestamp}] Keep-alive check OK. Register[1] value: {value}")

				except Exception as e:
					print(f"Keep-alive check failed: {e}. Attempting to reconnect...")
					# 연결 실패 시, 중앙 관리되는 tcp_connect 함수로 재연결 시도
					self.tcp_connect()
		print("Keep-alive thread stopped.")

	def start_monitoring(self):
		if self.tcp_connect():
			self.is_connected = True
			self.monitoring_thread = threading.Thread(target=self.heartbeat, daemon=True)
			self.monitoring_thread.start()
			print("Connection monitoring thread started.")

	def tcp_disconnect(self):
		"""연결 종료 및 스레드 정리"""
		print("Disconnecting...")
		self.is_connected = False # 스레드 종료 신호
		if self.monitoring_thread and self.monitoring_thread.is_alive():
			self.monitoring_thread.join(timeout=1) # 스레드가 끝날 때까지 잠시 기다림

		with self.lock:
			if self.touch_client:
				self.touch_client.close()
			if self.setup_client:
				self.setup_client.close()
		print("Disconnected.")

class ModbusManager():

	def __init__(self, connect_manager: ConnectionManager):
		self.connect_manager = connect_manager

	def control_unlock(self):
		values = [2300, 0, 700, 1]
		values_control = [2300, 0, 1600, 1]
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		else:
			for value in values:
				self.response = self.connect_manager.setup_client.write_register(2900, value)
				time.sleep(0.6)
			for value_control in values_control:
				self.response = self.connect_manager.setup_client.write_register(2901, value_control)
				time.sleep(0.6)
			print("Control Unlock")

	def unix_time_write(self, ts):
		# 1756180800 Tue Aug 26 2025 04:00:00 GMT+0000, Tue Aug 26 2025 13:00:00 GMT+0900 (한국 표준시)
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		
		# ts = 1756180800
		
		regs = self.connect_manager.setup_client.convert_to_registers(
			value=ts,
			data_type=self.connect_manager.setup_client.DATATYPE.UINT32,
			word_order="big",
		)
		regs_usec = self.connect_manager.setup_client.convert_to_registers(
			value=0,
			data_type=self.connect_manager.setup_client.DATATYPE.UINT32,
			word_order="big",
		)
		
		self.connect_manager.setup_client.read_holding_registers(3060)
		self.connect_manager.setup_client.write_registers(3061, regs)
		self.connect_manager.setup_client.write_registers(3063, regs_usec)
		self.connect_manager.setup_client.write_register(3060, 1)

	def unix_time_read(self):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		
		self.connect_manager.setup_client.read_holding_registers(3060, count=1)
		response = self.connect_manager.setup_client.read_holding_registers(3061, count=2)
		if response.isError():
			print("Modbus error:", response)
			return

		regs = response.registers

		sec_value = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.UINT32,  
			word_order="big",
		)
		dt_object = datetime.datetime.fromtimestamp(sec_value)

		response = self.connect_manager.setup_client.read_holding_registers(3063, count=2)
		if response.isError():
			print("Modbus error:", response)
			return

		regs = response.registers

		msec_value = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.UINT32,  
			word_order="big",
		)

		print(f"Unix Time: {sec_value}, 현재 시간: {dt_object}.{msec_value:06d}")

	def max_read(self):
		if not self.connect_manager.setup_client or not self.connect_manager.setup_client.is_socket_open():
			print("ERROR: Connection is not active right before read. Please check network or device.")
			return None # 에러 상황이므로 None 반환
		
		response = self.connect_manager.setup_client.read_holding_registers(31000, count=2)
		if response.isError():
			print("Modbus error:", response)
			return

		regs = response.registers

		value = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.FLOAT32,  
			word_order="big",
		)
		return value

	def aggregation_selection(self, value):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return

		self.connect_manager.setup_client.write_register(14900, value)

	def aggre_index_selection_update_mode(self, value):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		
		self.connect_manager.setup_client.write_register(14901, value)
	
	def aggregation_index_selection(self, value):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		
		self.connect_manager.setup_client.write_register(14903, value)
		response = self.connect_manager.setup_client.read_holding_registers(14903, count=1)
		regs = response.registers

		index_selection = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT16,  
			word_order="big",
		)

		return index_selection

	def aggregation_max_read(self):
		response = self.connect_manager.setup_client.read_holding_registers(31300, count=2)
		if response.isError():
			print("Modbus error:", response)
			return

		regs = response.registers

		value = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT32,  
			word_order="big",
		)
		return value

	def aggre_start_time_read(self):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
		response = self.connect_manager.setup_client.read_holding_registers(14913, count=2)
		regs = response.registers

		value_sec = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT32,  
			word_order="big",
		)

		response = self.connect_manager.setup_client.read_holding_registers(14915, count=1)
		regs = response.registers

		value_msec = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT16,  
			word_order="big",
		)
		sum_start_time = value_sec + value_msec/1000
		dt_start_1 = datetime.datetime.fromtimestamp(sum_start_time)

		return value_sec, value_msec, dt_start_1, sum_start_time
	
	def aggre_end_time_read(self):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
		response = self.connect_manager.setup_client.read_holding_registers(14916, count=2)
		regs = response.registers

		value_sec = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT32,  
			word_order="big",
		)

		response = self.connect_manager.setup_client.read_holding_registers(14918, count=1)
		regs = response.registers

		value_msec = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT16,  
			word_order="big",
		)

		sum_end_time = value_sec + value_msec/1000
		dt_end_1 = datetime.datetime.fromtimestamp(sum_end_time)

		return value_sec, value_msec, dt_end_1
	
	def aggre_index(self):
		if self.connect_manager.setup_client is None:
			print("setup_client가 연결되어 있지 않습니다.")
			return
		
		response = self.connect_manager.setup_client.read_holding_registers(14903, count=1)
		regs = response.registers

		index_selection = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT16,  
			word_order="big",
		)

		response = self.connect_manager.setup_client.read_holding_registers(14905, count=1)
		regs = response.registers

		index_newest = self.connect_manager.setup_client.convert_from_registers(
			registers=regs,
			data_type=self.connect_manager.setup_client.DATATYPE.INT16,  
			word_order="big",
		)

		return index_selection, index_newest
	
	def data_fetch(self):
		self.connect_manager.setup_client.read_holding_registers(14910, count=1)


		
class CMEngine():

	def __init__(self):
		"""CMEngine 클래스 초기화"""
		# self.modbus_manager = modbus_manager
		self.device_id = 0
		self.device_list = []
		self.device_locked = False
		self.cm_engine = win32com.client.Dispatch("OMICRON.CMEngAL")
		print("CMEngine initialized.")

	def scan_and_select_device(self):
		self.devlog("Scanning for devices...")
		self.cm_engine.DevScanForNew(False)
		device_str = self.cm_engine.DevGetList(0)
		
		devices = [dev.split(',') for dev in device_str.split(';') if dev]
		
		if not devices:
			self.devlog("No devices found!")
			return False
		
		self.device_list = devices
		self.devlog("Devices found:")
		for device in self.device_list:
			self.devlog(f"  - {device}")
		
		try:
			self.device_id = int(self.device_list[0][0])
			self.cm_engine.DevLock(self.device_id)
			self.device_locked = True
			serial = self.cm_engine.SerialNumber(self.device_id)
			ip_address = self.cm_engine.IPAddress(self.device_id)
			self.devlog(f"Device locked: {serial} - {ip_address}")
			return True
		except Exception as e:
			self.devlog(f"Failed to lock device. Error: {e}")
			return False

	def release_device(self):
		if self.device_locked:
			self.cm_engine.DevUnlock(self.device_id)
			self.device_locked = False
			self.devlog("Device unlocked.")

	def execute_command(self, cmd):
		try:
			# print(f"Exec cmd: {cmd}")
			self.cm_engine.Exec(self.device_id, cmd)
		except Exception as e:
			print(f"Failed to execute command '{cmd}'. Error: {e}")

	def query_command(self, cmd):
		try:
			# print(f"Exec query: {cmd}")
			response = self.cm_engine.Exec(self.device_id, cmd)
			# print(f"Query response: '{response}'")
			return response
		except Exception as e:
			print(f"Failed to execute query '{cmd}'. Error: {e}")
			return None
		
	def long_wait(self, total_seconds, chunk_seconds=300):
		"""
		긴 대기 시간을 여러 번의 짧은 seq:wait 명령으로 나누어 실행합니다.
		"""
		remaining_seconds = total_seconds
		while remaining_seconds > 0:
			# 남은 시간과 최대 대기 시간 중 더 작은 값을 선택
			wait_time = min(remaining_seconds, chunk_seconds)
			
			print(f"Waiting for {wait_time} seconds... ({remaining_seconds} seconds remaining)")
			# self.execute_command를 사용하여 명령 실행
			self.execute_command(f"seq:wait({wait_time}, 1)")
			
			remaining_seconds -= wait_time
			
		print("Long wait finished.")

	def cmc_setting(self, v1):
		send = self.execute_command
		
		send("seq:clr")
		send("seq:begin")

		send(f"out:v(1:1):a({v1});p(0);f(60)")
		send("out:v(1:2):a({v2});p(240);f(60)")
		send("out:v(1:3):a(110);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")

		send("out:on")

		send("seq:wait(5, 1)")

		send("out:off")

		send("seq:end")
		
		print("--- Sequence definition complete. Executing... ---")
		send("seq:exec")


	def cmc_output_single(self, first_time, peak_time, end_time):
		send = self.execute_command
		f_time = first_time + 10
		p_time = peak_time
		e_time = end_time
		
		send("seq:clr")
		send("seq:begin")

		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(50);p(240);f(60)")
		send("out:v(1:3):a(50);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")

		self.long_wait(f_time)

		send("out:v(1:1):a(220);p(0);f(60)")
		send("out:v(1:2):a(220);p(240);f(60)")
		send("out:v(1:3):a(220);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")

		self.long_wait(p_time)

		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(50);p(240);f(60)")
		send("out:v(1:3):a(50);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")

		self.long_wait(e_time)

		send("out:off")

		send("seq:end")
		
		print("--- Sequence definition complete. Executing... ---")
		send("seq:exec")

	def cmc_output_case1(self, step1, step2, step3, step4, step5, step6, step7):
		send = self.execute_command
		s1 = step1 + 10
		s2 = step2
		s3 = step3
		s4 = step4
		s5 = step5
		s6 = step6
		s7 = step7
		
		### Step 1 ###
		send("seq:clr")
		send("seq:begin")

		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(60);p(240);f(60)")
		send("out:v(1:3):a(70);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s1)

		### Step 2 ###
		send("out:v(1:1):a(100);p(0);f(60)")
		send("out:v(1:2):a(110);p(240);f(60)")
		send("out:v(1:3):a(120);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s2)

		### Step 3 ###
		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(60);p(240);f(60)")
		send("out:v(1:3):a(70);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s3)

		### Step 4 ###
		send("out:v(1:1):a(150);p(0);f(60)")
		send("out:v(1:2):a(160);p(240);f(60)")
		send("out:v(1:3):a(170);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s4)

		### Step 5 ###
		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(60);p(240);f(60)")
		send("out:v(1:3):a(70);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s5)

		### Step 6 ###
		send("out:v(1:1):a(220);p(0);f(60)")
		send("out:v(1:2):a(230);p(240);f(60)")
		send("out:v(1:3):a(240);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s6)

		### Step 7 ###
		send("out:v(1:1):a(50);p(0);f(60)")
		send("out:v(1:2):a(60);p(240);f(60)")
		send("out:v(1:3):a(70);p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(s7)

		send("out:off")

		send("seq:end")
		
		print("--- Sequence definition complete. Executing... ---")
		send("seq:exec")
	
	def device_timeout(self, timeout_seconds=None):
		print("Waiting for sequence to finish by polling status...")
		start_time = time.time()
		
		while True:
			if time.time() - start_time > timeout_seconds:
				print(f"\nError: Sequence did not finish within {timeout_seconds} seconds. (Timeout)")
				return False

			response = self.query_command("seq:status?(step)")
			if response is None:
				time.sleep(0.5)
				continue

			try:
				step_str = response.split(',')[1]
				current_step = int(step_str.strip().strip(';'))
				
				if current_step == 0:
					# 루프가 끝나기 전 줄바꿈을 해줘서 다음 출력이 깔끔하게 나오도록 함
					print("\nSequence has finished (current step is 0).")
					return True
				else:
					print(f"\rSequence is running... (current step: {current_step})", end="")

			except (IndexError, ValueError):
				print(f"\nWarning: Could not parse step from response: '{response}'. Retrying...")

			time.sleep(0.2)

	def devlog(self, msg):
		"""로그 메시지를 콘솔에 출력합니다."""
		print(msg)


if __name__ == "__main__":
	s1 = 32
	s2 = 2
	s3 = 33
	s4 = 1
	s5 = 220
	s6 = 3
	s7 = 9.3
	value = 4
	cm = ConnectionManager()
	cm.start_monitoring()
	modbus = ModbusManager(connect_manager=cm)
	modbus.control_unlock()
	modbus.aggregation_selection(value)

	cm_engine = CMEngine()
	if cm_engine.scan_and_select_device():
		cm_engine.cmc_output_case1(s1, s2, s3, s4, s5, s6, s7)
		print("-------테스트 시작 시간---------")
		modbus.unix_time_write(1756180790)
		time.sleep(10)
		modbus.unix_time_read()
		time.sleep(s1 + s2 + s3 + s4 + s5 + s6 + s7)
		print("----------결과-----------")
		value_max_1 = modbus.max_read()
		value_time_1 = modbus.aggregation_max_read()
		value_start_time_sec_1, value_start_time_msec_1, dt_start_1, sum_start_time_1 = modbus.aggre_start_time_read()
		value_end_time_sec_1, value_end_time_msec_1, dt_end_1 = modbus.aggre_end_time_read()
		peak_unixtime_1 = sum_start_time_1 + (value_time_1/1000)
		peak_datetime_1 = datetime.datetime.fromtimestamp(peak_unixtime_1)

		print(f"Aggregation {value}\n 전압: {value_max_1} \n PeakTime: {peak_datetime_1} \n Timeoffest: {value_time_1}")
		print(f"시작시간(Unix): {value_start_time_sec_1} + {value_start_time_msec_1} / 시간: {dt_start_1}")
		print(f"종료시간(Unix): {value_end_time_sec_1} + {value_end_time_msec_1} / 시간: {dt_end_1}")
		index_selection_1, index_newest_1 = modbus.aggre_index()
		print(f"index selec: {index_selection_1}, index newest: {index_newest_1}")

		print("------------------------")

		modbus.aggregation_selection(value-1)
		modbus.data_fetch()
		value_max_2 = modbus.max_read()
		value_time_2 = modbus.aggregation_max_read()
		value_start_time_sec_2, value_start_time_msec_2, dt_start_2, sum_start_time_2= modbus.aggre_start_time_read()
		value_end_time_sec_2, value_end_time_msec_2, dt_end_2 = modbus.aggre_end_time_read()
		peak_unixtime_2 = sum_start_time_2 + (value_time_2/1000)
		peak_datetime_2 = datetime.datetime.fromtimestamp(peak_unixtime_2)
		print(f"Aggregation {value - 1}\n 전압: {value_max_2} \n PeakTime: {peak_datetime_2} \n Timeoffest: {value_time_2}")
		print(f"시작시간(Unix): {value_start_time_sec_2} + {value_start_time_msec_2} / 시간: {dt_start_2}")
		print(f"종료시간(Unix): {value_end_time_sec_2} + {value_end_time_msec_2} / 시간: {dt_end_2}")
		index_selection_2, index_newest_2 = modbus.aggre_index()
		print(f"index selec: {index_selection_2}, index newest: {index_newest_2}")

		print("------------------------")

		modbus.aggre_index_selection_update_mode(0)
		index_selection3 = modbus.aggregation_index_selection(index_newest_2-3)
		modbus.data_fetch()
		value_max_3 = modbus.max_read()
		value_time_3 = modbus.aggregation_max_read()
		value_start_time_sec_3, value_start_time_msec_3, dt_start_3, sum_start_time_3 = modbus.aggre_start_time_read()
		value_end_time_sec_3, value_end_time_msec_3, dt_end_3 = modbus.aggre_end_time_read()
		peak_unixtime_3 = sum_start_time_3 + (value_time_3/1000)
		peak_datetime_3 = datetime.datetime.fromtimestamp(peak_unixtime_3)
		print(f"Aggregation {value - 1}\n 전압: {value_max_3} \n PeakTime: {peak_datetime_3} \n Timeoffest: {value_time_3}")
		print(f"시작시간(Unix): {value_start_time_sec_3} + {value_start_time_msec_3} / 시간: {dt_start_3}")
		print(f"종료시간(Unix): {value_end_time_sec_3} + {value_end_time_msec_3} / 시간: {dt_end_3}")
		print(f"index newest: {index_selection3}")
		index_selection_3, index_newest_3 = modbus.aggre_index()
		print(f"index selec: {index_selection_3}, index newest: {index_newest_3}")
		
		print("------------------------")

		modbus.aggre_index_selection_update_mode(0)
		index_selection4 = modbus.aggregation_index_selection(index_newest_2-4)
		modbus.data_fetch()
		value_max_4 = modbus.max_read()
		value_time_4 = modbus.aggregation_max_read()
		value_start_time_sec_4, value_start_time_msec_4, dt_start_4, sum_start_time_4 = modbus.aggre_start_time_read()
		value_end_time_sec_4, value_end_time_msec_4, dt_end_4 = modbus.aggre_end_time_read()
		peak_unixtime_4 = sum_start_time_4 + (value_time_4/1000)
		peak_datetime_4 = datetime.datetime.fromtimestamp(peak_unixtime_4)
		print(f"Aggregation {value - 1}\n 전압: {value_max_4} \n PeakTime: {peak_datetime_4} \n Timeoffest: {value_time_4}")
		print(f"시작시간(Unix): {value_start_time_sec_4} + {value_start_time_msec_4} / 시간: {dt_start_4}")
		print(f"종료시간(Unix): {value_end_time_sec_4} + {value_end_time_msec_4} / 시간: {dt_end_4}")
		print(f"index newest: {index_selection4}")
		index_selection_4, index_newest_4 = modbus.aggre_index()
		print(f"index selec: {index_selection_4}, index newest: {index_newest_4}")

		if cm_engine.device_timeout(timeout_seconds=120):
			print("\nSequence successfully completed.")
		else:
			print("\nSequence failed or timed out.")
		cm_engine.release_device()
	print("Program finished.")
	
	cm.tcp_disconnect()