from app.routes.auth import auth_bp
from app.routes.invoices import invoices_bp

def register_routes(app):
    app.register_blueprint(invoices_bp)
    app.register_blueprint(auth_bp)