import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Supabase 클라이언트 가져오기
from supabase_client import supabase

# Supabase 연결 확인
if supabase:
    logging.info("🚀 Supabase 연결됨 - 클라우드 데이터베이스 사용")
    # SQLite는 백업용으로만 사용
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cascade_system_backup.db"
else:
    logging.info("💾 로컬 SQLite 사용")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cascade_system.db"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)

# Import and initialize models
import models
User, Inspection = models.init_models(db)

with app.app_context():
    db.create_all()
    
    # Create default admin user if not exists
    from werkzeug.security import generate_password_hash
    
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User()
        admin_user.username = 'admin'
        admin_user.name = '관리자'
        admin_user.phone = '000-0000-0000'
        admin_user.employee_id = '000000'
        admin_user.password_hash = generate_password_hash('admin123')
        admin_user.role = 'admin'
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Default admin user created: admin/admin123")

# Import routes after models are initialized
import routes
routes.init_routes(app, db, User, Inspection)

