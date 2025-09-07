from PySide6.QtWidgets import QApplication
from aggre_dashboad import MyDashBoard
import sys

if __name__ == "__main__":
	app = QApplication(sys.argv)
	dashboard = MyDashBoard()
	dashboard.show()
	sys.exit(app.exec())