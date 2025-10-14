# Money Transfer Calculator: Multi-Tenant SaaS Platform

## Recent Changes

### 2025-10-14: Corrections majeures du système de calcul
- ✅ **Correction critique des frais de transaction**: 
  - Les frais sont maintenant soustraits de la monnaie d'envoi AVANT la conversion (au lieu d'après)
  - Logique corrigée: (montant_envoi - frais) × taux = montant_reçu
  - La devise des frais reflète maintenant correctement la monnaie d'envoi
  - Fichier modifié: `app/utils/calculations.py`
- ✅ **Correction des libellés de taux de change**:
  - Texte corrigé pour MAD → CDF: "Entrez combien de CDF pour 1 MAD" (au lieu de l'inverse)
  - Texte corrigé pour CDF → MAD: "Entrez combien de MAD pour 1 CDF" (au lieu de l'inverse)
  - Fichiers modifiés: `translations/fr.json`, `translations/en.json`
- ✅ **Correction critique précédente**: Résolution de l'erreur `TypeError: replace() argument 2 must be str, not Undefined`
  - Corrigé tous les templates pour utiliser `.currency_code` au lieu de `.currency`
  - Templates affectés: `admin_panel.html`, `index.html`
- ✅ **Script de mise à jour VPS**: Créé `update_vps.sh` avec gestion d'erreurs robuste
- ✅ **Documentation**: Ajouté `COMMANDES_VPS.md` avec instructions complètes de déploiement
- ✅ **Amélioration des taux de change**: 
  - Précision augmentée à 8 décimales
  - Toggle pour calcul automatique/manuel des taux inverses

## Overview

This is a **multi-tenant SaaS platform** for money transfer services. The application has been converted from a single-instance system to a full SaaS model with role-based access control (SuperAdmin and Admin). 

**Key Features:**
- **SuperAdmin**: Manages multiple admin accounts (transfer service operators)
- **Admin**: Each admin operates their own money transfer service with custom branding
- **Multi-Tenancy**: Each admin has a unique URL (`/username`) for their customers
- **Full Configuration**: Each admin can independently configure countries, rates, fees, and WhatsApp contacts

The system allows admins to facilitate money transfers between any two configurable countries with automatic calculations, WhatsApp integration, and comprehensive transaction tracking.

## User Preferences

Preferred communication style: Simple, everyday language.

## SaaS Features & Multi-Tenancy

### Role-Based Access Control
1. **SuperAdmin Role**
   - Full system administration capabilities
   - Can create, edit, suspend, activate, and delete admin accounts
   - Access to comprehensive dashboard with system-wide statistics
   - Monitors all transactions across all admin accounts
   - Login: `/superadmin/login`

2. **Admin Role**
   - Operates independent money transfer service
   - Unique username-based URL for customers (`/username`)
   - Full configuration control (countries, rates, fees, branding)
   - View transaction history for their account only
   - Login: `/admin/`

### SuperAdmin Dashboard Features
- **Statistics Overview**: Total admins, active/suspended accounts, total transactions
- **Admin Management**: CRUD operations for admin accounts
- **Per-Admin Analytics**: Transaction count and volume for each admin
- **Recent Activity**: Track new admin registrations
- **Transaction Monitoring**: View transactions filtered by admin account

### Admin Configuration Capabilities
Each admin can independently configure:
- Source and destination countries
- Exchange rates (bidirectional) with advanced features:
  - **High-precision calculation**: 8 decimal places for accurate rates
  - **Automatic inverse calculation**: Toggle to auto-calculate inverse rates or enter manually
  - **Manual mode**: Allows independent rate setting for both directions
- Tiered transaction fees
- WhatsApp contact numbers (dual contact system)
- Reception methods per country
- Custom branding (app title and promotional content)
- Password management

### Multi-Tenant Architecture
- **URL Structure**: Each admin gets unique customer-facing URL at `/{username}`
- **Data Isolation**: Transactions are linked to specific admin accounts
- **Account Status**: Admins can be suspended/activated by SuperAdmin
- **Suspended Account Handling**: Displays user-friendly message when admin is suspended

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla JavaScript with Tailwind CSS for styling.
- **Design Pattern**: Single-page application (SPA) with dynamic DOM manipulation.
- **UI/UX Decisions**: Gradient background, card-based layout for a modern, mobile-first, and responsive interface.

### Backend Architecture
- **Framework**: Flask (Python) with SQLAlchemy ORM.
- **Architecture Pattern**: Modular MVC-style structure utilizing Flask Blueprints for clear separation of concerns.
- **Blueprints**:
  - `main_bp`: Public-facing routes and user transfer pages
  - `admin_bp`: Admin panel and configuration
  - `superadmin_bp`: SuperAdmin dashboard and management
- **Code Organization**: 
  - `routes/`: Blueprint definitions (main, admin, superadmin)
  - `models/`: Database models (Admin, AdminConfig, Transaction)
  - `utils/`: Calculation and security utilities
  - `data/`: Country and currency information (54+ countries)
- **Database Models**:
  - `Admin`: User accounts with role (admin/superadmin) and status (active/suspended)
    - New fields: `full_name` (nom complet) et `whatsapp_number` (numéro WhatsApp)
  - `AdminConfig`: Per-admin configuration (countries, rates, fees, branding)
  - `Transaction`: Transaction records linked to admin accounts
- **Country & Currency System**: Comprehensive database of 54+ countries with multiple currencies per country where applicable.

### Exchange Rate & Calculation System
- **Configuration**: Exchange rates and tiered transaction fees are configurable via the admin panel and stored in `config.json`.
- **Bidirectional Calculation**: Supports two modes: calculating received amount from send amount, and calculating required send amount from desired receive amount.
- **Rounding Strategy**: All monetary amounts use ceiling rounding (`math.ceil`) to round up to the nearest cent, ensuring transparency. Iterative adjustment is used in receive-mode to handle fee tier boundaries.
- **Dynamic Adaptability**: All calculations, labels, and currency symbols automatically update based on the dynamically selected countries and currencies.

### Admin Panel
- **Access & Authentication**: `/admin/` route with session-based authentication
- **Password Security**: Werkzeug password hashing (PBKDF2-SHA256)
- **Capabilities**: 
  - Select and configure Country 1 and Country 2
  - Set exchange rates for both directions
  - Configure tiered transaction fees
  - Set up dual WhatsApp contacts (different for each direction)
  - Customize branding (title and promotional content)
  - Configure reception methods per country
  - Change admin password
  - View transaction history

### SuperAdmin Panel
- **Access & Authentication**: `/superadmin/login` with role verification
- **Dashboard**: System-wide statistics and admin management with modern, cohesive design
- **Admin Management**:
  - Create new admin accounts with username, email, full name, WhatsApp number, and reception methods
  - Edit admin credentials (email, password, full name, WhatsApp number)
  - Suspend/activate admin accounts via toggle switches
  - Delete admin accounts
  - View per-admin transaction history
- **Design**: Modern gradient-based interface with card layouts, smooth transitions, and responsive design
- **Security**: Only users with `role='superadmin'` can access

### Security Considerations
- **Password Security**: Werkzeug password hashing with PBKDF2-SHA256
- **Session Management**: Flask secure sessions with configurable lifetime
- **Role-Based Access**: Separate authentication for admin and superadmin
- **Status Checks**: Active account verification on each protected request
- **CSRF Protection**: Session-based CSRF protection
- **Data Isolation**: Admins can only access their own transactions

## External Dependencies

### Frontend
- **Tailwind CSS**: Loaded via CDN for utility-first styling.

### Backend
- **Python Standard Library**: `urllib.parse` for URL encoding.

### Integration Services
- **WhatsApp**: Utilizes the `wa.me` API for sending pre-filled transfer requests. Features a dual contact system allowing different WhatsApp numbers and contact names for each transfer direction.

### Data Storage
- **PostgreSQL**: Used for transaction history, storing details of all WhatsApp transfer requests. This includes date/time, direction, amounts, currencies, reception method, and contact details.
- **Database Tables**:
  - `admins`: User accounts (admin and superadmin)
  - `admin_configs`: Per-admin configuration settings
  - `transactions`: Transaction records linked to admin accounts

### Reception Methods
- **Configurable per country**, e.g., Airtel Money and Equity Bank for RDC (USD), Cash and CIH Bank for Morocco (MAD).

## URL Structure & Routes

### Public Routes
- `/` - Landing page with login options (SuperAdmin and Admin)
- `/{username}` - Customer-facing transfer page for specific admin

### Admin Routes
- `/admin/` - Admin login page (GET) or admin dashboard (when authenticated)
- `/admin/login` - Admin login endpoint (POST)
- `/admin/update` - Save admin configuration (POST)
- `/admin/history` - View admin's transaction history
- `/admin/logout` - Admin logout

### SuperAdmin Routes
- `/superadmin/login` - SuperAdmin login page and endpoint
- `/superadmin/dashboard` - SuperAdmin dashboard with statistics
- `/superadmin/admins` - List all admin accounts
- `/superadmin/admins/create` - Create new admin account
- `/superadmin/admins/{id}/edit` - Edit admin account
- `/superadmin/admins/{id}/suspend` - Suspend admin account (POST)
- `/superadmin/admins/{id}/activate` - Activate admin account (POST)
- `/superadmin/admins/{id}/delete` - Delete admin account (POST)
- `/superadmin/admins/{id}/transactions` - View admin's transaction history
- `/superadmin/logout` - SuperAdmin logout

## Getting Started

### Initial SuperAdmin Setup
Le compte SuperAdmin se crée **automatiquement** au démarrage de l'application avec les identifiants suivants:
- **Username**: `myoneart`
- **Email**: `moa@myoneart.com`
- **Mot de passe**: `my0n34rt`

Pour utiliser le SuperAdmin:
1. Accédez à la page d'accueil `/`
2. Connectez-vous avec les identifiants ci-dessus
3. Vous serez redirigé vers le dashboard SuperAdmin
4. Créez des comptes admin depuis le dashboard

**Note**: Si vous souhaitez créer un SuperAdmin différent, vous pouvez utiliser le script `python init_superadmin.py`

### Creating Admin Accounts
1. Login as SuperAdmin
2. Navigate to "Admins" section
3. Click "Create Admin"
4. Enter username (used for customer URL), email, and password
5. New admin can now login at `/admin/` and configure their service

### Admin Configuration
1. Login at `/admin/`
2. Configure:
   - Source and destination countries
   - Exchange rates (both directions)
   - Transaction fee tiers
   - WhatsApp contact numbers
   - Reception methods
   - Branding (title and promotional content)
3. Share customer URL: `yourdomain.com/{username}`