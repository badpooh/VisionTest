from PySide6.QtWidgets import QApplication
import sys

from dashboard import MyDashBoard
from setup_test.setup_process import SetupTest
from demo_test.demo_process import DemoTest


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setup_test = SetupTest()
    test_mode = DemoTest()
    dashboard = MyDashBoard(setup_test_instance=setup_test, test_mode_instance=test_mode)
    dashboard.cb_AccuraSMChanged.connect(setup_test.on_accurasm_checked)
    dashboard.show()
    sys.exit(app.exec())