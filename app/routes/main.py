from flask import Blueprint, render_template, request, jsonify, abort
from app.config.settings import load_config
from app.utils.calculations import calculate_transfer
from app.models.transaction import Transaction
from app.models.admin import Admin, AdminConfig
from app.data import get_country_by_code, get_reception_methods
from app.database import db
import urllib.parse

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('welcome.html')

@main_bp.route('/<username>')
def user_index(username):
    admin = Admin.query.filter_by(username=username, role='admin').first()
    
    if not admin:
        abort(404)
    
    if admin.status != 'active':
        return render_template('account_suspended.html', username=username), 403
    
    if not admin.config:
        abort(404)
    
    config = admin.config.to_dict()
    
    country1 = get_country_by_code(config['countries']['country1']['code'])
    country2 = get_country_by_code(config['countries']['country2']['code'])
    
    config['country1_info'] = country1
    config['country2_info'] = country2
    
    custom_methods1 = config.get('reception_methods', {}).get('country1', [])
    custom_methods2 = config.get('reception_methods', {}).get('country2', [])
    
    config['country1_reception_methods'] = get_reception_methods(config['countries']['country1']['code'], custom_methods1)
    config['country2_reception_methods'] = get_reception_methods(config['countries']['country2']['code'], custom_methods2)
    
    config['username'] = username
    
    return render_template('index.html', config=config, username=username, admin_id=admin.id)

@main_bp.route('/calculate', methods=['POST'])
def calculate():
    config = load_config()
    data = request.json
    
    direction = data.get('direction')
    amount = float(data.get('amount', 0))
    calculation_type = data.get('calculation_type')
    
    result = calculate_transfer(direction, amount, calculation_type, config)
    return jsonify(result)

@main_bp.route('/<username>/calculate', methods=['POST'])
def user_calculate(username):
    admin = Admin.query.filter_by(username=username, role='admin', status='active').first()
    
    if not admin or not admin.config:
        return jsonify({'error': 'Admin introuvable'}), 404
    
    config = admin.config.to_dict()
    data = request.json
    
    direction = data.get('direction')
    amount = float(data.get('amount', 0))
    calculation_type = data.get('calculation_type')
    
    result = calculate_transfer(direction, amount, calculation_type, config)
    return jsonify(result)

@main_bp.route('/generate_whatsapp', methods=['POST'])
def generate_whatsapp():
    config = load_config()
    data = request.json
    
    whatsapp_url, transaction_data = generate_whatsapp_message_from_config(data, config)
    
    transaction = Transaction(
        direction=data.get('direction'),
        send_amount=float(data.get('send_amount', 0)),
        receive_amount=float(data.get('receive_amount', 0)),
        send_currency=data.get('send_currency'),
        receive_currency=data.get('receive_currency'),
        reception_method=data.get('reception_method'),
        reception_details=data.get('reception_details'),
        country1_name=transaction_data['country1_name'],
        country2_name=transaction_data['country2_name'],
        whatsapp_phone=transaction_data['whatsapp_phone'],
        whatsapp_contact=transaction_data['whatsapp_contact']
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'whatsapp_url': whatsapp_url})

@main_bp.route('/<username>/generate_whatsapp', methods=['POST'])
def user_generate_whatsapp(username):
    admin = Admin.query.filter_by(username=username, role='admin', status='active').first()
    
    if not admin or not admin.config:
        return jsonify({'error': 'Admin introuvable'}), 404
    
    config = admin.config.to_dict()
    data = request.json
    
    whatsapp_url, transaction_data = generate_whatsapp_message_from_config(data, config)
    
    transaction = Transaction(
        admin_id=admin.id,
        direction=data.get('direction'),
        send_amount=float(data.get('send_amount', 0)),
        receive_amount=float(data.get('receive_amount', 0)),
        send_currency=data.get('send_currency'),
        receive_currency=data.get('receive_currency'),
        reception_method=data.get('reception_method'),
        reception_details=data.get('reception_details'),
        country1_name=transaction_data['country1_name'],
        country2_name=transaction_data['country2_name'],
        whatsapp_phone=transaction_data['whatsapp_phone'],
        whatsapp_contact=transaction_data['whatsapp_contact']
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'whatsapp_url': whatsapp_url})

def generate_whatsapp_message_from_config(data, config):
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
