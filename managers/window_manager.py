from PySide6.QtWidgets import QApplication, QMainWindow


class window_manager:
    @staticmethod
    def go_to_page(window_class: QMainWindow):
        """Close all top-level windows and open the target page."""
        window_manager.close_all_active_windows()
        window_manager.open_page(window_class)

    @staticmethod
    def close_all_active_windows():
        for window in QApplication.instance().topLevelWidgets():
            window.close()

    @staticmethod
    def open_page(window_class: QMainWindow):
        window_manager.current_window = window_class()
        window_manager.current_window.show()
        return window_manager.current_window
    
    