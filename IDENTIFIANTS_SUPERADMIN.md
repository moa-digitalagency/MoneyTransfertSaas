# 🔐 Identifiants SuperAdmin

## Compte Principal

Voici les identifiants pour accéder au panneau SuperAdmin :

### Connexion
- **URL** : `/` (page d'accueil)
- **Nom d'utilisateur** : `myoneart`
- **Email** : `moa@myoneart.com`
- **Mot de passe** : `my0n34rt`

### Sécurité
- ✅ Mot de passe haché avec **scrypt** (algorithme Werkzeug)
- ✅ Hash : `scrypt:32768:8:1$F3WTigOKIFIA0yRj$72ff6424d8d59ca4e857399b9fb97eb707f21604d364d80a7df7475ffaf768ad8874cdeb8bbe8a4738523e72c14a4ef47f6000d1a73d928c13f5d5a26e4be660`
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
