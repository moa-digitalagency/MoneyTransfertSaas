#!/usr/bin/env python
import sys
from app import create_app
from app.models.admin import Admin
from app.database import db

def init_superadmin():
    app = create_app()
    
    with app.app_context():
        existing = Admin.query.filter_by(role='superadmin').first()
        
        if existing:
            print(f"Un superadmin existe déjà: {existing.username}")
            choice = input("Voulez-vous le remplacer? (oui/non): ")
            if choice.lower() not in ['oui', 'yes', 'y']:
                print("Opération annulée")
                return
            db.session.delete(existing)
            db.session.commit()
        
        username = input("Nom d'utilisateur du superadmin: ").strip()
        email = input("Email du superadmin: ").strip()
        password = input("Mot de passe du superadmin: ").strip()
        
        if not username or not email or not password:
            print("Tous les champs sont requis!")
            return
        
        superadmin = Admin(
            username=username,
            email=email,
            role='superadmin',
            status='active'
        )
        superadmin.set_password(password)
        
        db.session.add(superadmin)
        db.session.commit()
        
        print(f"\n✅ Superadmin créé avec succès!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"\nConnectez-vous sur: /superadmin/login")

if __name__ == '__main__':
    init_superadmin()
