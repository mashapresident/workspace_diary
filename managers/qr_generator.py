from io import BytesIO

import qrcode


class qr_generator:

    @staticmethod
    def generate_qr_code_jpg(data: str) -> bytes:
        # Створюємо QR-код
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Створюємо зображення QR-коду
        img = qr.make_image(fill="black", back_color="white")

        # Зберігаємо в JPEG форматі у байтовий потік
        with BytesIO() as output:
            img.save(output, format="JPEG")
            return output.getvalue()
