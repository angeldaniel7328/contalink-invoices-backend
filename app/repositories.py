
import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

from app.models import Invoice
from app import db

logger = logging.getLogger(__name__)


class InvoiceRepository:

    @staticmethod
    def find_by_date_range(start_date: datetime, end_date: datetime, page: int, page_size: int):
        try:
            query = (
                Invoice.query
                .filter(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date
                )
            )

            total = query.count()

            items = (
                query
                .order_by(Invoice.invoice_date.asc())
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )

            return total, items

        except SQLAlchemyError:
            logger.exception(
                "Error querying invoices. start_date=%s, end_date=%s, page=%s, page_size=%s",
                start_date,
                end_date,
                page,
                page_size,
            )
            raise

    @staticmethod
    def find_top_sales_days(limit=10):
        return (
            db.session.query(
                func.date(Invoice.invoice_date).label("invoice_day"),
                func.sum(Invoice.total).label("total_sales")
            )
            .filter(Invoice.active.is_(True))
            .group_by(func.date(Invoice.invoice_date))
            .order_by(func.sum(Invoice.total).desc())
            .limit(limit)
            .all()
        )