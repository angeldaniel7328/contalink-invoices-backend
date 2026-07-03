import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError

from app.schemas import InvoiceQuerySchema
from app.services import InvoiceService

invoices_bp = Blueprint('customers', __name__, url_prefix='/api/invoices')

query_schema = InvoiceQuerySchema()
invoice_service = InvoiceService()

logger = logging.getLogger(__name__)


@invoices_bp.get("")
@jwt_required()
def get_invoices():
    try:
        query = query_schema.load(request.args)

        start_date,end_date = query["start_date"], query["end_date"]
        page,page_size = query["page"], query["page_size"]

        logger.debug(
            "Searching invoices. start_date=%s end_date=%s page=%s page_size=%s",
            start_date,
            end_date,
            page,
            page_size,
        )

        response = invoice_service.get_invoices(start_date, end_date, page, page_size)

        return jsonify(response), HTTPStatus.OK

    except ValidationError as err:
        logger.warning("Invalid invoice query parameters: %s",err.messages)

        return jsonify(err.messages), HTTPStatus.BAD_REQUEST