from pymodbus.client import ModbusTcpClient as ModbusClient
import pythoncom
import threading
import re, time
import win32com.client
import datetime
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ConnectionException

class ConnectionManager:

	_instance = None
	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super(ConnectionManager, cls).__new__(cls)
		return cls._instance

	def __init__(self):
		if not hasattr(self, 'initialized'):
			self.SERVER_IP = None 
			# self.TOUCH_PORT = 5100
			# self.SETUP_PORT = 502
			self.SETUP_PORT = None
			self.is_connected = False
			self.monitoring_thread = None 
			self.lock = threading.Lock() 
			self.touch_client = None
			self.setup_client = None
			self.initialized = True
			
	def ip_connect(self, selected_ip):
		self.SERVER_IP = selected_ip
		print(f"IP set to: {self.SERVER_IP}")
			
	# def tp_update(self, selected_tp):
	# 	self.TOUCH_PORT = selected_tp
	
	def sp_update(self, selected_sp):
		self.SETUP_PORT = selected_sp
		
	def tcp_connect(self):
		if not self.SERVER_IP or not self.SETUP_PORT:
			print("Cannot connect: IP or PORT is missing.")
			return
		
		# self.touch_client = ModbusClient(self.SERVER_IP, port=self.TOUCH_PORT)
		self.setup_client = ModbusClient(self.SERVER_IP, port=self.SETUP_PORT)

		# touch_ok = self.touch_client.connect()
		setup_ok = self.setup_client.connect()

		if setup_ok:
			self.is_connected = True
			print("is connected")
			print(setup_ok)
			return True
		else:
			if not setup_ok:
				print("Failed to connect setup_client")
			print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Connection failed. setup_ok={setup_ok}")
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
			time.sleep(300)
			
			with self.lock:
				if not self.is_connected:
					break
				
				client_to_check = self.setup_client
			
			if client_to_check:
				try:
					response = client_to_check.read_holding_registers(1, count=1)
					if response.isError():
						raise ConnectionException("Heartbeat read failed")
					else:
						value = response.registers[0]
						timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
						print(f"[{timestamp}] Heartbeat check OK. Register[1] value: {value}")

				except Exception as e:
					print(f"Heartbeat check failed: {e}. Attempting to reconnect...")
					# 연결 실패 시, 중앙 관리되는 tcp_connect 함수로 재연결 시도
					self.tcp_connect()
		print("Heartbeat thread stopped.")

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

	def fetch_and_print_report(self, report_title):
		"""
		Modbus 장비에서 집계 데이터를 읽어와서 형식에 맞게 출력하는 함수
		"""
		print(f"\n--- [Report] {report_title} ---")
		
		# 1. 모든 관련 데이터를 한 번에 읽어옵니다.
		value_max = self.max_read()
		value_time = self.aggregation_max_read()
		start_sec, start_msec, start_dt, start_unix = self.aggre_start_time_read()
		end_sec, end_msec, end_dt = self.aggre_end_time_read()
		idx_select, idx_newest = self.aggre_index()

		# 2. Peak 시간 계산 (값이 None이 아닐 때만 안전하게 계산)
		peak_datetime = "Calculation Error"
		if start_unix is not None and value_time is not None:
			try:
				peak_unixtime = start_unix + (value_time / 1000)
				peak_datetime = datetime.datetime.fromtimestamp(peak_unixtime)
			except (TypeError, ValueError):
				pass # 계산 중 에러가 나도 프로그램이 멈추지 않도록 처리

		# 3. 결과를 일관된 형식으로 출력합니다.
		print(f"  Max Voltage : {value_max}")
		print(f"  Peak Time   : {peak_datetime}")
		print(f"  Time Offset : {value_time} ms")
		print(f"  Start Time  : {start_dt}")
		print(f"  End Time    : {end_dt}")
		print(f"  Index Select: {idx_select}, Index Newest: {idx_newest}")
		
		# 다음 단계에서 사용할 수 있도록 newest_index를 반환
		return idx_newest
		
class CMEngine():

	def __init__(self):
		self.device_id = 0
		self.device_list = []
		self.device_locked = False
		self.cm_engine = None

	def connect(self):
		"""COM 객체를 생성하고 장치를 스캔하여 잠급니다."""
		# 이미 연결된 경우 다시 시도하지 않음
		if self.device_locked:
			print("Device is already connected and locked.")
			return True
		
		try:
			print("Initializing COM and connecting to CMEngine...")
			# COM 라이브러리 초기화 (스레드 충돌 방지)
			pythoncom.CoInitialize()
			self.cm_engine = win32com.client.Dispatch("OMICRON.CMEngAL")
		except Exception as e:
			print(f"FATAL: Failed to create CMEngine COM object. Check if OMICRON software is installed. Error: {e}")
			self.cm_engine = None
			return False

		# 기존의 scan_and_select_device 로직을 여기에 통합
		if self.scan_and_select_device():
			return True
		else:
			# 실패 시 COM 객체 정리
			self.cm_engine = None
			return False

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
		
	def long_wait(self, stop_event, total_seconds, chunk_seconds=300):
		"""
		긴 대기 시간을 여러 번의 짧은 seq:wait 명령으로 나누어 실행합니다.
		"""
		remaining_seconds = total_seconds
		while remaining_seconds > 0:
			# 남은 시간과 최대 대기 시간 중 더 작은 값을 선택
			if stop_event.is_set():
				print("Stop signal received during long_wait. Aborting.")
				return
			wait_time = min(remaining_seconds, chunk_seconds)
			
			print(f"Waiting for {wait_time} seconds... ({remaining_seconds} seconds remaining)")
			# self.execute_command를 사용하여 명령 실행
			self.execute_command(f"seq:wait({wait_time}, 1)")
			
			remaining_seconds -= wait_time
			
		print("Long wait finished.")
	
	def device_timeout(self, stop_event, timeout_seconds=None):
		print("Waiting for sequence to finish by polling status...")
		start_time = time.time()
		
		# ★★★ 1. 마지막으로 확인된 스텝을 저장할 변수를 추가합니다 ★★★
		last_known_step = -1 # 초기값은 절대 나올 수 없는 값으로 설정

		while True:
			if stop_event.is_set():
				return False # 중단 신호가 오면 실패로 간주하고 즉시 반환
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
				
				# ★★★ 2. 현재 스텝이 마지막으로 확인된 스텝과 다를 때만 처리합니다 ★★★
				if current_step != last_known_step:
					if current_step == 0:
						print("\nSequence has finished (current step is 0).")
						return True
					else:
						# 줄바꿈(\n)을 추가하여 각 스텝 변경을 명확히 보여줍니다.
						print(f"\nSequence is now on step: {current_step}")
						# 마지막 확인된 스텝을 현재 스텝으로 업데이트합니다.
						last_known_step = current_step

			except (IndexError, ValueError):
				# 에러 메시지는 한 번만 출력하는 것이 좋습니다.
				if last_known_step != -99: # -99는 에러 상태를 의미
					print(f"\nWarning: Could not parse step from response: '{response}'.")
					last_known_step = -99 # 동일한 에러가 반복 출력되지 않도록 상태 저장

			time.sleep(0.2)

	def devlog(self, msg):
		"""로그 메시지를 콘솔에 출력합니다."""
		print(msg)

	def build_and_exec(self, stop_event, s1, s2, s3, s4, s5, s6, s7, v_s1, v_s2, v_s3, v_s4, v_s5, v_s6, v_s7):

		send = self.execute_command
		
		### Step 1 ###
		send("seq:clr")
		send("seq:begin")

		send(f"out:v(1:1):a({v_s1});p(0);f(60)")
		send(f"out:v(1:2):a({v_s1+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s1+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s1+10)

		### Step 2 ###
		send(f"out:v(1:1):a({v_s2});p(0);f(60)")
		send(f"out:v(1:2):a({v_s2+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s2+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s2)

		### Step 3 ###
		send(f"out:v(1:1):a({v_s3});p(0);f(60)")
		send(f"out:v(1:2):a({v_s3+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s3+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s3)

		### Step 4 ###
		send(f"out:v(1:1):a({v_s4});p(0);f(60)")
		send(f"out:v(1:2):a({v_s4+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s4+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s4)

		### Step 5 ###
		send(f"out:v(1:1):a({v_s5});p(0);f(60)")
		send(f"out:v(1:2):a({v_s5+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s5+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s5)

		### Step 6 ###
		send(f"out:v(1:1):a({v_s6});p(0);f(60)")
		send(f"out:v(1:2):a({v_s6+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s6+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s6)

		### Step 7 ###
		send(f"out:v(1:1):a({v_s7});p(0);f(60)")
		send(f"out:v(1:2):a({v_s7+10});p(240);f(60)")
		send(f"out:v(1:3):a({v_s7+20});p(120);f(60)")
		send("out:i(1:1):a(1);p(0);f(60)")
		send("out:i(1:2):a(1);p(240);f(60)") 
		send("out:i(1:3):a(1);p(120);f(60)")
		send("out:on")
		self.long_wait(stop_event, s7)

		send("out:off")

		send("seq:end")
		
		if stop_event.is_set(): return

		print("--- Sequence definition complete. Executing... ---")
		send("seq:exec")

		self.seq_start = time.monotonic()
		# self.plan = plan
		# self.durations = [s["duration"] for s in plan]

	def start_supervisor(self, total_expected_sec):
		self._supervisor_stop_evt = threading.Event()
		
		# 스레드에 필요한 device_id를 인자로 넘겨줍니다.
		args_for_thread = (self.device_id, total_expected_sec, self._supervisor_stop_evt)
		
		# target을 새로운 함수로 지정합니다.
		self._supervisor_thread = threading.Thread(target=self._supervisor_loop, args=args_for_thread, daemon=True)
		self._supervisor_thread.start()

	def _supervisor_loop(self, device_id, total_expected_sec, stop_evt):
		"""Supervisor 스레드 전용 루프 함수"""
		pythoncom.CoInitialize()
		thread_cm_engine = None
		try:
			# 1. 이 스레드 전용의 새로운 COM 객체를 생성
			thread_cm_engine = win32com.client.Dispatch("OMICRON.CMEngAL")

			# ★★★ 2. 이 스레드에서도 DevLock을 호출하여 장비를 잠급니다 ★★★
			thread_cm_engine.DevLock(device_id)
			print("Supervisor thread has successfully locked the device.")

			start_ts = time.time()
			
			while not stop_evt.is_set():
				# ... (이하 루프 로직은 동일)
				elapsed = time.time() - start_ts
				if elapsed >= total_expected_sec:
					print("Supervisor: expected duration reached.")
					break

				resp = thread_cm_engine.Exec(device_id, "seq:status?(step)")
				# ...

		except Exception as e:
			print(f"Supervisor thread encountered an error: {e}")
		finally:
			# 3. 스레드가 끝나기 전 잠금 해제도 시도 (선택 사항이지만 좋은 습관)
			# self.modbus.unix_time_read()
			if thread_cm_engine and device_id:
				try:
					thread_cm_engine.DevUnlock(device_id)
				except Exception:
					pass # 이미 해제되었을 수 있음
			
			pythoncom.CoUninitialize()
			print("Supervisor thread stopped.")

	def _compute_resume(self, elapsed):
		t=0
		for idx,d in enumerate(self.durations):
			if elapsed < t + d:
				remain = t + d - elapsed
				return idx, max(0.1, remain)  # remain 최소 0.1s
			t += d
		return None, 0

	def _recover(self, idx, remain):
		print(f"[RECOVER] restart from step {idx} with remain ~{remain:.2f}s")
		# 보호 상태 클리어: 안전차원에서
		try: self.execute_command("out:off")
		except: pass
		# 시퀀스 재작성: idx 스텝은 remain만큼, 그 뒤는 원래 duration
		plan2 = []
		step0 = dict(self.plan[idx])  # shallow copy
		step0["duration"] = remain
		plan2.append(step0)
		for k in range(idx+1, len(self.plan)):
			plan2.append(self.plan[k])
		self.build_and_exec(plan2, start_index=0, first_wait_override=remain)