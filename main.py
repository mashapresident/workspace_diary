import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication



class AppState:
    person = None
    
    
    @staticmethod
    def start():
        app = QApplication(sys.argv)
        icon = QIcon("./interface/assets/final_icon.png")
        app.setWindowIcon(icon)
        
        
        from interface.windows.login_page import login_page
        from managers.window_manager import window_manager
        window_manager.open_page(login_page)
        sys.exit(app.exec())


if __name__ == "__main__":
    AppState.start()
