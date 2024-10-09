from views.auth_views import auth_bp
from  views.vehiculos_views import vehiculo_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(vehiculo_bp)