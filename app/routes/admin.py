from flask import Blueprint, render_template, request, session, redirect, url_for
import json
import logging
from app.models.admin import Admin, AdminConfig
from app.models.transaction import Transaction
from app.data import COUNTRIES
from app.database import db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def require_admin_login():
    if 'admin_id' not in session or session.get('admin_role') != 'admin':
        return False
    
    admin = Admin.query.get(session['admin_id'])
    if not admin or admin.status != 'active':
        session.clear()
        return False
    
    return admin

@admin_bp.route('/')
def admin():
    admin = require_admin_login()
    if not admin:
        return render_template('admin_login.html')
    
    if not admin.config:
        config_obj = AdminConfig(admin_id=admin.id)
        db.session.add(config_obj)
        db.session.commit()
        admin.config = config_obj
    
    config = admin.config.to_dict()
    success_message = request.args.get('success', '')
    
    return render_template('admin_panel.html', 
                         config=config, 
                         countries=COUNTRIES,
                         countries_json=json.dumps(COUNTRIES),
                         username=admin.username,
                         success=success_message)

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    admin = Admin.query.filter_by(username=username, role='admin').first()
    
    if admin and admin.check_password(password):
        if admin.status != 'active':
            return render_template('admin_login.html', error='Compte suspendu')
        
        session.clear()
        session['admin_id'] = admin.id
        session['admin_role'] = 'admin'
        session.permanent = True
        
        logger.info(f"Connexion admin réussie: {admin.username}")
        return redirect(url_for('admin.admin'))
    
    logger.warning("Connexion admin échouée")
    return render_template('admin_login.html', error='Identifiants incorrects')

@admin_bp.route('/update', methods=['POST'])
def admin_update():
    admin = require_admin_login()
    if not admin:
        return redirect(url_for('admin.admin'))
    
    if not admin.config:
        admin.config = AdminConfig(admin_id=admin.id)
        db.session.add(admin.config)
    
    config = admin.config
    
    config.country1_code = request.form.get('country1_code')
    config.country1_currency = request.form.get('country1_currency')
    config.country2_code = request.form.get('country2_code')
    config.country2_currency = request.form.get('country2_currency')
    
    rate_1to2_str = request.form.get('country1_to_country2', '0').strip()
    rate_2to1_str = request.form.get('country2_to_country1', '0').strip()
    
    try:
        config.rate_country1_to_country2 = float(rate_1to2_str) if rate_1to2_str else 0
    except ValueError:
        config.rate_country1_to_country2 = 0
    
    try:
        config.rate_country2_to_country1 = float(rate_2to1_str) if rate_2to1_str else 0
    except ValueError:
        config.rate_country2_to_country1 = 0
    
    config.whatsapp_phone_1to2 = request.form.get('phone_country1_to_country2')
    config.whatsapp_contact_1to2 = request.form.get('contact_name_country1_to_country2')
    config.whatsapp_phone_2to1 = request.form.get('phone_country2_to_country1')
    config.whatsapp_contact_2to1 = request.form.get('contact_name_country2_to_country1')
    
    country1_to_country2_fees = []
    for i in range(10):
        min_key = f'country1_to_country2[{i}][min]'
        if min_key in request.form:
            min_val_str = request.form.get(min_key, '0').strip()
            max_val_str = request.form.get(f'country1_to_country2[{i}][max]', '0').strip()
            fee_val_str = request.form.get(f'country1_to_country2[{i}][fee]', '0').strip()
            
            if min_val_str and max_val_str and fee_val_str:
                try:
                    min_val = float(min_val_str)
                    max_val = float(max_val_str)
                    fee_val = float(fee_val_str)
                    country1_to_country2_fees.append({'min': min_val, 'max': max_val, 'fee': fee_val})
                except ValueError:
                    pass
    
    country2_to_country1_fees = []
    for i in range(10):
        min_key = f'country2_to_country1[{i}][min]'
        if min_key in request.form:
            min_val_str = request.form.get(min_key, '0').strip()
            max_val_str = request.form.get(f'country2_to_country1[{i}][max]', '0').strip()
            fee_val_str = request.form.get(f'country2_to_country1[{i}][fee]', '0').strip()
            
            if min_val_str and max_val_str and fee_val_str:
                try:
                    min_val = float(min_val_str)
                    max_val = float(max_val_str)
                    fee_val = float(fee_val_str)
                    country2_to_country1_fees.append({'min': min_val, 'max': max_val, 'fee': fee_val})
                except ValueError:
                    pass
    
    config.transaction_fees_1to2 = country1_to_country2_fees
    config.transaction_fees_2to1 = country2_to_country1_fees
    
    new_password = request.form.get('new_password')
    if new_password and new_password.strip():
        admin.set_password(new_password)
    
    app_title = request.form.get('app_title')
    app_content = request.form.get('app_content')
    if app_title:
        config.app_title = app_title
    if app_content:
        config.app_content = app_content
    
    reception_methods_1 = request.form.get('reception_methods_country1', '').strip()
    reception_methods_2 = request.form.get('reception_methods_country2', '').strip()
    
    config.reception_methods_country1 = [m.strip() for m in reception_methods_1.split('\n') if m.strip()] if reception_methods_1 else []
    config.reception_methods_country2 = [m.strip() for m in reception_methods_2.split('\n') if m.strip()] if reception_methods_2 else []
    
    config.direction_1to2_enabled = request.form.get('direction_1to2_enabled') == 'on'
    config.direction_2to1_enabled = request.form.get('direction_2to1_enabled') == 'on'
    
    config.page_suspended = request.form.get('page_suspended') == '1'
    suspension_message = request.form.get('suspension_message', '').strip()
    if suspension_message:
        config.suspension_message = suspension_message
    else:
        config.suspension_message = 'Service temporairement suspendu. Veuillez réessayer ultérieurement.'
    
    db.session.commit()
    
    logger.info("Configuration mise à jour avec succès")
    return redirect(url_for('admin.admin', success='Configuration mise à jour avec succès!'))

@admin_bp.route('/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('main.index'))

@admin_bp.route('/history')
def admin_history():
    admin = require_admin_login()
    if not admin:
        return redirect(url_for('admin.admin'))
    
    transactions = Transaction.query.filter_by(admin_id=admin.id).order_by(Transaction.created_at.desc()).all()
    transactions_data = [t.to_dict() for t in transactions]
    
    return render_template('admin_history.html', 
                         transactions=transactions_data,
                         username=admin.username)
