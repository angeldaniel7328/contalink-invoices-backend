from flask import current_app

from app.repositories import InvoiceRepository
from app.mail.email_service import send_email


def send_daily_sales_report():
    top_days = InvoiceRepository.find_top_sales_days()

    body = ["Top 10 días con mayor venta\n"]

    for index, row in enumerate(top_days, start=1):
        body.append(
            f"{index}. {row.invoice_day}: ${row.total_sales}"
        )

    send_email(
        subject="Top 10 días con mayor venta",
        body="\n".join(body),
        to_email=current_app.config["MAIL_TO"],
    )