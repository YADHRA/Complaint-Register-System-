from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.database import db
from backend.routes.auth import auth_bp
from backend.routes.complaints import complaints_bp
from backend.routes.admin import admin_bp
from backend.routes.faq import faq_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(complaints_bp, url_prefix='/api/complaints')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(faq_bp, url_prefix='/api/faq')

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
