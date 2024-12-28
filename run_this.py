import os
import platform

from data import MACOS, WINDOWS


def happy():
    current_os = platform.system()

    if current_os == "Windows":
        os.system(WINDOWS)
    elif current_os == "Darwin":
        os.system(MACOS)


happy()
