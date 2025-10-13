# 🔐 Identifiants SuperAdmin

## Compte Principal

Le compte SuperAdmin est créé **automatiquement** au démarrage de l'application.

### Connexion
- **URL** : `/` (page d'accueil)
- **Nom d'utilisateur** : `myoneart`
- **Email** : `moa@myoneart.com`
- **Mot de passe** : `my0n34rt`

### Sécurité
- ✅ Création automatique au déploiement
- ✅ Mot de passe haché avec **Werkzeug** (PBKDF2-SHA256)
- ✅ Rôle : `superadmin`
- ✅ Statut : `active`

## Accès SuperAdmin

### Dashboard SuperAdmin
Une fois connecté, vous aurez accès à :
- **Statistiques globales** : Nombre d'admins, transactions, etc.
- **Gestion des admins** : Créer, éditer, suspendre, activer, supprimer
- **Analytics** : Statistiques par admin (transactions, volume)
- **Historique** : Vue des transactions par admin

### Créer un Admin
1. Connectez-vous sur `/`
2. Allez dans "Admins"
3. Cliquez "Créer Admin"
4. Remplissez :
   - Username (sera l'URL `/{username}`)
   - Email
   - Mot de passe

## Structure de la Plateforme

### URLs
- `/` → Connexion SuperAdmin
- `/superadmin/dashboard` → Dashboard SuperAdmin
- `/admin/` → Connexion Admin
- `/{username}` → Page client pour un admin spécifique

### Base de Données
- **Statut** : ✅ PostgreSQL créée et configurée
- **Tables** :
  - `admins` : Comptes utilisateurs (admin/superadmin)
  - `admin_configs` : Configurations par admin
  - `transactions` : Historique des transactions

---

**Note de sécurité** : Gardez ces identifiants en lieu sûr. Le compte SuperAdmin a un accès complet à la plateforme.
