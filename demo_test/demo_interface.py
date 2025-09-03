import sys
from PySide6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import QTimer

class InterfaceUI(QDialog):
  
  def __init__(self, duration=130, parent=None):
      super().__init__(parent)
      self.setWindowTitle("Demand Test")
      self.duration = duration
      self.setup_ui()

  def setup_ui(self):
      self.remaining_time = self.duration
      layout = QVBoxLayout(self)
      
      self.message_label = QLabel(f"{self.duration}초 동안 대기해 주세요...", self)
      layout.addWidget(self.message_label)
      
      self.time_label = QLabel(f"남은 시간: {self.remaining_time}초", self)
      layout.addWidget(self.time_label)
      
      close_button = QPushButton("지금 닫기", self)
      close_button.clicked.connect(self.reject)
      layout.addWidget(close_button)
      
      self.timer = QTimer(self)
      self.timer.timeout.connect(self.update_countdown)
      self.timer.start(1000)

  def update_countdown(self):
      self.remaining_time -= 1
      self.time_label.setText(f"남은 시간: {self.remaining_time}초")
      
      if self.remaining_time <= 0:
          self.accept()

class Interface():
    
  def show_interface(self, duration):
      dialog = InterfaceUI(duration=duration)
      dialog.exec()



