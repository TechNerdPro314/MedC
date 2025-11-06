from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os

# Регистрация шрифта для поддержки кириллицы
pdfmetrics.registerFont(TTFont('DejaVuSans', 'app/fonts/DejaVuSans.ttf'))

def generate_medication_pdf(patient, doctor, appointment, medications):
    # Формируем имя папки и файла
    patient_folder = f"pdfs/{patient.last_name}_{patient.first_name}_{patient.patronymic}".replace(" ", "_")
    os.makedirs(patient_folder, exist_ok=True)

    pdf_filename = f"{patient_folder}/medications_{appointment.id}.pdf"

    # Создаём PDF
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    # === ШАПКА ОРГАНИЗАЦИИ ===
    c.setFont("DejaVuSans", 12)
    organization_name = "Медицинская организация \"Здоровье\""
    organization_address = "г. Москва, ул. Ленина, д. 10, тел.: +7 (495) 123-45-67"

    c.drawCentredString(width / 2, height - 40, organization_name)
    c.drawCentredString(width / 2, height - 60, organization_address)

    # === ЗАГОЛОВОК ДОКУМЕНТА ===
    c.setFont("DejaVuSans", 14)
    c.drawCentredString(width / 2, height - 100, "МЕДИЦИНСКОЕ НАЗНАЧЕНИЕ")

    # === ДАННЫЕ ПАЦИЕНТА И ВРАЧА ===
    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 140, f"Пациент: {patient.last_name} {patient.first_name} {patient.patronymic}")

    # Обработка даты рождения
    date_of_birth = "Не указано"
    if patient.date_of_birth:
        possible_formats = ["%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"]
        for fmt in possible_formats:
            try:
                parsed_date = datetime.strptime(patient.date_of_birth.strip(), fmt)
                date_of_birth = parsed_date.strftime('%d.%m.%Y')
                break
            except ValueError:
                continue
        else:
            date_of_birth = f"Некорректный формат ({patient.date_of_birth})"

    c.drawString(50, height - 160, f"Дата рождения: {date_of_birth}")
    c.drawString(50, height - 180, f"Телефон пациента: {patient.phone}")
    c.drawString(50, height - 200, f"Адрес: {patient.address}")
    c.drawString(50, height - 220, f"Полис страхования: {patient.insurance_policy}")

    c.drawString(50, height - 260, f"Лечащий врач: {doctor.last_name} {doctor.first_name} {doctor.patronymic}")
    c.drawString(50, height - 280, f"Специализация: {doctor.specialization}")

    # Обработка даты приёма
    appointment_date_str = appointment.appointment_day.strftime('%d.%m.%Y') if appointment.appointment_day else "Не указано"
    c.drawString(50, height - 300, f"Дата приёма: {appointment_date_str}")
    c.drawString(50, height - 320, f"Время приёма: {appointment.appointment_time}")
    c.drawString(50, height - 340, f"Оказанная услуга: {appointment.service}")

    # === НАЗНАЧЕННЫЕ ЛЕКАРСТВА ===
    c.setFont("DejaVuSans", 12)
    c.drawString(50, height - 380, "Назначенные лекарства:")

    y = height - 410
    if medications:
        for idx, med in enumerate(medications, 1):
            c.drawString(60, y, f"{idx}. {med.medication_name}, дозировка: {med.dosage}")
            y -= 20
    else:
        c.drawString(60, y, "Нет назначенных лекарств.")
        y -= 20

    # === ПОДПИСЬ И ПЕЧАТЬ ===
    y_footer = 120
    c.setFont("DejaVuSans", 12)

    # Линия для подписи врача
    c.drawString(50, y_footer, "Подпись врача: __________________________")

    # === ДОБАВЛЕНИЕ ИЗОБРАЖЕНИЯ ПЕЧАТИ ===
    try:
        # Путь к изображению печати
        stamp_path = "app/assets/stamp.png"

        # Загрузка изображения
        stamp_image = ImageReader(stamp_path)
        stamp_width = 100  # ширина печати
        stamp_height = 100  # высота печати

        # Рисуем печать рядом с подписью
        c.drawImage(stamp_image, 180, y_footer - 50, width=stamp_width, height=stamp_height, mask='auto')
    except Exception as e:
        print(f"Ошибка загрузки печати: {e}")

    # === ДАТА ВЫДАЧИ ДОКУМЕНТА ===
    c.setFont("DejaVuSans", 12)
    c.drawString(50, y_footer - 40, f"Дата выдачи документа: {datetime.now().strftime('%d.%m.%Y')}")

    # Завершаем и сохраняем PDF
    c.save()

    return pdf_filename
