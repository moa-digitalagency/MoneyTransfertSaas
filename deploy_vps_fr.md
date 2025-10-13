# Guide de Déploiement VPS - TransfertSpace

## 📋 Prérequis

- Un serveur VPS avec Ubuntu 20.04 ou 22.04
- Accès root ou sudo
- Nom de domaine (optionnel mais recommandé)
- Au moins 1 GB de RAM et 20 GB d'espace disque

## 🚀 Installation

### 1. Mettre à jour le système

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Installer les dépendances système

```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

### 3. Configurer PostgreSQL

```bash
# Se connecter à PostgreSQL
sudo -u postgres psql

# Créer la base de données et l'utilisateur
CREATE DATABASE transfertspace;
CREATE USER transfertspace_user WITH PASSWORD 'votre_mot_de_passe_securise';
ALTER ROLE transfertspace_user SET client_encoding TO 'utf8';
ALTER ROLE transfertspace_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE transfertspace_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE transfertspace TO transfertspace_user;
\q
```

### 4. Cloner et configurer l'application

```bash
# Créer un utilisateur système pour l'application
sudo useradd -m -s /bin/bash transfertspace
sudo su - transfertspace

# Cloner le projet (remplacer par votre dépôt)
git clone https://github.com/votre-repo/transfertspace.git
cd transfertspace

# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances Python
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn psycopg2-binary werkzeug
```

### 5. Configuration des variables d'environnement

```bash
# Créer le fichier .env
nano .env
```

Ajouter le contenu suivant (modifier selon vos besoins):

```env
DATABASE_URL=postgresql://transfertspace_user:votre_mot_de_passe_securise@localhost/transfertspace
SESSION_SECRET=votre_cle_secrete_tres_longue_et_aleatoire
FLASK_ENV=production
```

### 6. Initialiser la base de données

```bash
# Toujours dans l'environnement virtuel
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Configurer Gunicorn comme service systemd

Sortir de l'utilisateur transfertspace:
```bash
exit
```

Créer le fichier service:
```bash
sudo nano /etc/systemd/system/transfertspace.service
```

Ajouter le contenu suivant:

```ini
[Unit]
Description=TransfertSpace Gunicorn Service
After=network.target

[Service]
User=transfertspace
Group=www-data
WorkingDirectory=/home/transfertspace/transfertspace
Environment="PATH=/home/transfertspace/transfertspace/venv/bin"
EnvironmentFile=/home/transfertspace/transfertspace/.env
ExecStart=/home/transfertspace/transfertspace/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --reuse-port main:app

[Install]
WantedBy=multi-user.target
```

Activer et démarrer le service:
```bash
sudo systemctl daemon-reload
sudo systemctl start transfertspace
sudo systemctl enable transfertspace
sudo systemctl status transfertspace
```

### 8. Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/transfertspace
```

Ajouter la configuration suivante (adapter votre_domaine.com):

```nginx
server {
    listen 80;
    server_name votre_domaine.com www.votre_domaine.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/transfertspace/transfertspace/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Activer le site:
```bash
sudo ln -s /etc/nginx/sites-available/transfertspace /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configurer SSL avec Let's Encrypt (Recommandé)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d votre_domaine.com -d www.votre_domaine.com
```

### 10. Configurer le pare-feu

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 📊 Maintenance

### Vérifier les logs

```bash
# Logs de l'application
sudo journalctl -u transfertspace -f

# Logs Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Redémarrer l'application

```bash
sudo systemctl restart transfertspace
```

### Mettre à jour l'application

```bash
sudo su - transfertspace
cd transfertspace
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
exit
sudo systemctl restart transfertspace
```

### Sauvegarder la base de données

```bash
sudo -u postgres pg_dump transfertspace > backup_$(date +%Y%m%d).sql
```

### Restaurer la base de données

```bash
sudo -u postgres psql transfertspace < backup_20250113.sql
```

## 🔒 Sécurité

1. **Changer les mots de passe par défaut** dans `.env` et PostgreSQL
2. **Activer le pare-feu** avec ufw
3. **Mettre à jour régulièrement** le système et l'application
4. **Configurer des sauvegardes automatiques** de la base de données
5. **Monitorer les logs** régulièrement pour détecter les activités suspectes

## 🆘 Dépannage

### L'application ne démarre pas

```bash
sudo journalctl -u transfertspace -n 50
```

### Erreur de connexion à la base de données

Vérifier les paramètres dans `.env` et que PostgreSQL est en cours d'exécution:
```bash
sudo systemctl status postgresql
```

### Erreur 502 Bad Gateway

Vérifier que Gunicorn est en cours d'exécution:
```bash
sudo systemctl status transfertspace
```

## 📞 Support

Pour toute assistance technique, contactez:
- Email: moa@myoneart.com
- Web: https://www.myoneart.com

---

© 2025 MOA Digital Agency LLC - TransfertSpace
