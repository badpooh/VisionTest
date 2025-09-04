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
		send("out:v(1:1):a(220);p(0);f(60)")
		send("out:v(1:2):a(230);p(240);f(60)")
		send("out:v(1:3):a(240);p(120);f(60)")
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
		send("out:v(1:1):a(150);p(0);f(60)")
		send("out:v(1:2):a(160);p(240);f(60)")
		send("out:v(1:3):a(170);p(120);f(60)")
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

	def build_and_exec(self, plan):
		send = self.execute_command
		send("seq:clr")
		send("seq:begin")

		send("out:pmode(abs)")   # 첫 on은 abs
		first = True
		for step in plan:
			V = step["V"]; I = step["I"]; dur = step["duration"]

			# 3상 전압/전류 설정
			for idx, (a,p,f) in enumerate(V, start=1):
				send(f"out:v(1:{idx}):a({a});p({p});f({f})")
			for idx, (a,p,f) in enumerate(I, start=1):
				send(f"out:i(1:{idx}):a({a});p({p});f({f})")

			send("out:on")
			if first:
				send("out:pmode(diff)")  # 이후부턴 diff로 위상 점프 방지
				first = False

			# 긴 대기는 쪼개서 시퀀스에 누적
			self.long_wait(dur)

		send("out:off")
		send("seq:end")
		send("seq:exec")
		self.seq_start = time.monotonic()
		self.plan = plan
		self.durations = [s["duration"] for s in plan]

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

def fetch_and_print_report(modbus_obj, report_title):
	"""
	Modbus 장비에서 집계 데이터를 읽어와서 형식에 맞게 출력하는 함수
	"""
	print(f"\n--- [Report] {report_title} ---")
	
	# 1. 모든 관련 데이터를 한 번에 읽어옵니다.
	value_max = modbus_obj.max_read()
	value_time = modbus_obj.aggregation_max_read()
	start_sec, start_msec, start_dt, start_unix = modbus_obj.aggre_start_time_read()
	end_sec, end_msec, end_dt = modbus_obj.aggre_end_time_read()
	idx_select, idx_newest = modbus_obj.aggre_index()

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

if __name__ == "__main__":
	s1, s2, s3, s4, s5, s6, s7 = 12, 1, 30, 1, 7, 0.5, 4.3
	value = 3
	
	plan = [
		{"V":[(50,0,60),(60,240,60),(70,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s1+10},
		{"V":[(100,0,60),(110,240,60),(120,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s2},
		{"V":[(50,0,60),(60,240,60),(70,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s3},
		{"V":[(220,0,60),(230,240,60),(240,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s4},
		{"V":[(50,0,60),(60,240,60),(70,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s5},
		{"V":[(150,0,60),(160,240,60),(170,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s6},
		{"V":[(50,0,60),(60,240,60),(70,120,60)], "I":[(1,0,60),(1,240,60),(1,120,60)], "duration": s7},
	]

	cm = ConnectionManager()
	cm.start_monitoring()
	modbus = ModbusManager(connect_manager=cm)
	modbus.control_unlock()
	
	cm_engine = CMEngine()
	if cm_engine.scan_and_select_device():
		
		### --- [Phase 1] 10분 집계 테스트 및 결과 확인 ---
		modbus.aggregation_selection(value)
		cm_engine.build_and_exec(plan)
		print("-------Writing Test Start Time---------")
		modbus.unix_time_write(1756911590)
		time.sleep(10) # 쓰기 명령 후 잠시 대기
		modbus.unix_time_read() # 확인을 위해 바로 읽기
		
		# device_timeout으로 시퀀스가 끝날 때까지 기다리는 것이 더 안정적입니다.
		total_sec = sum(p["duration"] for p in plan)
		if cm_engine.device_timeout(timeout_seconds=total_sec + 120):
			print("\nSequence successfully completed.")
			
			# 시퀀스가 끝난 직후 결과 확인
			
			time.sleep(5)
			newest_idx_1 = fetch_and_print_report(modbus, f"Aggregation Mode {value}")

			### --- [Phase 2] 1시간 집계 결과 확인 ---
			modbus.aggregation_selection(value - 1) # 모드를 5 (1 hour)로 변경
			modbus.data_fetch() # 데이터 갱신 트리거
			newest_idx_2 = fetch_and_print_report(modbus, f"Aggregation Mode {value - 1}")

			### --- [Phase 3] 특정 인덱스(newest-3) 결과 확인 ---
			modbus.aggre_index_selection_update_mode(0)
			index_to_check_3 = newest_idx_2 - 3
			modbus.aggregation_index_selection(index_to_check_3)
			modbus.data_fetch()
			fetch_and_print_report(modbus, f"Specific Index {index_to_check_3}")

			### --- [Phase 4] 특정 인덱스(newest-4) 결과 확인 ---
			modbus.aggre_index_selection_update_mode(0)
			index_to_check_4 = newest_idx_2 - 4
			modbus.aggregation_index_selection(index_to_check_4)
			modbus.data_fetch()
			fetch_and_print_report(modbus, f"Specific Index {index_to_check_4}")

		else:
			print("\nSequence failed or timed out.")
			
		cm_engine.release_device()

	print("Program finished.")
	cm.tcp_disconnect()