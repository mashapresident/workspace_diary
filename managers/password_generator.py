import random
import string

class password_generator:
    @staticmethod
    def generate_password() -> str:
        # Генерация 3 случайных цифр
        digits = ''.join(random.choices(string.digits, k=3))
        # Генерация 3 случайных букв
        letters = ''.join(random.choices(string.ascii_letters, k=3))
        # Объединение и перемешивание
        password = list(digits + letters)
        return ''.join(password)

# Пример использования
print(password_generator.generate_password())