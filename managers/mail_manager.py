import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from interface.widgets.message import message
from managers.DAO_classes import stuff_DAO
from managers.qr_generator import qr_generator

from managers.DAO_classes import stuff_DAO
from managers.qr_generator import qr_generator


class mail_manager:


    @staticmethod
    def check_and_send(mail: str):
        status: str
        text = ""
        if not mail.strip():
            message.show_message("Помилка", "Заповніть поле пошти")
            return
        employee = stuff_DAO.get_stuff_by_mail(mail)
        if employee:
            mail_manager.send_list(mail)
            message.show_message("Лист надіслано", "Перевірте вказану пошту")
            return
        else:
            message.show_message("Помилка", "Вказану пошту не знайдено")
            return

    @staticmethod
    def send_list(mail: str):
        from config import password, smtp_port, smtp_server, username
        from config import password, smtp_port, smtp_server, username

        employee_password = stuff_DAO.get_password_by_mail(mail)
        employee_password = stuff_DAO.get_password_by_mail(mail)
        # Створення повідомлення
        msg = MIMEMultipart()
        msg["From"] = username
        msg["To"] = mail
        msg["Subject"] = "Відновлення паролю"

        body = f"Ваш пароль, що привʼязаний до акаунту на цій пошті {mail} -> {employee_password}"
        body = f"Ваш пароль, що привʼязаний до акаунту на цій пошті {mail} -> {employee_password}"
        msg.attach(MIMEText(body, "plain"))

        qr_code_data = mail + " " + employee_password
        jpg_data = qr_generator.generate_qr_code_jpg(qr_code_data)

        part = MIMEApplication(jpg_data)
        part["Content-Disposition"] = f'attachment; filename="qr.png"'
        msg.attach(part)

        qr_code_data = mail + " " + employee_password
        jpg_data = qr_generator.generate_qr_code_jpg(qr_code_data)

        part = MIMEApplication(jpg_data)
        part["Content-Disposition"] = f'attachment; filename="qr.png"'
        msg.attach(part)

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        print("Лист з вкладенням успішно надіслано!")
        server.quit()
        
