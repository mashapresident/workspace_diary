import os
import platform


def shutdown_computer():
    # Перевірка операційної системи
    current_os = platform.system()

    if current_os == "Windows":
        # Для Windows
        os.system("shutdown /s /f /t 0")
    elif current_os == "Darwin":
        # Для macOS
        os.system("sudo shutdown -h now")
    else:
        print("Unsupported OS")


# Викликаємо функцію для вимикання комп'ютера
shutdown_computer()
