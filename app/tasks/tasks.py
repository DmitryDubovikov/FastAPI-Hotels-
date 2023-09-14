from pathlib import Path
import smtplib
from app.config import settings

from PIL import Image
from pydantic import EmailStr

from app.tasks.celery import celery
from app.tasks.email_templates import booking_confirmation_template


@celery.task
def process_image(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized = image.resize((800, 600))
    image_resized.save(f"app/static/images/resized_800_600_{image_path.name}")
    image_thumbnail = image.resize((200, 150))
    image_thumbnail.save(f"app/static/images/resized_200_150_{image_path.name}")


# @celery.task
def send_booking_confirmation(booking: dict, email_to: EmailStr):
    template = booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(template)


def send_booking_confirmation_with_background_tasks(booking: dict, email_to: EmailStr):
    template = booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(template)
