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
    """
    Get invoices by date range.
    ---
    tags:
      - Invoices

    summary: Retrieve invoices

    description: |
      Returns a paginated list of invoices filtered by the invoice date range.

    produces:
      - application/json

    parameters:
      - name: start_date
        in: query
        type: date
        required: true
        description: Start date in YYYY-MM-DD format.
        example: "2022-01-01"

      - name: end_date
        in: query
        type: date
        required: true
        description: End date in YYYY-MM-DD format.
        example: "2022-01-31"

      - name: page
        in: query
        type: integer
        required: false
        default: 1
        minimum: 1
        description: Page number.
        example: 1

      - name: page_size
        in: query
        type: integer
        required: false
        default: 3
        minimum: 1
        maximum: 100
        description: Number of records per page.
        example: 3

    responses:
      200:
        description: Invoices retrieved successfully.
        examples:
          application/json:
            total: 1454
            page: 1
            page_size: 3
            total_pages: 485
            items:
              - id: 1270
                invoice_number: C29718
                total: "10.0"
                invoice_date: "2022-01-03T07:50:08"
                status: Vigente
                active: false
              - id: 1675
                invoice_number: C29723
                total: "14.45"
                invoice_date: "2022-01-03T07:51:03"
                status: Vigente
                active: false
              - id: 1339
                invoice_number: C29725
                total: "14.45"
                invoice_date: "2022-01-03T07:51:17"
                status: Cancelado
                active: true

      400:
        description: Invalid request parameters.
        examples:
          application/json:
            start_date:
              - The start_date cannot be later than end_date.
    """
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