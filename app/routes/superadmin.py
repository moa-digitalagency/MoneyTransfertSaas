from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.models.admin import Admin, AdminConfig
from app.models.transaction import Transaction
from app.database import db
from sqlalchemy import func

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
    
    return render_template('superadmin_dashboard.html',
                         total_admins=total_admins,
                         active_admins=active_admins,
                         suspended_admins=suspended_admins,
                         total_transactions=total_transactions,
                         recent_admins=recent_admins,
                         admin_stats=admin_stats)

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
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if Admin.query.filter_by(username=username).first():
            return render_template('superadmin_create_admin.html', 
                                 error='Ce nom d\'utilisateur existe déjà')
        
        if Admin.query.filter_by(email=email).first():
            return render_template('superadmin_create_admin.html', 
                                 error='Cet email existe déjà')
        
        admin = Admin(
            username=username,
            email=email,
            role='admin',
            status='active'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.flush()
        
        config = AdminConfig(
            admin_id=admin.id,
            country1_code='CD',
            country1_currency='USD',
            country2_code='MA',
            country2_currency='MAD',
            rate_country1_to_country2=10.0,
            rate_country2_to_country1=0.1,
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
    
    return render_template('superadmin_create_admin.html')

@superadmin_bp.route('/admins/<int:admin_id>/edit', methods=['GET', 'POST'])
def edit_admin(admin_id):
    if not require_superadmin_login():
        return redirect(url_for('main.index'))
    
    admin = Admin.query.get_or_404(admin_id)
    
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        
        existing = Admin.query.filter(Admin.email == email, Admin.id != admin_id).first()
        if existing:
            return render_template('superadmin_edit_admin.html', 
                                 admin=admin,
                                 error='Cet email existe déjà')
        
        admin.email = email
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

@superadmin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
