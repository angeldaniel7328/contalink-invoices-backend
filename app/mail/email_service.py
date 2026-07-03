import smtplib
from email.message import EmailMessage
from flask import current_app


def send_email(subject, body, to_email):
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = current_app.config["MAIL_USERNAME"]
    message["To"] = to_email
    message.set_content(body)

    with smtplib.SMTP(
        current_app.config["MAIL_SERVER"],
        current_app.config["MAIL_PORT"],
    ) as server:
        server.starttls()
        server.login(
            current_app.config["MAIL_USERNAME"],
            current_app.config["MAIL_PASSWORD"],
        )
        server.send_message(message)