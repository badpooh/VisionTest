from PySide6.QtWidgets import QApplication
import sys

from dashboard import MyDashBoard
from demo_test.demo_process import DemoTest


if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_mode = DemoTest()
    dashboard = MyDashBoard(test_mode_instance=test_mode)
    dashboard.show()
    sys.exit(app.exec())