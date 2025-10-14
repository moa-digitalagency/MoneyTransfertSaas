import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def init_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    db.init_app(app)
    
    with app.app_context():
        from app.models.transaction import Transaction
        from app.models.admin import Admin, AdminConfig
        db.create_all()
        
        existing_superadmin = Admin.query.filter_by(role='superadmin').first()
        if not existing_superadmin:
            superadmin = Admin()
            superadmin.username = 'myoneart'
            superadmin.email = 'moa@myoneart.com'
            superadmin.role = 'superadmin'
            superadmin.status = 'active'
            superadmin.set_password('my0n34rt')
            db.session.add(superadmin)
            db.session.commit()
            print("✅ Superadmin créé automatiquement")
