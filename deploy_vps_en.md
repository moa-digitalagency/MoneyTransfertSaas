# VPS Deployment Guide - TransfertSpace

## 📋 Prerequisites

- VPS server with Ubuntu 20.04 or 22.04
- Root or sudo access
- Domain name (optional but recommended)
- At least 1 GB RAM and 20 GB disk space

## 🚀 Installation

### 1. Update the system

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install system dependencies

```bash
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

### 3. Configure PostgreSQL

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE transfertspace;
CREATE USER transfertspace_user WITH PASSWORD 'your_secure_password';
ALTER ROLE transfertspace_user SET client_encoding TO 'utf8';
ALTER ROLE transfertspace_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE transfertspace_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE transfertspace TO transfertspace_user;
\q
```

### 4. Clone and configure the application

```bash
# Create a system user for the application
sudo useradd -m -s /bin/bash transfertspace
sudo su - transfertspace

# Clone the project (replace with your repository)
git clone https://github.com/your-repo/transfertspace.git
cd transfertspace

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install flask flask-sqlalchemy gunicorn psycopg2-binary werkzeug
```

### 5. Configure environment variables

```bash
# Create .env file
nano .env
```

Add the following content (modify as needed):

```env
DATABASE_URL=postgresql://transfertspace_user:your_secure_password@localhost/transfertspace
SESSION_SECRET=your_very_long_and_random_secret_key
FLASK_ENV=production
```

### 6. Initialize the database

```bash
# Still in the virtual environment
python3 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 7. Configure Gunicorn as systemd service

Exit from transfertspace user:
```bash
exit
```

Create the service file:
```bash
sudo nano /etc/systemd/system/transfertspace.service
```

Add the following content:

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

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start transfertspace
sudo systemctl enable transfertspace
sudo systemctl status transfertspace
```

### 8. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/transfertspace
```

Add the following configuration (adapt your_domain.com):

```nginx
server {
    listen 80;
    server_name your_domain.com www.your_domain.com;

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

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/transfertspace /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configure SSL with Let's Encrypt (Recommended)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your_domain.com -d www.your_domain.com
```

### 10. Configure firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## 📊 Maintenance

### Check logs

```bash
# Application logs
sudo journalctl -u transfertspace -f

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Restart the application

```bash
sudo systemctl restart transfertspace
```

### Update the application

```bash
sudo su - transfertspace
cd transfertspace
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
exit
sudo systemctl restart transfertspace
```

### Backup the database

```bash
sudo -u postgres pg_dump transfertspace > backup_$(date +%Y%m%d).sql
```

### Restore the database

```bash
sudo -u postgres psql transfertspace < backup_20250113.sql
```

## 🔒 Security

1. **Change default passwords** in `.env` and PostgreSQL
2. **Enable firewall** with ufw
3. **Regularly update** system and application
4. **Configure automatic backups** of the database
5. **Monitor logs** regularly to detect suspicious activity

## 🆘 Troubleshooting

### Application won't start

```bash
sudo journalctl -u transfertspace -n 50
```

### Database connection error

Check parameters in `.env` and that PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

### 502 Bad Gateway error

Check that Gunicorn is running:
```bash
sudo systemctl status transfertspace
```

## 📞 Support

For technical assistance, contact:
- Email: moa@myoneart.com
- Web: https://www.myoneart.com

---

© 2025 MOA Digital Agency LLC - TransfertSpace
