from flask import Blueprint, render_template, request, jsonify, abort
from app.config.settings import load_config
from app.utils.calculations import calculate_transfer
from app.models.transaction import Transaction
from app.models.admin import Admin, AdminConfig
from app.data import get_country_by_code, get_reception_methods
from app.database import db
from app.utils.i18n import get_translations
import urllib.parse

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    from flask import redirect, url_for, session
    from app.models.admin import Admin
    from app.data import COUNTRIES
    import logging
    import json
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        t = get_translations()
        
        logging.debug(f"Tentative de connexion pour: {username}")
        
        if not username or not password:
            logging.debug("Username ou password vide")
            return render_template('welcome.html', error=t['welcome']['errors']['fill_all_fields'], countries_json=json.dumps(COUNTRIES))
        
        admin = Admin.query.filter_by(username=username, role='superadmin').first()
        
        if not admin:
            logging.debug(f"Aucun superadmin trouvé avec username: {username}")
            return render_template('welcome.html', error=t['welcome']['errors']['invalid_credentials'], countries_json=json.dumps(COUNTRIES))
        
        if not admin.check_password(password):
            logging.debug(f"Mot de passe incorrect pour: {username}")
            return render_template('welcome.html', error=t['welcome']['errors']['invalid_credentials'], countries_json=json.dumps(COUNTRIES))
        
        if admin.status != 'active':
            logging.debug(f"Compte suspendu: {username}")
            return render_template('welcome.html', error=t['welcome']['errors']['account_suspended'], countries_json=json.dumps(COUNTRIES))
        
        logging.debug(f"Connexion réussie pour: {username}")
        session.clear()
        session['admin_id'] = admin.id
        session['admin_role'] = 'superadmin'
        session.permanent = True
        
        return redirect(url_for('superadmin.dashboard'))
    
    return render_template('welcome.html', countries_json=json.dumps(COUNTRIES))

@main_bp.route('/<username>')
def user_index(username):
    admin = Admin.query.filter_by(username=username, role='admin').first()
    
    if not admin:
        abort(404)
    
    if admin.status != 'active':
        return render_template('account_suspended.html', username=username), 403
    
    if not admin.config:
        abort(404)
    
    if admin.config.page_suspended:
        return render_template('account_suspended.html', username=username, custom_message=admin.config.suspension_message), 403
    
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
    try:
        amount = float(data.get('amount', 0) or 0)
    except (ValueError, TypeError):
        amount = 0
    calculation_type = data.get('calculation_type')
    
    result = calculate_transfer(direction, amount, calculation_type, config)
    return jsonify(result)

@main_bp.route('/<username>/calculate', methods=['POST'])
def user_calculate(username):
    admin = Admin.query.filter_by(username=username, role='admin', status='active').first()
    t = get_translations()
    
    if not admin or not admin.config:
        error_msg = t.get('errors', {}).get('admin_not_found', 'Admin not found')
        return jsonify({'error': error_msg}), 404
    
    config = admin.config.to_dict()
    data = request.json
    
    direction = data.get('direction')
    try:
        amount = float(data.get('amount', 0) or 0)
    except (ValueError, TypeError):
        amount = 0
    calculation_type = data.get('calculation_type')
    
    result = calculate_transfer(direction, amount, calculation_type, config)
    return jsonify(result)

@main_bp.route('/generate_whatsapp', methods=['POST'])
def generate_whatsapp():
    config = load_config()
    data = request.json
    t = get_translations()
    
    whatsapp_url, transaction_data = generate_whatsapp_message_from_config(data, config, t)
    
    try:
        send_amount = float(data.get('send_amount', 0) or 0)
        receive_amount = float(data.get('receive_amount', 0) or 0)
    except (ValueError, TypeError):
        send_amount = 0
        receive_amount = 0
    
    transaction = Transaction(
        direction=data.get('direction'),
        send_amount=send_amount,
        receive_amount=receive_amount,
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
    t = get_translations()
    
    if not admin or not admin.config:
        error_msg = t.get('errors', {}).get('admin_not_found', 'Admin not found')
        return jsonify({'error': error_msg}), 404
    
    config = admin.config.to_dict()
    data = request.json
    
    whatsapp_url, transaction_data = generate_whatsapp_message_from_config(data, config, t)
    
    try:
        send_amount = float(data.get('send_amount', 0) or 0)
        receive_amount = float(data.get('receive_amount', 0) or 0)
    except (ValueError, TypeError):
        send_amount = 0
        receive_amount = 0
    
    transaction = Transaction(
        admin_id=admin.id,
        direction=data.get('direction'),
        send_amount=send_amount,
        receive_amount=receive_amount,
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

def generate_whatsapp_message_from_config(data, config, t=None):
    if t is None:
        t = get_translations()
    
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
        transfer_text = f"{t['whatsapp_message']['from']} {country1['name']} {t['whatsapp_message']['to']} {country2['name']}"
    else:
        transfer_text = f"{t['whatsapp_message']['from']} {country2['name']} {t['whatsapp_message']['to']} {country1['name']}"
    
    message = f"""{t['whatsapp_message']['greeting']} {whatsapp['contact_name']}, {t['whatsapp_message']['transfer_from_to']} {transfer_text}.

*{t['whatsapp_message']['send_amount']}* {send_amount} {send_currency}
*{t['whatsapp_message']['receive_amount']}* {receive_amount} {receive_currency}

*{t['whatsapp_message']['reception_method']}* {reception_method}
*{t['whatsapp_message']['details']}* {reception_details}

{t['whatsapp_message']['confirm_request']}"""
    
    encoded_message = urllib.parse.quote(message)
    phone = whatsapp['phone']
    whatsapp_url = f"https://wa.me/{phone}?text={encoded_message}"
    
    return whatsapp_url, {
        'country1_name': country1['name'],
        'country2_name': country2['name'],
        'whatsapp_phone': phone,
        'whatsapp_contact': whatsapp['contact_name']
    }
