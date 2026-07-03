from app.extensions import db


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String, nullable=False)
    total = db.Column(db.Numeric, nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)