from datetime import datetime
from app.database import db
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='admin')
    status = db.Column(db.String(20), nullable=False, default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    transactions = db.relationship('Transaction', backref='admin', lazy=True, cascade='all, delete-orphan')
    config = db.relationship('AdminConfig', backref='admin', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AdminConfig(db.Model):
    __tablename__ = 'admin_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False, unique=True)
    
    country1_code = db.Column(db.String(10), nullable=False, default='CD')
    country1_currency = db.Column(db.String(10), nullable=False, default='USD')
    country2_code = db.Column(db.String(10), nullable=False, default='MA')
    country2_currency = db.Column(db.String(10), nullable=False, default='MAD')
    
    rate_country1_to_country2 = db.Column(db.Float, nullable=False, default=10.0)
    rate_country2_to_country1 = db.Column(db.Float, nullable=False, default=0.1)
    
    whatsapp_phone_1to2 = db.Column(db.String(20))
    whatsapp_contact_1to2 = db.Column(db.String(100))
    whatsapp_phone_2to1 = db.Column(db.String(20))
    whatsapp_contact_2to1 = db.Column(db.String(100))
    
    transaction_fees_1to2 = db.Column(db.JSON, nullable=False, default=lambda: [
        {'min': 0, 'max': 100, 'fee': 5},
        {'min': 100, 'max': 500, 'fee': 10},
        {'min': 500, 'max': 10000, 'fee': 20}
    ])
    transaction_fees_2to1 = db.Column(db.JSON, nullable=False, default=lambda: [
        {'min': 0, 'max': 1000, 'fee': 50},
        {'min': 1000, 'max': 5000, 'fee': 100},
        {'min': 5000, 'max': 100000, 'fee': 200}
    ])
    
    app_title = db.Column(db.String(200), default='Transfert Monétaire')
    app_content = db.Column(db.Text, default='La seule référence pour vos transfert d\'argent sûr')
    
    reception_methods_country1 = db.Column(db.JSON, default=list)
    reception_methods_country2 = db.Column(db.JSON, default=list)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'countries': {
                'country1': {'code': self.country1_code, 'currency_code': self.country1_currency},
                'country2': {'code': self.country2_code, 'currency_code': self.country2_currency}
            },
            'rates': {
                'country1_to_country2': self.rate_country1_to_country2,
                'country2_to_country1': self.rate_country2_to_country1
            },
            'whatsapp': {
                'country1_to_country2': {'phone': self.whatsapp_phone_1to2, 'contact_name': self.whatsapp_contact_1to2},
                'country2_to_country1': {'phone': self.whatsapp_phone_2to1, 'contact_name': self.whatsapp_contact_2to1}
            },
            'transaction_fees': {
                'country1_to_country2': self.transaction_fees_1to2 or [],
                'country2_to_country1': self.transaction_fees_2to1 or []
            },
            'app_section': {
                'title': self.app_title,
                'content': self.app_content
            },
            'reception_methods': {
                'country1': self.reception_methods_country1 or [],
                'country2': self.reception_methods_country2 or []
            }
        }
