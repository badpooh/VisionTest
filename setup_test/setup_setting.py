from PySide6.QtWidgets import QVBoxLayout, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QTableWidgetItem, QTableWidget, QHeaderView
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression, Qt, Signal, QEvent

from config.config_setting import SettingList as sl
from setup_test.ui_setting import Ui_Form
from setup_test.ui_setup_ip import Ui_setup_ip
from setup_test.setup_db import IPDataBase


class SettingWindow(QWidget, Ui_Form):
    
	tcSelected = Signal(int, str)
  
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setObjectName("My Setting")
		self.current_row = None
		self.checkbox_states = sl.DEFAULT_CHECKBOX_STATES.copy()

		for key, widget_name in sl.CHECKBOX_MAPPING:
			checkbox_widget = getattr(self, widget_name, None)
			if checkbox_widget is not None:
				checkbox_widget.stateChanged.connect(
					lambda state, k=key: self.on_checkbox_changed(state, k)
				)
			else:
				print(f"[WARNING] 위젯 '{widget_name}'를 찾을 수 없음")

		self.btn_apply.clicked.connect(self.tc_apply)
		self.btn_cancel.clicked.connect(self.close)
		
	def open_new_window(self, row):
		instance_qwidget = SettingWindow()
		instance_qwidget.setWindowTitle(f"Setting {row}")
		instance_qwidget.resize(1000, 1000)
		instance_qwidget.current_row = row
		return instance_qwidget
	
	def on_checkbox_changed(self, state, key):
		self.checkbox_states[key] = state == 2  # 2는 체크됨, 0은 체크되지 않음
		print(f"{key.capitalize()} checkbox {'checked' if state == 2 else 'unchecked'}")

		def sequence(btn_name, s, e):
			#0~50ea
			if key == btn_name:
				if state == 2:
					for cb_key, widget_name in sl.CHECKBOX_MAPPING[s:e]:
						if cb_key == btn_name:
							continue
						checkbox_widget = getattr(self, widget_name, None)
						if checkbox_widget is not None:
							checkbox_widget.setChecked(False)
							checkbox_widget.setEnabled(False)
				else:
					for cb_key, widget_name in sl.CHECKBOX_MAPPING[s:e]:
						checkbox_widget = getattr(self, widget_name, None)
						if checkbox_widget is not None:
							checkbox_widget.setEnabled(True)

		sequence('tm_all', 0, 64)
		sequence('tm_balance', 0, 64)
		sequence('tm_noload', 0, 64)
		sequence('vol_all', 3, 10)
		sequence('curr_all', 10, 19)
		sequence('pow_all', 20, 26)
		sequence('anal_all', 26, 34)
		sequence('m_s_initialize', 0, 64)
		sequence('m_s_meas_all', 36, 41)
		sequence('m_s_event_all', 41, 46)
		sequence('m_s_network_all', 46, 50)
		sequence('m_s_control_all', 50, 54)
		sequence('m_s_system_all', 54, 64)
	
	def tc_apply(self):
		selected_keys = [key for key, val in self.checkbox_states.items() if val is True]
		if selected_keys:
			text = ", ".join(selected_keys)
			self.tcSelected.emit(self.current_row, text)
			print(f"선택된 tc: {selected_keys}, row={self.current_row}")
			self.close()
		else:
			print("선택된 항목이 없습니다.")
	
class SettingIP(QWidget, Ui_setup_ip):
	
	ipSelected = Signal(str)
	tpSelected = Signal(str)
	spSelected = Signal(str)
	
	def __init__(self):
		super().__init__()
		self.setObjectName("IP Setting")
		self.setupUi(self)
		regex = QRegularExpression(r"^[0-9.]*$")
		validator = QRegularExpressionValidator(regex, self)
		self.ip_typing.setValidator(validator)
		self.ip_list.verticalHeader().setVisible(False)
		self.ip_list.horizontalHeader().setVisible(False)
		self.ip_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		
		self.btn_ip_add.clicked.connect(self.add_ip)
		self.btn_ip_select.clicked.connect(self.select_ip)
		self.btn_ip_del.clicked.connect(self.del_ip)
		self.btn_tp_add.clicked.connect(self.add_touch_port)
		self.btn_tp_select.clicked.connect(self.select_touch_port)
		self.btn_tp_del.clicked.connect(self.del_touch_port)
		self.btn_sp_add.clicked.connect(self.add_setup_port)
		self.btn_sp_select.clicked.connect(self.select_setup_port)
		self.btn_sp_del.clicked.connect(self.del_setup_port)
		
		self.db = IPDataBase()
		
		self.load_ips()

		self.ip_list.viewport().installEventFilter(self)
		self.tp_list.viewport().installEventFilter(self)
		self.sp_list.viewport().installEventFilter(self)

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseButtonPress:
			# 1) ip_list 영역에서 발생한 클릭인지
			if source is self.ip_list.viewport():
				item = self.ip_list.itemAt(event.pos())
				if item is None:
					# 빈 공간 클릭 시 선택 해제
					self.ip_list.clearSelection()
					self.ipSelected.emit("")
			# 2) tp_list 영역에서 발생한 클릭인지
			elif source is self.tp_list.viewport():
				item = self.tp_list.itemAt(event.pos())
				if item is None:
					self.tp_list.clearSelection()
					self.tpSelected.emit("")
			# 3) sp_list 영역에서 발생한 클릭인지
			elif source is self.sp_list.viewport():
				item = self.sp_list.itemAt(event.pos())
				if item is None:
					self.sp_list.clearSelection()
					self.spSelected.emit("")

		return super().eventFilter(source, event)

	def open_ip_window(self):
		self.show()
		
	def load_ips(self):
		self.ip_list.setRowCount(0)
		self.tp_list.setRowCount(0)
		self.sp_list.setRowCount(0)

		all_data = self.db.get_all_ips()
		
		for row_data in all_data:
			row_id, row_type, row_value = row_data  # 예: (1, 'ip', '10.10.10.1')

			if row_type == 'ip':
				ip_row_position = self.ip_list.rowCount()
				self.ip_list.insertRow(ip_row_position)

				ip_item = QTableWidgetItem(row_value)
				ip_item.setTextAlignment(Qt.AlignCenter)
				self.ip_list.setItem(ip_row_position, 0, ip_item)

			elif row_type == 'tp':
				tp_row_position = self.tp_list.rowCount()
				self.tp_list.insertRow(tp_row_position)

				tp_item = QTableWidgetItem(row_value)
				tp_item.setTextAlignment(Qt.AlignCenter)
				self.tp_list.setItem(tp_row_position, 0, tp_item)

			elif row_type == 'sp':
				sp_row_position = self.sp_list.rowCount()
				self.sp_list.insertRow(sp_row_position)

				sp_item = QTableWidgetItem(row_value)
				sp_item.setTextAlignment(Qt.AlignCenter)
				self.sp_list.setItem(sp_row_position, 0, sp_item)

			else:
				print(f"알 수 없는 type: {row_type}, value: {row_value}")
			
	def add_ip(self):
		typed_text = self.ip_typing.text()
		if not typed_text:
			return
		row_position = self.ip_list.rowCount()
		self.ip_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.ip_list.setItem(row_position, 0, item)
		self.db.add_ip(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태

	def select_ip(self):
		row = self.ip_list.currentRow()
		if row < 0:
			return

		item = self.ip_list.item(row, 0)
		if item:
			selected_ip = item.text()
			print(f"선택된 IP: {selected_ip}")
			self.ipSelected.emit(selected_ip)

	def del_ip(self):
		row = self.ip_list.currentRow()
		if row < 0:
			return

		item = self.ip_list.item(row, 0)
		if item:
			selected_ip = item.text()
			# 1) DB에서 삭제
			self.db.delete_ip(selected_ip)
			# 2) 테이블에서도 삭제
			self.ip_list.removeRow(row)
			
	def add_touch_port(self):
		typed_text = self.tp_typing.text()
		if not typed_text:
			return
		row_position = self.tp_list.rowCount()
		self.tp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.tp_list.setItem(row_position, 0, item)
		self.db.add_touch_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			print(f"선택된 TP: {selected_tp}")
			self.tpSelected.emit(selected_tp)
	
	def del_touch_port(self):
		row = self.tp_list.currentRow()
		if row < 0:
			return

		item = self.tp_list.item(row, 0)
		if item:
			selected_tp = item.text()
			self.db.delete_ip(selected_tp)
			self.tp_list.removeRow(row)
	
	def add_setup_port(self):
		typed_text = self.sp_typing.text()
		if not typed_text:
			return
		row_position = self.sp_list.rowCount()
		self.sp_list.insertRow(row_position)
		item = QTableWidgetItem(typed_text)
		item.setTextAlignment(Qt.AlignCenter)
		self.sp_list.setItem(row_position, 0, item)
		self.db.add_setup_port(typed_text)

		all_ips = self.db.get_all_ips()
		print("=== 현재 저장된 IP 목록 ===")
		for ip_row in all_ips:
			print(ip_row)  # (id, ip) 형태
			
	def select_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			print(f"선택된 SP: {selected_sp}")
			self.spSelected.emit(selected_sp)
	
	def del_setup_port(self):
		row = self.sp_list.currentRow()
		if row < 0:
			return

		item = self.sp_list.item(row, 0)
		if item:
			selected_sp = item.text()
			self.db.delete_ip(selected_sp)
			self.sp_list.removeRow(row)
    