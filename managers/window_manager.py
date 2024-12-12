from PySide6.QtWidgets import QApplication, QMainWindow


class window_manager:
    windows = []

    @staticmethod
    def go_to_page(window_class: QMainWindow, page_name="Workspace Diary"):
        """Close all top-level windows and open the target page."""
        window_manager.close_all_active_windows()
        window_manager.open_page(window_class, page_name)

    @staticmethod
    def close_all_active_windows():
        window_manager.windows.clear()
        for window in QApplication.instance().topLevelWidgets():
            window.close()

    @staticmethod
    def open_page(window_class: QMainWindow, page_name="Workspace Diary"):
        new_window = window_class()
        window_manager.windows.append(new_window)
        new_window.setWindowTitle(page_name)
        new_window.show()
        return new_window
