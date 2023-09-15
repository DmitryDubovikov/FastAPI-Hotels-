from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def booking_confirmation_template(booking: dict, email_to: EmailStr):
    email_message = EmailMessage()
    email_message["Subject"] = "Booking confirmation"
    email_message["From"] = settings.SMTP_USER
    email_message["To"] = email_to
    email_message.set_content(
        f"""
        <h1>Booking confirmation</h1>
        You have booked a hotel from {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html",
    )
    return email_message
