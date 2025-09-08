from PySide6.QtWidgets import QApplication
from aggre_dashboad import MyDashBoard
from aggre_function import ConnectionManager, CMEngine
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    connection_manager = ConnectionManager()
    cm_engine = CMEngine()
    dashboard = MyDashBoard(connection_manager, cm_engine)
    
    dashboard.show()
    sys.exit(app.exec())