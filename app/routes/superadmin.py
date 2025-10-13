from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.models.admin import Admin, AdminConfig
from app.models.transaction import Transaction
from app.database import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json

superadmin_bp = Blueprint('superadmin', __name__, url_prefix='/superadmin')

def require_superadmin_login():
    if 'admin_id' not in session or session.get('admin_role') != 'superadmin':
        return False
    
    admin = Admin.query.get(session['admin_id'])
    if not admin or admin.role != 'superadmin' or admin.status != 'active':
        session.clear()
        return False
    
    return admin

@superadmin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('main.index'))

@superadmin_bp.route('/dashboard')
def dashboard():
    import logging
    logging.debug(f"Dashboard accessed. Session: {dict(session)}")
    
    admin = require_superadmin_login()
    if not admin:
        logging.debug("require_superadmin_login returned False, redirecting to index")
        return redirect(url_for('main.index'))
    
    logging.debug(f"SuperAdmin dashboard accessed by: {admin.username}")
    
    total_admins = Admin.query.filter_by(role='admin').count()
    active_admins = Admin.query.filter_by(role='admin', status='active').count()
    suspended_admins = Admin.query.filter_by(role='admin', status='suspended').count()
    total_transactions = Transaction.query.count()
    
    recent_admins = Admin.query.filter_by(role='admin').order_by(Admin.created_at.desc()).limit(5).all()
    
    admin_stats = db.session.query(
        Admin.id,
        Admin.username,
        Admin.email,
        Admin.status,
        func.count(Transaction.id).label('transaction_count'),
        func.sum(Transaction.send_amount).label('total_volume')
    ).outerjoin(Transaction, Admin.id == Transaction.admin_id)\
     .filter(Admin.role == 'admin')\
     .group_by(Admin.id, Admin.username, Admin.email, Admin.status)\
     .all()
    
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=today_start.weekday())
    month_start = today_start.replace(day=1)
    
    stats_today = db.session.query(func.sum(Transaction.send_amount)).filter(
        Transaction.created_at >= today_start
    ).scalar()
    
    stats_week = db.session.query(func.sum(Transaction.send_amount)).filter(
        Transaction.created_at >= week_start
    ).scalar()
    
    stats_month = db.session.query(func.sum(Transaction.send_amount)).filter(
        Transaction.created_at >= month_start
    ).scalar()
    
    total_today = round(stats_today, 2) if stats_today else 0
    total_week = round(stats_week, 2) if stats_week else 0
    total_month = round(stats_month, 2) if stats_month else 0
    
    daily_stats = []
    for i in range(7):
        day_start = today_start - timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        day_total = db.session.query(func.sum(Transaction.send_amount)).filter(
            Transaction.created_at >= day_start,
            Transaction.created_at < day_end
        ).scalar()
        
        daily_stats.append({
            'date': day_start.strftime('%Y-%m-%d'),
            'day_name': day_start.strftime('%A'),
            'total': round(day_total, 2) if day_total else 0
        })
    
    top_admins = db.session.query(
        Admin.username,
        func.sum(Transaction.send_amount).label('total'),
        func.count(Transaction.id).label('count')
    ).join(
        Transaction, Transaction.admin_id == Admin.id
    ).filter(
        Admin.role == 'admin'
    ).group_by(
        Admin.id, Admin.username
    ).order_by(
        desc('total')
    ).limit(10).all()
    
    return render_template('superadmin_dashboard.html',
                         total_admins=total_admins,
                         active_admins=active_admins,
                         suspended_admins=suspended_admins,
                         total_transactions=total_transactions,
                         recent_admins=recent_admins,
                         admin_stats=admin_stats,
                         total_today=total_today,
                         total_week=total_week,
                         total_month=total_month,
                         daily_stats=daily_stats,
                         top_admins=top_admins)

@superadmin_bp.route('/admins')
def admins_list():
    if not require_superadmin_login():
        return redirect(url_for('main.index'))
    
    admins = Admin.query.filter_by(role='admin').order_by(Admin.created_at.desc()).all()
    
    return render_template('superadmin_admins.html', admins=admins)

@superadmin_bp.route('/admins/create', methods=['GET', 'POST'])
def create_admin():
    if not require_superadmin_login():
        return redirect(url_for('main.index'))
    
    from app.data import COUNTRIES
    
    if request.method == 'POST':
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        whatsapp_number = request.form.get('whatsapp_number')
        password = request.form.get('password')
        country1_code = request.form.get('country1_code', 'RDC')
        country1_currency = request.form.get('country1_currency', 'USD')
        country2_code = request.form.get('country2_code', 'MA')
        country2_currency = request.form.get('country2_currency', 'MAD')
        reception_methods_country1 = request.form.getlist('reception_methods_country1')
        reception_methods_country2 = request.form.getlist('reception_methods_country2')
        
        if Admin.query.filter_by(username=username).first():
            return render_template('superadmin_create_admin.html', 
                                 countries=COUNTRIES,
                                 countries_json=json.dumps(COUNTRIES),
                                 error='Ce nom d\'utilisateur existe déjà')
        
        if Admin.query.filter_by(email=email).first():
            return render_template('superadmin_create_admin.html', 
                                 countries=COUNTRIES,
                                 countries_json=json.dumps(COUNTRIES),
                                 error='Cet email existe déjà')
        
        admin = Admin(
            username=username,
            full_name=full_name,
            email=email,
            whatsapp_number=whatsapp_number,
            role='admin',
            status='active'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.flush()
        
        config = AdminConfig(
            admin_id=admin.id,
            country1_code=country1_code,
            country1_currency=country1_currency,
            country2_code=country2_code,
            country2_currency=country2_currency,
            rate_country1_to_country2=10.0,
            rate_country2_to_country1=0.1,
            whatsapp_phone_1to2=whatsapp_number or '212699140001',
            whatsapp_contact_1to2=full_name or 'Eazi',
            whatsapp_phone_2to1=whatsapp_number or '212699140001',
            whatsapp_contact_2to1=full_name or 'Eazi',
            reception_methods_country1=reception_methods_country1 if reception_methods_country1 else ['Remise en personne'],
            reception_methods_country2=reception_methods_country2 if reception_methods_country2 else ['Remise en personne'],
            transaction_fees_1to2=[
                {'min': 0, 'max': 100, 'fee': 5},
                {'min': 100, 'max': 500, 'fee': 10},
                {'min': 500, 'max': 10000, 'fee': 20}
            ],
            transaction_fees_2to1=[
                {'min': 0, 'max': 1000, 'fee': 50},
                {'min': 1000, 'max': 5000, 'fee': 100},
                {'min': 5000, 'max': 100000, 'fee': 200}
            ]
        )
        
        db.session.add(config)
        db.session.commit()
        
        return redirect(url_for('superadmin.admins_list'))
    
    return render_template('superadmin_create_admin.html', 
                         countries=COUNTRIES,
                         countries_json=json.dumps(COUNTRIES))

@superadmin_bp.route('/admins/<int:admin_id>/edit', methods=['GET', 'POST'])
def edit_admin(admin_id):
    if not require_superadmin_login():
        return redirect(url_for('main.index'))
    
    admin = Admin.query.get_or_404(admin_id)
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        whatsapp_number = request.form.get('whatsapp_number')
        new_password = request.form.get('new_password')
        
        existing = Admin.query.filter(Admin.email == email, Admin.id != admin_id).first()
        if existing:
            return render_template('superadmin_edit_admin.html', 
                                 admin=admin,
                                 error='Cet email existe déjà')
        
        admin.full_name = full_name
        admin.email = email
        admin.whatsapp_number = whatsapp_number
        if new_password:
            admin.set_password(new_password)
        
        db.session.commit()
        return redirect(url_for('superadmin.admins_list'))
    
    return render_template('superadmin_edit_admin.html', admin=admin)

@superadmin_bp.route('/admins/<int:admin_id>/suspend', methods=['POST'])
def suspend_admin(admin_id):
    if not require_superadmin_login():
        return jsonify({'error': 'Non autorisé'}), 403
    
    admin = Admin.query.get_or_404(admin_id)
    admin.status = 'suspended'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Compte suspendu'})

@superadmin_bp.route('/admins/<int:admin_id>/activate', methods=['POST'])
def activate_admin(admin_id):
    if not require_superadmin_login():
        return jsonify({'error': 'Non autorisé'}), 403
    
    admin = Admin.query.get_or_404(admin_id)
    admin.status = 'active'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Compte activé'})

@superadmin_bp.route('/admins/<int:admin_id>/delete', methods=['POST'])
def delete_admin(admin_id):
    if not require_superadmin_login():
        return jsonify({'error': 'Non autorisé'}), 403
    
    admin = Admin.query.get_or_404(admin_id)
    db.session.delete(admin)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Admin supprimé'})

@superadmin_bp.route('/admins/<int:admin_id>/transactions')
def admin_transactions(admin_id):
    if not require_superadmin_login():
        return redirect(url_for('main.index'))
    
    admin = Admin.query.get_or_404(admin_id)
    transactions = Transaction.query.filter_by(admin_id=admin_id).order_by(Transaction.created_at.desc()).all()
    
    return render_template('superadmin_admin_transactions.html',
                         admin=admin,
                         transactions=[t.to_dict() for t in transactions])

@superadmin_bp.route('/statistics')
def statistics():
    admin = require_superadmin_login()
    if not admin:
        return redirect(url_for('main.index'))
    
    admin_stats = db.session.query(
        Admin.id,
        Admin.username,
        Admin.full_name,
        Admin.email,
        Admin.status,
        Admin.created_at,
        func.count(Transaction.id).label('transaction_count'),
        func.sum(Transaction.send_amount).label('total_volume')
    ).outerjoin(Transaction, Admin.id == Transaction.admin_id)\
     .filter(Admin.role == 'admin')\
     .group_by(Admin.id, Admin.username, Admin.full_name, Admin.email, Admin.status, Admin.created_at)\
     .order_by(desc('total_volume'))\
     .all()
    
    return render_template('superadmin_statistics.html', admin_stats=admin_stats)

@superadmin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
