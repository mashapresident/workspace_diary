from interface.widgets.message import message
from interface.windows.manager_page import manager_page
from interface.windows.stuff_page import stuff_page
from managers.DAO_classes import stuff_DAO
from managers.window_manager import window_manager


class login_manager:
    @staticmethod
    def login_by_mail(mail: str, input_password: str) -> None:
        if not mail.strip():
            message.show_message("Помилка", "Заповніть поле пошти")
            return
        elif not input_password.strip():
            message.show_message("Помилка", "Заповніть поле пароль")
            return

        stuff_record = stuff_DAO.get_stuff_by_mail(mail)

        if not stuff_record or stuff_record.password != input_password:
            message.show_message("Помилка", "Неправильні дані")
            return

        login_manager.enter_account(stuff_record)

    @staticmethod
    def is_input_invalid(mail: str, input_password: str) -> bool:
        """Checks if the input fields are empty or whitespace."""
        return not mail.strip() or not input_password.strip()

    @staticmethod
    def enter_account(stuff_record):
        """Redirect to the appropriate account page based on role."""
        target_page = (
            manager_page if stuff_record.role.lower() == "manager" else stuff_page
        )
        window_manager.go_to_page(lambda: target_page(stuff_record))
