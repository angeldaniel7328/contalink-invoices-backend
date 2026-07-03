import math
from datetime import datetime

from app.repositories import InvoiceRepository
from app.schemas import InvoiceResponseSchema

class InvoiceService:

    def __init__(self):
        self.response_schema = InvoiceResponseSchema()

    def get_invoices(self, start_date: datetime, end_date: datetime, page: int, page_size: int):
        """
        Obtiene las facturas dentro del rango de fechas especificado y
        construye la respuesta paginada que será enviada al cliente.
        """
        total, invoices = InvoiceRepository.find_by_date_range(
            start_date,
            end_date,
            page,
            page_size
        )

        return self.response_schema.dump({
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": math.ceil(total / page_size),
            "items": invoices
        })