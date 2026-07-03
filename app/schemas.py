from marshmallow import Schema, fields, validates_schema, ValidationError, validate


class InvoiceQuerySchema(Schema):
    """
    Esquema utilizado para validar los parámetros de consulta del endpoint
    de facturas.
    """

    start_date = fields.Date(
        required=True,
        load_only=True,
        error_messages={
            "required": "The start_date parameter is required.",
            "invalid": "The start_date must have the format YYYY-MM-DD."
        }
    )

    end_date = fields.Date(
        required=True,
        load_only=True,
        error_messages={
            "required": "The end_date parameter is required.",
            "invalid": "The end_date must have the format YYYY-MM-DD."
        }
    )

    @validates_schema
    def validate_date_range(self, data, **kwargs):
        if data["start_date"] > data["end_date"]:
            raise ValidationError(
                {
                    "start_date": [
                        "The start_date cannot be later than end_date."
                    ]
                }
            )

    page = fields.Int(
        load_default=1,
        load_only=True,
        validate=validate.Range(min=1),
        error_messages={
            "invalid": "The page must be an integer greater than or equal to 1."
        }
    )

    page_size = fields.Int(
        load_default=20,
        load_only=True,
        validate=validate.Range(min=1, max=100),
        error_messages={
            "invalid": "The page_size must be an integer between 1 and 100."
        }
    )

class InvoiceSchema(Schema):
    """
    Esquema utilizado para serializar una factura.
    """

    id = fields.Int(dump_only=True)
    invoice_number = fields.Str(dump_only=True)
    total = fields.Decimal(dump_only=True, as_string=True)
    invoice_date = fields.DateTime(dump_only=True)
    status = fields.Str(dump_only=True)
    active = fields.Bool(dump_only=True)

class InvoiceResponseSchema(Schema):
    """
    Esquema utilizado para serializar la respuesta paginada de facturas.
    """

    total = fields.Int(dump_only=True)
    page = fields.Int(dump_only=True)
    page_size = fields.Int(dump_only=True)
    total_pages = fields.Int(dump_only=True)
    items = fields.Nested(InvoiceSchema, dump_only=True, many=True)