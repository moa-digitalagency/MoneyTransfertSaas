import urllib.parse
from datetime import datetime
from app.database import db
from app.config.settings import load_config
from app.data import get_country_by_code

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    direction = db.Column(db.String(50), nullable=False)
    send_amount = db.Column(db.Float, nullable=False)
    receive_amount = db.Column(db.Float, nullable=False)
    send_currency = db.Column(db.String(10), nullable=False)
    receive_currency = db.Column(db.String(10), nullable=False)
    reception_method = db.Column(db.String(50), nullable=False)
    reception_details = db.Column(db.String(200), nullable=False)
    country1_name = db.Column(db.String(100))
    country2_name = db.Column(db.String(100))
    whatsapp_phone = db.Column(db.String(20))
    whatsapp_contact = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'direction': self.direction,
            'send_amount': self.send_amount,
            'receive_amount': self.receive_amount,
            'send_currency': self.send_currency,
            'receive_currency': self.receive_currency,
            'reception_method': self.reception_method,
            'reception_details': self.reception_details,
            'country1_name': self.country1_name,
            'country2_name': self.country2_name,
            'whatsapp_phone': self.whatsapp_phone,
            'whatsapp_contact': self.whatsapp_contact,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

def generate_whatsapp_message(data):
    config = load_config()
    whatsapp_config = config['whatsapp']
    
    direction = data.get('direction')
    send_amount = data.get('send_amount')
    receive_amount = data.get('receive_amount')
    send_currency = data.get('send_currency')
    receive_currency = data.get('receive_currency')
    reception_method = data.get('reception_method')
    reception_details = data.get('reception_details')
    
    if direction not in whatsapp_config:
        direction = 'country1_to_country2'
    
    whatsapp = whatsapp_config[direction]
    
    country1 = get_country_by_code(config['countries']['country1']['code'])
    country2 = get_country_by_code(config['countries']['country2']['code'])
    
    if direction == 'country1_to_country2':
        transfer_text = f"de {country1['name']} vers {country2['name']}"
    else:
        transfer_text = f"de {country2['name']} vers {country1['name']}"
    
    message = f"""Bonjour {whatsapp['contact_name']}, j'ai besoin de faire un transfert {transfer_text}.

*Montant à envoyer:* {send_amount} {send_currency}
*Montant à recevoir:* {receive_amount} {receive_currency}

*Moyen de réception:* {reception_method}
*Coordonnées:* {reception_details}

Merci de confirmer cette demande."""
    
    encoded_message = urllib.parse.quote(message)
    phone = whatsapp['phone']
    whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
    
    return whatsapp_url, {
        'country1_name': country1['name'],
        'country2_name': country2['name'],
        'whatsapp_phone': phone,
        'whatsapp_contact': whatsapp['contact_name']
    }
