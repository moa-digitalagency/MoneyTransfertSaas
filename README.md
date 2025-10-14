# TransfertSpace - Plateforme SaaS Multi-Tenant de Transfert d'Argent

Application web SaaS configurable permettant à plusieurs opérateurs de transfert d'argent de gérer leurs services de transfert entre n'importe quelle paire de pays avec conversion automatique de devises.

## 🌍 Fonctionnalités Principales

### Architecture Multi-Tenant SaaS
- 🏢 **TransfertSpace** : Plateforme centralisée de gestion
- 👥 **Multi-Opérateurs** : Chaque admin gère son propre service de transfert
- 🔗 **URL Unique** : Chaque admin dispose d'une URL personnalisée (`/username`)
- 📱 **Demande d'Inscription** : Bouton WhatsApp pour créer un nouveau compte admin
- 🎨 **Branding Personnalisable** : Chaque admin configure son propre service

### Fonctionnalités de Transfert
- 🌐 **Configuration Multi-Pays** : Support de 54+ pays et leurs devises
  - Sélectionnez n'importe quelle paire de pays depuis le panneau admin
  - Support de devises multiples : USD, EUR, MAD, CDF, FCFA (XOF/XAF), GBP, CAD, KES, RWF, et plus
  - Interface dynamique qui s'adapte automatiquement aux pays sélectionnés
  
- 🔄 **Contrôle des Directions de Transfert** : 
  - Activez/désactivez indépendamment chaque direction (Pays 1 → Pays 2 ou Pays 2 → Pays 1)
  - Configurez des transferts unidirectionnels ou bidirectionnels
  - Interface client s'adapte automatiquement aux directions disponibles
  - Par défaut, les deux directions sont activées (compatibilité descendante)

- 💱 **Calcul bidirectionnel** : Transferts dans les deux directions configurables
- 💰 **Deux modes de calcul** : 
  - Montant à envoyer (calcule le montant reçu)
  - Montant à recevoir (calcule le montant à envoyer)
- 💵 **Frais de transaction** : Jusqu'à 10 paliers configurables pour chaque direction
- 🔄 **Calcul automatique inverse** : Les taux de change inverses se calculent automatiquement
- 📱 **Intégration WhatsApp** : envoi direct de la demande de transfert avec contacts configurables
- ⚙️ **Panneau d'administration** : gestion complète des pays, devises, taux, frais et paramètres
- 🔐 **Sécurité** : authentification avec hachage de mot de passe sécurisé

### Rôles et Permissions

#### TransfertSpace (SuperAdmin)
- Gestion complète de tous les comptes admin
- Création, modification, suspension et suppression d'admins
- Visualisation des statistiques globales
- Accès à l'historique de toutes les transactions
- **Login** : `myoneart` / `my0n34rt` (à changer immédiatement !)

#### Admins
- Gestion de leur propre service de transfert
- Configuration des pays, devises, taux et frais
- URL personnalisée pour leurs clients (`/username`)
- Historique de leurs propres transactions
- **Login** : `/admin/`

## 📋 Demande d'Inscription

Les utilisateurs peuvent demander la création d'un compte admin via un formulaire accessible sur la page d'accueil :

### Comment ça marche?

1. **Bouton "Demander un compte"** sur la page principale
2. **Formulaire de demande** avec :
   - Nom complet
   - Numéro WhatsApp
   - Pays d'origine (envoi) et devise
   - Pays de destination (réception) et devise
3. **Envoi automatique** de la demande au numéro WhatsApp : **+212699140001**
4. **Notification par WhatsApp** : Une fois le compte créé par le SuperAdmin, l'utilisateur reçoit ses identifiants de connexion et son URL personnalisée directement sur WhatsApp

### Concept Important

- **Transferts toujours internationaux** : Les transferts se font toujours entre deux pays différents (ex: Maroc ↔ RDC, France ↔ Sénégal)
- **Demande d'inscription** : Il s'agit d'une demande, pas d'une création automatique
- **Validation manuelle** : Le SuperAdmin valide et crée le compte
- **URL personnalisée** : Chaque admin reçoit son propre lien `/username` pour ses clients

## Exemples de Configurations Possibles

- **RDC (USD) ⇄ Maroc (MAD)**
- **Côte d'Ivoire (FCFA) ⇄ Maroc (MAD)**
- **Sénégal (FCFA) ⇄ France (EUR)**
- **Kenya (KES) ⇄ Rwanda (RWF)**
- **Cameroun (FCFA) ⇄ Canada (CAD)**
- **Rép. du Congo (FCFA) ⇄ Belgique (EUR)**
- Ou n'importe quelle autre combinaison des 54+ pays disponibles !

## Installation

### Prérequis
- Python 3.11 ou supérieur
- PostgreSQL (pour la base de données)

### Installation des dépendances

```bash
pip install -r requirements.txt
```

## Démarrage

### Mode développement

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

L'application sera accessible sur `http://localhost:5000`

### Mode production

```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port --workers 4 main:app
```

## Configuration

### Premier Accès TransfertSpace (SuperAdmin)

Le compte TransfertSpace est créé automatiquement au démarrage :

- **Username** : `myoneart`
- **Email** : `moa@myoneart.com`
- **Mot de passe** : `my0n34rt`

⚠️ **Changez ce mot de passe immédiatement après la première connexion !**

### Créer un Admin

1. Connectez-vous en tant que TransfertSpace
2. Accédez à "Admins" puis "Créer un Admin"
3. Remplissez les informations :
   - Username (sera l'URL : `/username`)
   - Nom complet
   - Email
   - Numéro WhatsApp
   - Mot de passe
   - Pays 1 et Devise
   - Pays 2 et Devise
   - Moyens de réception

### Configuration Admin

Chaque admin peut configurer :

#### Pays et Devises
- **Pays 1 & Pays 2** : Sélection parmi 54+ pays avec drapeaux
- **Devises** : Mise à jour automatique selon le pays sélectionné

#### Taux de Change
- **Calcul automatique inverse** : Entrez USD→MAD = 10, MAD→USD = 0.1 se calcule automatiquement
- Précision jusqu'à 6 décimales

#### Frais de Transaction
- **Jusqu'à 10 paliers** pour chaque direction
- Seuls les paliers remplis sont pris en compte
- Configuration Min/Max/Frais pour chaque palier

#### Autres Paramètres
- **Contacts WhatsApp** : Numéros et noms séparés pour chaque direction
- **Moyens de Réception** : Personnalisables par pays
- **Bloc Application** : Titre et contenu du bloc promotionnel
- **Mot de passe** : Changement sécurisé du mot de passe admin

### Pays et Devises Disponibles

L'application supporte 54+ pays incluant :

| Région | Pays Disponibles |
|--------|------------------|
| **Afrique Centrale** | RDC (USD, CDF), Rép. du Congo (FCFA), Cameroun (FCFA), Gabon (FCFA), Tchad (FCFA), Centrafrique (FCFA) |
| **Afrique de l'Ouest** | Côte d'Ivoire (FCFA), Sénégal (FCFA), Mali (FCFA), Burkina Faso (FCFA), Bénin (FCFA), Togo (FCFA), Niger (FCFA), Nigeria (NGN), Ghana (GHS), Guinée (GNF) |
| **Afrique du Nord** | Maroc (MAD), Tunisie (TND), Algérie (DZD), Égypte (EGP), Libye (LYD) |
| **Afrique de l'Est** | Kenya (KES), Rwanda (RWF), Ouganda (UGX), Tanzanie (TZS), Éthiopie (ETB), Burundi (BIF) |
| **Afrique Australe** | Afrique du Sud (ZAR), Zimbabwe (USD), Botswana (BWP), Namibie (NAD), Mozambique (MZN), Zambie (ZMW) |
| **Europe** | France (EUR), Belgique (EUR), Royaume-Uni (GBP) |
| **Amérique** | États-Unis (USD), Canada (CAD) |
| **Océan Indien** | Madagascar (MGA), Maurice (MUR), Seychelles (SCR) |

## Structure du projet

```
.
├── app/
│   ├── __init__.py
│   ├── config/
│   │   └── settings.py
│   ├── data/
│   │   ├── countries.py         # 54+ pays et devises
│   │   └── __init__.py
│   ├── models/
│   │   ├── admin.py            # Modèles Admin et AdminConfig
│   │   └── transaction.py      # Modèle Transaction
│   ├── routes/
│   │   ├── main.py            # Routes publiques
│   │   ├── admin.py           # Routes admin
│   │   └── superadmin.py      # Routes TransfertSpace + DB management
│   ├── utils/
│   │   ├── calculations.py    # Calculs avec 10 paliers
│   │   ├── security.py        # Hachage de mots de passe
│   │   ├── db_management.py   # Gestion BD, backups, GitHub
│   │   └── i18n.py            # Système de traduction
│   └── database.py            # Configuration PostgreSQL
├── backups/                   # Sauvegardes de la base de données
├── templates/
│   ├── welcome.html           # Page d'accueil avec inscription
│   ├── index.html             # Interface de transfert client
│   ├── admin_login.html       # Login admin
│   ├── admin_panel.html       # Panneau admin (10 paliers)
│   ├── superadmin_*.html      # Interfaces TransfertSpace
│   └── ...
├── static/
│   ├── background.jpg
│   └── bg-transfer.jpg
├── main.py                    # Point d'entrée
├── requirements.txt
└── pyproject.toml
```

## Base de Données PostgreSQL

L'application utilise PostgreSQL avec 3 tables principales :

- **admins** : Comptes admin et TransfertSpace
- **admin_configs** : Configurations personnalisées par admin
- **transactions** : Historique de toutes les transactions

## Déploiement

### Variables d'environnement

```bash
DATABASE_URL=postgresql://...
SESSION_SECRET=votre_clé_secrète
```

### Déploiement sur serveur

1. Configurez PostgreSQL
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez avec Gunicorn : `gunicorn --bind=0.0.0.0:5000 --workers 4 main:app`
4. Configurez un reverse proxy (Nginx/Apache) si nécessaire

## Sécurité

⚠️ **Important pour la production** :
- **Changez IMMÉDIATEMENT** le mot de passe TransfertSpace par défaut
- Utilisez HTTPS pour toutes les communications
- Configurez `SESSION_SECRET` avec une valeur aléatoire sécurisée
- Limitez les tentatives de connexion
- Effectuez des sauvegardes régulières de la base de données

## 🔧 Gestion de Base de Données et Déploiement

### Système de Gestion de Base de Données

Le SuperAdmin dispose d'un système complet de gestion de base de données accessible depuis le menu **"Base de données"** :

#### 🔄 Mises à Jour Automatiques depuis GitHub
- **Repository GitHub** : https://github.com/moa-digitalagency/MoneyTransfertSaas.git
- **Vérification des mises à jour** : Détection automatique des nouvelles versions
- **Mise à jour en un clic** : Pull depuis GitHub avec exécution automatique des migrations
- **Backup automatique** : Sauvegarde complète de la base de données avant chaque mise à jour

#### 💾 Système de Backup
- **Création manuelle** : Créez des sauvegardes à la demande
- **Backup automatique** : Avant chaque mise à jour GitHub
- **Restauration** : Restaurez n'importe quelle sauvegarde en un clic
- **Stockage local** : Les backups sont stockés dans le dossier `/backups`
- **Format PostgreSQL** : Fichiers `.sql` compatibles avec pg_dump/pg_restore

#### 🔀 Système de Migrations
- **Migrations automatiques** : Détection et exécution automatique des fichiers `migrate_*.py`
- **Suivi des migrations** : Historique complet dans le journal d'activité
- **Rollback** : Restaurez une sauvegarde en cas de problème

#### 📊 Journal d'Activité
- Suivi de toutes les opérations (backups, restaurations, mises à jour)
- Horodatage précis de chaque action
- Codes de couleur pour les succès/erreurs

### Déploiement sur Replit

#### Configuration du Domaine/Sous-domaine

Pour configurer un domaine personnalisé (ex: `gec.my-app.site`) :

1. **Depuis l'interface Replit** :
   - Cliquez sur "Deploy" dans votre Repl
   - Allez dans "Settings" > "Domains"
   - Ajoutez votre domaine personnalisé
   - Suivez les instructions pour configurer les DNS

2. **Configuration automatique** :
   ```bash
   # Replit configure automatiquement les variables d'environnement
   REPLIT_DOMAINS=gec.my-app.site
   REPLIT_DEV_DOMAIN=gec.my-app.site
   ```

#### Déploiement Automatique

La configuration de déploiement est déjà en place :

```bash
# Mode production avec autoscaling
gunicorn --bind=0.0.0.0:5000 --reuse-port main:app
```

**Options de déploiement** :
- **Autoscale** : S'adapte automatiquement à la charge (recommandé pour ce projet)
- **VM** : Serveur toujours actif (pour services temps réel)
- **Scheduled** : Exécution programmée (pour tâches cron)

#### Mise à Jour depuis GitHub

1. **Accédez à la gestion de base de données** : `/superadmin/database`
2. **Vérifiez les mises à jour** : Cliquez sur "Vérifier les mises à jour"
3. **Mise à jour** : Cliquez sur "Mettre à jour et migrer"
   - ✅ Backup automatique de la base de données
   - ✅ Pull du code depuis GitHub
   - ✅ Exécution des migrations
   - ✅ Journal d'activité complet

## Nouvelles Fonctionnalités (Octobre 2025)

✨ **Dernières améliorations** :
- 🗄️ **Système de gestion de base de données** : Interface complète pour backups, restaurations et mises à jour
- 🔄 **Mises à jour GitHub automatiques** : Pull depuis GitHub avec migrations automatiques
- 💾 **Backups automatiques** : Sauvegarde avant chaque mise à jour
- 🔀 **Système de migrations** : Exécution automatique des scripts de migration
- 📊 **Journal d'activité** : Suivi complet de toutes les opérations de base de données
- 🌐 **Support domaines personnalisés** : Configuration facile via Replit
- 🎨 Boutons d'action améliorés (Modifier, Supprimer, Transactions)
- 🔄 Toggle de statut admin amélioré avec feedback
- 🌍 Liste complète de 54+ pays avec devises dynamiques
- 📊 Extension à 10 paliers de frais de transaction
- 🔢 Calcul automatique inverse des taux de change
- 📝 Formulaire de demande d'inscription via WhatsApp
- 🏷️ Rebranding : SuperAdmin → TransfertSpace

## Support

Pour toute question ou problème :
- **Email** : moa@myoneart.com
- **WhatsApp** : +212699140001
- **Website** : [www.myoneart.com](https://www.myoneart.com)

---

**TransfertSpace**  
By **[MOA Digital Agency LLC](https://www.myoneart.com)**  
Developed by: **Aisance KALONJI**  
Transfert Monétaire Facile, Bénéfique & Rapide
