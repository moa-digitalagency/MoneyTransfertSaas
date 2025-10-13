#!/usr/bin/env python
from app import create_app
from app.models.admin import Admin
from app.database import db

def create_superadmin():
    app = create_app()
    
    with app.app_context():
        existing = Admin.query.filter_by(username='myoneart').first()
        
        if existing:
            print(f"Le superadmin '{existing.username}' existe déjà")
            return
        
        superadmin = Admin(
            username='myoneart',
            email='moa@myoneart.com',
            role='superadmin',
            status='active'
        )
        superadmin.set_password('my0n34rt')
        
        db.session.add(superadmin)
        db.session.commit()
        
        print(f"\n✅ Superadmin créé avec succès!")
        print(f"Username: myoneart")
        print(f"Email: moa@myoneart.com")
        print(f"Mot de passe: my0n34rt")
        print(f"\nConnectez-vous sur: /")

if __name__ == '__main__':
    create_superadmin()
