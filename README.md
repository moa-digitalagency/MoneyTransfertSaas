# Transfert Monétique - Application Multi-Pays de Transfert d'Argent

Application web configurable pour calculer les transferts d'argent entre n'importe quelle paire de pays avec conversion automatique de devises.

## 🌍 Fonctionnalités Principales

- 🌐 **Configuration Multi-Pays** : Support de 24+ pays et leurs devises
  - Sélectionnez n'importe quelle paire de pays depuis le panneau admin
  - Support de devises multiples : USD, EUR, MAD, FCFA, GBP, CAD, KES, RWF, et plus
  - Interface dynamique qui s'adapte automatiquement aux pays sélectionnés
  
- 💱 **Calcul bidirectionnel** : Transferts dans les deux directions configurables
- 💰 **Deux modes de calcul** : 
  - Montant à envoyer (calcule le montant reçu)
  - Montant à recevoir (calcule le montant à envoyer)
- 💵 **Frais de transaction par paliers** configurables pour chaque direction
- 📱 **Intégration WhatsApp** : envoi direct de la demande de transfert avec contacts configurables
- ⚙️ **Panneau d'administration** : gestion complète des pays, devises, taux, frais et paramètres
- 🔐 **Sécurité** : authentification admin avec hachage SHA-256 et protection CSRF

## Exemples de Configurations Possibles

- **RDC (USD) ⇄ Maroc (MAD)** - Configuration par défaut
- **Côte d'Ivoire (FCFA) ⇄ Maroc (MAD)**
- **Sénégal (FCFA) ⇄ France (EUR)**
- **Kenya (KES) ⇄ Rwanda (RWF)**
- **Cameroun (FCFA) ⇄ Canada (CAD)**
- Ou n'importe quelle autre combinaison des 24+ pays disponibles !

## Installation

### Prérequis
- Python 3.11 ou supérieur

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou avec uv :

```bash
uv sync
```

## Démarrage

### Mode développement

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

### Mode production (avec Gunicorn)

```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port app:app
```

Pour un déploiement avec plusieurs workers :

```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port --workers 4 app:app
```

## Configuration

### Accès au panneau d'administration

1. Cliquez sur le lien **"For Admin"** en bas de la page d'accueil
2. Connectez-vous avec le mot de passe admin par défaut : **`admin`**
3. Vous pouvez configurer :

#### Configuration des Pays et Devises
- **Pays 1** : Sélectionnez le premier pays (avec drapeau)
- **Devise Pays 1** : Choisissez la devise pour ce pays
- **Pays 2** : Sélectionnez le deuxième pays (avec drapeau)
- **Devise Pays 2** : Choisissez la devise pour ce pays

#### Autres Paramètres
- **Taux de change** : Entre les deux devises sélectionnées (bidirectionnel)
- **Frais de transaction** : Par palier pour chaque direction
- **Contacts WhatsApp** : Numéros et noms séparés pour chaque direction
- **Bloc Application** : Titre et contenu du bloc promotionnel
- **Mot de passe admin** : Changez le mot de passe par défaut

### Pays et Devises Disponibles

L'application supporte 24+ pays incluant :

| Pays | Drapeau | Devises Disponibles |
|------|---------|-------------------|
| RDC | 🇨🇩 | USD, CDF |
| Maroc | 🇲🇦 | MAD |
| Côte d'Ivoire | 🇨🇮 | XOF (FCFA) |
| Sénégal | 🇸🇳 | XOF (FCFA) |
| Cameroun | 🇨🇲 | XAF (FCFA) |
| France | 🇫🇷 | EUR |
| Belgique | 🇧🇪 | EUR |
| Canada | 🇨🇦 | CAD |
| États-Unis | 🇺🇸 | USD |
| Royaume-Uni | 🇬🇧 | GBP |
| Kenya | 🇰🇪 | KES |
| Rwanda | 🇷🇼 | RWF |
| Et 12+ autres pays... | | |

### Fichier config.json

Le fichier `config.json` contient toutes les configurations :

```json
{
  "admin_password_hash": "hash_du_mot_de_passe",
  "countries": {
    "country1": {
      "code": "RDC",
      "currency_code": "USD"
    },
    "country2": {
      "code": "MA",
      "currency_code": "MAD"
    }
  },
  "rates": {
    "country1_to_country2": 10.2,
    "country2_to_country1": 0.098
  },
  "transaction_fees": {
    "country1_to_country2": [...],
    "country2_to_country1": [...]
  },
  "whatsapp": {
    "country1_to_country2": {
      "phone": "212600265350",
      "contact_name": "Néhémie"
    },
    "country2_to_country1": {
      "phone": "212600265350",
      "contact_name": "Néhémie"
    }
  }
}
```

## Structure du projet

```
.
├── app/
│   ├── __init__.py          # Application Flask factory
│   ├── config/
│   │   └── settings.py      # Gestion de config.json
│   ├── data/
│   │   ├── countries.py     # Base de données des pays et devises
│   │   └── __init__.py
│   ├── models/
│   │   └── transaction.py   # Logique WhatsApp et transactions
│   ├── routes/
│   │   ├── main.py         # Routes principales
│   │   └── admin.py        # Routes admin
│   └── utils/
│       ├── calculations.py  # Calculs avec arrondis
│       └── security.py      # Hachage de mots de passe
├── templates/
│   ├── index.html          # Page principale (dynamique)
│   ├── admin_login.html    # Login admin
│   └── admin_panel.html    # Panneau d'administration
├── static/
│   └── bg-transfer.jpg     # Image de fond
├── app.py                  # Point d'entrée
├── config.json            # Configuration (pays, taux, frais)
├── requirements.txt       # Dépendances Python
└── pyproject.toml         # Configuration uv
```

## Déploiement

### Sur un serveur

1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Configurez les variables d'environnement si nécessaire

3. Lancez avec Gunicorn :
   ```bash
   gunicorn --bind=0.0.0.0:5000 --workers 4 app:app
   ```

4. (Optionnel) Configurez un reverse proxy (Nginx/Apache)

### Variables d'environnement (optionnel)

Vous pouvez utiliser les variables d'environnement pour la production :
- `FLASK_SECRET_KEY` : Clé secrète Flask (sinon générée aléatoirement)
- `PORT` : Port d'écoute (défaut: 5000)

## Sécurité

⚠️ **Important pour la production** :
- **Changez IMMÉDIATEMENT le mot de passe admin par défaut** (`admin` → votre mot de passe sécurisé)
- Utilisez HTTPS pour les communications
- Configurez une clé secrète Flask fixe via variable d'environnement
- Envisagez d'utiliser bcrypt ou argon2 pour le hachage des mots de passe
- Ajoutez une limitation du taux de tentatives de connexion

## Comment Changer de Pays

1. Connectez-vous au panneau admin
2. Dans **"Configuration des Pays"** :
   - Sélectionnez votre nouveau **Pays 1** (ex: Côte d'Ivoire 🇨🇮)
   - Choisissez sa **devise** (ex: XOF - Franc CFA)
   - Sélectionnez votre nouveau **Pays 2** (ex: France 🇫🇷)
   - Choisissez sa **devise** (ex: EUR - Euro)
3. Ajustez les **taux de change** entre FCFA et EUR
4. Configurez les **frais** pour chaque direction
5. Mettez à jour les **contacts WhatsApp** si nécessaire
6. Enregistrez

**Tout le reste s'adapte automatiquement** : interface, drapeaux, calculs, et messages !

## Support

Pour toute question ou problème :
- Contactez le support via WhatsApp au numéro configuré dans l'application

---

**MoneyTransfert**  
By **MOA Digital Agency LLC**  
Developed by: **Aisance KALONJI**  
Contact: moa@myoneart.com  
www.myoneart.com
