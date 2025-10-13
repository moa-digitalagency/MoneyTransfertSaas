import hashlib

def hash_password(password):
    """Convertit un mot de passe en hash SHA-256 pour stockage sécurisé"""
    return hashlib.sha256(password.encode()).hexdigest()
