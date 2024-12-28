import re

from PySide6.QtCore import QDate

from interface.widgets.message import message
from managers.DAO_classes import (
    customer_DAO,
    groups_DAO,
    project_DAO,
    stuff_DAO,
    stuff_group_DAO,
)


class extra_windows_manager:
    @staticmethod
    def add_stuff(name, surname, role, phone, address, email, birth_date):
        if extra_windows_manager.not_all_fields_filled(
            [name, surname, role, phone, address, email, birth_date]
        ):
            return

        if extra_windows_manager.incorrect_mail(email):
            return

        if extra_windows_manager.incorrect_phone(phone):
            return

        if extra_windows_manager.incorrect_age(birth_date):
            return

        if stuff_DAO.get_stuff_by_phone(phone):
            message.show_message(
                "Помилка", "Співробітник з таким номером телефона вже існує"
            )
            return

        if stuff_DAO.get_stuff_by_email(email):
            message.show_message("Помилка", "Співробітник з такою поштою вже існує")
            return

        stuff_DAO.add_stuff(
            name,
            surname,
            role,
            phone,
            address,
            email,
            birth_date.toString("yyyy-MM-dd"),
        )
        message.show_message("Успішно", "Працівника зареєстровано")

    @staticmethod
    def add_customer(name, surname, phone, address, email, birth_date):
        if extra_windows_manager.not_all_fields_filled(
            [name, surname, phone, address, email, birth_date]
        ):
            return

        if extra_windows_manager.incorrect_mail(email):
            return

        if extra_windows_manager.incorrect_phone(phone):
            return

        if extra_windows_manager.incorrect_age(birth_date):
            return

        if customer_DAO.get_customer_by_phone(phone):
            message.show_message("Помилка", "Клієнт з таким номером телефона вже існує")
            return

        if customer_DAO.get_customer_by_email(email):
            message.show_message("Помилка", "Клієнт з такою поштою вже існує")
            return

        customer_DAO.add_customer(
            name,
            surname,
            phone,
            address,
            email,
            birth_date.toString("yyyy-MM-dd"),
        )
        message.show_message("Успішно", "Клієнта зареєстровано")

    @staticmethod
    def add_project(name, group_name, customer_name, cost, paid):
        if extra_windows_manager.not_all_fields_filled(
            [name, group_name, customer_name, cost, paid]
        ):
            return

        group_id = groups_DAO.get_group_id_by_name(group_name)
        customer_id = customer_DAO.get_customer_id_by_fullname(customer_name)

        project_DAO.add_project(name, group_id, customer_id, int(cost), int(paid))
        message.show_message("Успішно", "Проєкт створено")

    @staticmethod
    def not_all_fields_filled(list):
        for item in list:
            if item == None or item == "":
                message.show_message("Помилка", "Не всі обовʼязкові поля заповнені")
                return True
        return False

    @staticmethod
    def add_group(group_name, group_list):
        if not group_name:
            message.show_message("Помилка", "Назва групи не може бути порожньою")
            return
        elif group_list == []:
            message.show_message("Помилка", "Група не може бути порожньою")
            return

        groups_DAO.add_group(group_name)

        group_id = groups_DAO.get_group_id_by_name(group_name)

        for item in group_list:
            staff_id = stuff_DAO.get_staff_id_by_fullname(item)
            stuff_group_DAO.add_stuff_to_group(staff_id, group_id)

        message.show_message("Успішно", f"Група '{group_name}' додана")

    @staticmethod
    def incorrect_mail(email):
        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.match(email_regex, email):
            message.show_message("Помилка", "Некоректний email")
            return True
        return False

    @staticmethod
    def incorrect_phone(phone):
        phone_regex = r"^\+380\d{9}$"

        if not re.match(phone_regex, phone):
            message.show_message(
                "Помилка", "Некоректний номер телефону. Формат: +380XXXXXXXXX"
            )
            return True
        return False

    @staticmethod
    def incorrect_age(birth_date):
        if birth_date.addYears(18) > QDate.currentDate():
            message.show_message("Помилка", "Вік має бути 18 років або більше")
            return True
        return False
