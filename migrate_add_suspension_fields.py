"""
Migration script to add page_suspended and suspension_message fields to admin_configs table.
Run this script once to update existing databases with the new fields.

Usage: python migrate_add_suspension_fields.py
"""

from app import app, db

def migrate():
    with app.app_context():
        try:
            db.session.execute("""
                ALTER TABLE admin_configs 
                ADD COLUMN IF NOT EXISTS page_suspended BOOLEAN NOT NULL DEFAULT FALSE;
            """)
            
            db.session.execute("""
                ALTER TABLE admin_configs 
                ADD COLUMN IF NOT EXISTS suspension_message TEXT DEFAULT 'Service temporairement suspendu. Veuillez réessayer ultérieurement.';
            """)
            
            db.session.commit()
            print("✅ Migration réussie! Les champs page_suspended et suspension_message ont été ajoutés.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Erreur lors de la migration: {e}")
            print("Les champs existent peut-être déjà ou la base de données n'est pas accessible.")

if __name__ == '__main__':
    migrate()
