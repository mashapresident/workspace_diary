from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QGuiApplication, QImage, QPixmap

from interface.widgets.message import message
from interface.windows.qr_page import qr_page
from managers.login_manager import login_manager
from managers.qr_scanner.qr_scanner_thread import qr_scanner_thread
from managers.window_manager import window_manager


class qr_manager:
    thread = None
    qr_page = None

    @staticmethod
    def scann_qr_code_from_cam():
        if qr_manager.qr_page:
            return
        qr_manager.qr_page = window_manager.open_page(qr_page)
        qr_manager.start_thread()

    @staticmethod
    def start_thread():
        if not qr_manager.thread:
            qr_manager.thread = qr_scanner_thread()
            qr_manager.thread.qr_data_received.connect(qr_manager.handle_qr)
            qr_manager.thread.image_received.connect(qr_manager.qr_page.update_image)
            qr_manager.qr_page.close_page.connect(qr_manager.closeEvent)
            qr_manager.thread.start()

    @staticmethod
    @Slot(str)
    def handle_qr(qr_data):
        qr_manager.thread.stop()
        entry_data = qr_data.split(" ")
        try:
            email = entry_data[0]
            password = entry_data[1]
            login_manager.login_by_mail(email, password)
        except IndexError:
            qr_manager.qr_page.close()
            message.show_message("Помилка", "З Qr кодом щось не так")

    @staticmethod
    @Slot(bool)
    def closeEvent():
        if qr_manager.thread.isRunning():
            qr_manager.thread.stop()
            qr_manager.qr_page = None
            qr_manager.thread = None
