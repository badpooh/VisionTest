from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QObject, Signal
import sys
import time
import threading
import pythoncom

from aggre_ui import Ui_Form
from aggre_function import ConnectionManager, CMEngine, ModbusManager

class StreamEmitter(QObject):
	textWritten = Signal(str)

	def write(self, text):
		self.textWritten.emit(str(text))
	
	def flush(self):
		pass

class MyDashBoard(QMainWindow, Ui_Form):
	
	# 테스트 완료 시그널 정의
	test_finished_signal = Signal()

	def __init__(self, connection_manager: ConnectionManager, cm_engine: CMEngine):
		super().__init__()
		self.setupUi(self)
		self.setWindowTitle("Aggreagion Test v1.0")

		self.connection_manager = connection_manager
		# self.cm_engine = cm_engine # 더 이상 메인 스레드에서는 cm_engine을 직접 사용하지 않음
		self.modbus_manager = ModbusManager(self.connection_manager)

		self.log_stream = StreamEmitter()
		self.log_stream.textWritten.connect(self.append_log_text)
		sys.stdout = self.log_stream
		sys.stderr = self.log_stream

		print("UI logger initialized.")

		# --- 시그널/슬롯 연결 ---
		self.btn_connect.clicked.connect(self.on_connect_clicked)
		self.btn_disconnect.clicked.connect(self.on_disconnect_clicked)
		self.btn_start.clicked.connect(self.test_start)
		self.btn_stop.clicked.connect(self.test_stop)
		self.test_finished_signal.connect(self.on_test_finished)

		self.test_stop_event = threading.Event()

	def on_connect_clicked(self):
		ip_address = self.lineEdit_ip.text()
		self.connection_manager.ip_connect(ip_address)
		self.connection_manager.sp_update(502)
		self.connection_manager.start_monitoring()

	def on_disconnect_clicked(self):
		self.connection_manager.tcp_disconnect()

	def on_test_finished(self):
		"""테스트가 완료되었을 때 UI를 업데이트하는 슬롯"""
		print("--- All test sequences finished ---")
		self.btn_start.setEnabled(True) # 시작 버튼 다시 활성화
		self.btn_stop.setEnabled(False)
	
	def test_stop(self):
		print("--- STOP button clicked. Sending stop signal to test thread... ---")
		self.test_stop_event.set()
 
	def test_start(self):
		"""'START' 버튼 클릭 시 실행: 값 파싱 및 작업자 스레드 시작"""
		try:
			value = int(self.index_1.text())
			s1 = float(self.lineEdit_time1.text())
			s2 = float(self.lineEdit_time2.text())
			s3 = float(self.lineEdit_time3.text())
			s4 = float(self.lineEdit_time4.text())
			s5 = float(self.lineEdit_time5.text())
			s6 = float(self.lineEdit_time6.text())
			s7 = float(self.lineEdit_time7.text())
			v_s1 = float(self.lineEdit_source1.text())
			v_s2 = float(self.lineEdit_source2.text())
			v_s3 = float(self.lineEdit_source3.text())
			v_s4 = float(self.lineEdit_source4.text())
			v_s5 = float(self.lineEdit_source5.text())
			v_s6 = float(self.lineEdit_source6.text())
			v_s7 = float(self.lineEdit_source7.text())
			self.idx_minus_num_1 = int(self.index_2.text())
			self.idx_minus_num_2 = int(self.index_3.text())
		except ValueError:
			print("Error: 모든 값에 유효한 숫자를 입력해야 합니다.")
			return

		print("--- Starting test in background thread ---")
		self.test_stop_event.clear() # 새 테스트 시작 전 이벤트 초기화
		self.btn_start.setEnabled(False) # 테스트 중 버튼 비활성화
		self.btn_stop.setEnabled(True)

		# 작업자 스레드를 생성하고 시작
		test_thread = threading.Thread(
			target=self.run_full_test_sequence,
			args=(self.test_stop_event, value, s1, s2, s3, s4, s5, s6, s7, v_s1, v_s2, v_s3, v_s4, v_s5, v_s6, v_s7) # 필요한 모든 값을 전달
		)
		test_thread.daemon = True
		test_thread.start()

	def run_full_test_sequence(self, stop_event, value, s1, s2, s3, s4, s5, s6, s7, v_s1, v_s2, v_s3, v_s4, v_s5, v_s6, v_s7):
		pythoncom.CoInitialize()
		thread_cm_engine = CMEngine()
		self.modbus_manager.control_unlock()
		try:
			if thread_cm_engine.connect():
				# --- [Phase 1] 테스트 실행 및 결과 확인 ---
				self.modbus_manager.aggregation_selection(value)
				thread_cm_engine.build_and_exec(stop_event, s1, s2, s3, s4, s5, s6, s7, v_s1, v_s2, v_s3, v_s4, v_s5, v_s6, v_s7) # v_s 값들도 전달 필요
				
				if stop_event.is_set(): raise InterruptedError("Test stopped by user.")

				print("-------Writing Test Start Time---------")
				self.modbus_manager.unix_time_write(1756911590)
				time.sleep(10) # 쓰기 명령 후 잠시 대기
				if stop_event.is_set(): raise InterruptedError("Test stopped by user.")
				self.modbus_manager.unix_time_read()

				_, initial_newest_index = self.modbus_manager.aggre_index()
				print(f"Initial newest index: {initial_newest_index}")
				
				total_sec = s1 + 10 + s2 + s3 + s4 + s5 + s6 + s7
				if thread_cm_engine.device_timeout(stop_event, timeout_seconds=total_sec + 120):
					if stop_event.is_set(): raise InterruptedError("Test stopped by user.")

					self.modbus_manager.unix_time_read()
					print("\nSequence successfully completed.")
					
					# ★★★ 추가된 폴링 로직 ★★★
					# 2. Modbus 장비의 집계가 완료될 때까지 '최신 인덱스'가 바뀔 때까지 기다립니다.
					print("Waiting for Modbus device to update aggregation data...")
					polling_start_time = time.time()
					while True:
						if stop_event.is_set(): raise InterruptedError("Test stopped by user.")

						_, current_newest_index = self.modbus_manager.aggre_index()
						# 인덱스가 바뀌었다는 것은 새 데이터가 저장되었다는 의미
						if current_newest_index > initial_newest_index:
							print(f"Modbus data updated! (Index changed from {initial_newest_index} to {current_newest_index})")
							break
						# 폴링 타임아웃 (최대 10초)
						if time.time() - polling_start_time > 10:
							print("Polling timeout: Modbus index did not update.")
							break
						time.sleep(0.1) # 0.1초 간격으로 빠르게 확인
					# ★★★

					if stop_event.is_set(): raise InterruptedError("Test stopped by user.")

					# 3. 이제 최종 데이터가 준비되었으므로 결과 확인
					newest_idx_1 = self.modbus_manager.fetch_and_print_report(f"Aggregation Mode {value}")


					### --- [Phase 2]
					if stop_event.is_set(): raise InterruptedError("Test stopped by user.")
					self.modbus_manager.aggregation_selection(value - 1) # 모드를 5 (1 hour)로 변경
					self.modbus_manager.data_fetch() # 데이터 갱신 트리거
					newest_idx_2 = self.modbus_manager.fetch_and_print_report(f"Aggregation Mode {value - 1}")

					### --- [Phase 3] 특정 인덱스(newest-3) 결과 확인 ---
					if stop_event.is_set(): raise InterruptedError("Test stopped by user.")
					self.modbus_manager.aggre_index_selection_update_mode(0)
					index_to_check_3 = newest_idx_2 - self.idx_minus_num_1
					self.modbus_manager.aggregation_index_selection(index_to_check_3)
					self.modbus_manager.data_fetch()
					self.modbus_manager.fetch_and_print_report(f"Specific Index {index_to_check_3}")

					### --- [Phase 4] 특정 인덱스(newest-4) 결과 확인 ---
					if stop_event.is_set(): raise InterruptedError("Test stopped by user.")
					self.modbus_manager.aggre_index_selection_update_mode(0)
					index_to_check_4 = newest_idx_2 - self.idx_minus_num_2
					self.modbus_manager.aggregation_index_selection(index_to_check_4)
					self.modbus_manager.data_fetch()
					self.modbus_manager.fetch_and_print_report(f"Specific Index {index_to_check_4}")
					
				else:
					if stop_event.is_set():
						print("\nSequence execution was cancelled by user.")
					else:
						print("\nSequence failed or timed out.")
				
		except InterruptedError as e:
			print(f"\n[INFO] {e}")
		finally:
			# OMICRON 시퀀스 중지 및 연결 해제
			if thread_cm_engine and thread_cm_engine.device_locked:
				print("Stopping OMICRON sequence and releasing device...")
				thread_cm_engine.execute_command("out:off") # 출력 비활성화
				thread_cm_engine.execute_command("seq:stop") # 시퀀스 정지
				thread_cm_engine.release_device()
			pythoncom.CoUninitialize()
			# 테스트 완료 후 메인 스레드에 신호 보내기
			self.test_finished_signal.emit()

	def append_log_text(self, text):
		"""textWritten 시그널이 발생하면, 전달받은 텍스트를 QTextEdit에 추가합니다."""
		# 1. 빈 줄은 추가하지 않도록 합니다.
		log_text = text.strip()
		if not log_text:
			return

		# 2. QTextEdit의 append 메소드를 사용하여 텍스트를 새 줄에 추가합니다.
		self.log_print.append(log_text)
		
		# 3. 스크롤바를 항상 맨 아래로 이동시켜 최신 로그를 보여줍니다.
		scrollbar = self.log_print.verticalScrollBar()
		scrollbar.setValue(scrollbar.maximum())