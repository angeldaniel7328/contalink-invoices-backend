import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.sales_report_job import send_daily_sales_report

logger = logging.getLogger(__name__)


def start_scheduler(app):

    scheduler = BackgroundScheduler(timezone="America/Mexico_City")

    def job():
        logger.info("Executing daily sales report job")
        with app.app_context():
            send_daily_sales_report()
        logger.info("Daily sales report job finished")

    with app.app_context():
        send_daily_sales_report()

    scheduler.add_job(
        job,
        trigger="cron",
        hour=8,
        minute=0,
        id="daily-sales-report",
        replace_existing=True,
    )

    scheduler.start()