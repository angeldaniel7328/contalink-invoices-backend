
import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from app.models import Invoice

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