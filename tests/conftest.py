from datetime import datetime

from pytest import fixture
from flask.testing import FlaskClient

from app import create_app
from app.extensions import db
from app.config import  ConfigTest
from app.models import Invoice

@fixture()
def app():
    app = create_app(ConfigTest)

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()

@fixture()
def client(app) -> FlaskClient:
    return app.test_client()

@fixture()
def sample_invoices(app):
    invoices = [
        Invoice(
            invoice_number="C29718",
            total=10.0,
            invoice_date=datetime(2022, 1, 3, 7, 50, 8),
            status="Vigente",
            active=False
        ),
        Invoice(
            invoice_number="C29723",
            total=14.45,
            invoice_date=datetime(2022, 1, 3, 7, 51, 3),
            status="Vigente",
            active=False
        ),
        Invoice(
            invoice_number="C29725",
            total=14.45,
            invoice_date=datetime(2022, 1, 3, 7, 51, 17),
            status="Cancelado",
            active=True
        ),
    ]

    db.session.add_all(invoices)
    db.session.commit()

    return invoices