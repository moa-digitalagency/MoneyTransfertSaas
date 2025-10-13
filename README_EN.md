# TransfertSpace - Multi-Tenant Money Transfer SaaS Platform

Configurable SaaS web application allowing multiple money transfer operators to manage their transfer services between any pair of countries with automatic currency conversion.

## 🌍 Main Features

### Multi-Tenant SaaS Architecture
- 🏢 **TransfertSpace**: Centralized management platform
- 👥 **Multi-Operators**: Each admin manages their own transfer service
- 🔗 **Unique URL**: Each admin has a personalized URL (`/username`)
- 📱 **Registration Request**: WhatsApp button to create a new admin account
- 🎨 **Customizable Branding**: Each admin configures their own service

### Transfer Features
- 🌐 **Multi-Country Configuration**: Support for 54+ countries and their currencies
  - Select any country pair from the admin panel
  - Multiple currency support: USD, EUR, MAD, CDF, FCFA (XOF/XAF), GBP, CAD, KES, RWF, and more
  - Dynamic interface that automatically adapts to selected countries
  
- 💱 **Bidirectional Calculation**: Transfers in both configurable directions
- 💰 **Two Calculation Modes**: 
  - Amount to send (calculates received amount)
  - Amount to receive (calculates amount to send)
- 💵 **Transaction Fees**: Up to 10 configurable tiers for each direction
- 🔄 **Automatic Inverse Calculation**: Inverse exchange rates are calculated automatically
- 📱 **WhatsApp Integration**: Direct transfer request sending with configurable contacts
- ⚙️ **Administration Panel**: Complete management of countries, currencies, rates, fees, and settings
- 🔐 **Security**: Authentication with secure password hashing

### Roles and Permissions

#### TransfertSpace (SuperAdmin)
- Complete management of all admin accounts
- Creation, modification, suspension, and deletion of admins
- View global statistics
- Access to all transaction history
- **Login**: `myoneart` / `my0n34rt` (change immediately!)

#### Admins
- Management of their own transfer service
- Configuration of countries, currencies, rates, and fees
- Personalized URL for their clients (`/username`)
- History of their own transactions
- **Login**: `/admin/`

## 📋 Registration Request

Users can request the creation of an admin account via a form accessible on the homepage:

### How does it work?

1. **"Request an account" button** on the main page
2. **Request form** with:
   - Full name
   - WhatsApp number
   - Origin country (sending) and currency
   - Destination country (receiving) and currency
3. **Automatic sending** of the request to WhatsApp number: **+212699140001**
4. **WhatsApp Notification**: Once the account is created by the SuperAdmin, the user receives their login credentials and personalized URL directly on WhatsApp

### Important Concept

- **Always international transfers**: Transfers are always between two different countries (e.g., Morocco ↔ DRC, France ↔ Senegal)
- **Registration request**: This is a request, not an automatic creation
- **Manual validation**: The SuperAdmin validates and creates the account
- **Personalized URL**: Each admin receives their own `/username` link for their clients

## Possible Configuration Examples

- **DRC (USD) ⇄ Morocco (MAD)**
- **Ivory Coast (FCFA) ⇄ Morocco (MAD)**
- **Senegal (FCFA) ⇄ France (EUR)**
- **Kenya (KES) ⇄ Rwanda (RWF)**
- **Cameroon (FCFA) ⇄ Canada (CAD)**
- **Republic of Congo (FCFA) ⇄ Belgium (EUR)**
- Or any other combination of the 54+ available countries!

## Installation

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (for the database)

### Installing dependencies

```bash
pip install -r requirements.txt
```

## Getting Started

### Development mode

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

The application will be accessible at `http://localhost:5000`

### Production mode

```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port --workers 4 main:app
```

## Configuration

### First TransfertSpace Access (SuperAdmin)

The TransfertSpace account is created automatically at startup:

- **Username**: `myoneart`
- **Email**: `moa@myoneart.com`
- **Password**: `my0n34rt`

⚠️ **Change this password immediately after first login!**

### Create an Admin

1. Log in as TransfertSpace
2. Go to "Admins" then "Create Admin"
3. Fill in the information:
   - Username (will be the URL: `/username`)
   - Full name
   - Email
   - WhatsApp number
   - Password
   - Country 1 and Currency
   - Country 2 and Currency
   - Reception methods

### Admin Configuration

Each admin can configure:

#### Countries and Currencies
- **Country 1 & Country 2**: Selection from 54+ countries with flags
- **Currencies**: Automatic update according to selected country

#### Exchange Rates
- **Automatic inverse calculation**: Enter USD→MAD = 10, MAD→USD = 0.1 is calculated automatically
- Precision up to 6 decimals

#### Transaction Fees
- **Up to 10 tiers** for each direction
- Only filled tiers are taken into account
- Min/Max/Fee configuration for each tier

#### Other Settings
- **WhatsApp Contacts**: Separate numbers and names for each direction
- **Reception Methods**: Customizable by country
- **Application Block**: Title and content of promotional block
- **Password**: Secure admin password change

### Available Countries and Currencies

The application supports 54+ countries including:

| Region | Available Countries |
|--------|---------------------|
| **Central Africa** | DRC (USD, CDF), Rep. of Congo (FCFA), Cameroon (FCFA), Gabon (FCFA), Chad (FCFA), Central African Republic (FCFA) |
| **West Africa** | Ivory Coast (FCFA), Senegal (FCFA), Mali (FCFA), Burkina Faso (FCFA), Benin (FCFA), Togo (FCFA), Niger (FCFA), Nigeria (NGN), Ghana (GHS), Guinea (GNF) |
| **North Africa** | Morocco (MAD), Tunisia (TND), Algeria (DZD), Egypt (EGP), Libya (LYD) |
| **East Africa** | Kenya (KES), Rwanda (RWF), Uganda (UGX), Tanzania (TZS), Ethiopia (ETB), Burundi (BIF) |
| **Southern Africa** | South Africa (ZAR), Zimbabwe (USD), Botswana (BWP), Namibia (NAD), Mozambique (MZN), Zambia (ZMW) |
| **Europe** | France (EUR), Belgium (EUR), United Kingdom (GBP) |
| **America** | United States (USD), Canada (CAD) |
| **Indian Ocean** | Madagascar (MGA), Mauritius (MUR), Seychelles (SCR) |

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── config/
│   │   └── settings.py
│   ├── data/
│   │   ├── countries.py         # 54+ countries and currencies
│   │   └── __init__.py
│   ├── models/
│   │   ├── admin.py            # Admin and AdminConfig models
│   │   └── transaction.py      # Transaction model
│   ├── routes/
│   │   ├── main.py            # Public routes
│   │   ├── admin.py           # Admin routes
│   │   └── superadmin.py      # TransfertSpace routes
│   ├── utils/
│   │   ├── calculations.py    # Calculations with 10 tiers
│   │   └── security.py        # Password hashing
│   └── database.py            # PostgreSQL configuration
├── templates/
│   ├── welcome.html           # Homepage with registration
│   ├── index.html             # Client transfer interface
│   ├── admin_login.html       # Admin login
│   ├── admin_panel.html       # Admin panel (10 tiers)
│   ├── superadmin_*.html      # TransfertSpace interfaces
│   └── ...
├── static/
│   ├── background.jpg
│   └── bg-transfer.jpg
├── main.py                    # Entry point
├── requirements.txt
└── pyproject.toml
```

## PostgreSQL Database

The application uses PostgreSQL with 3 main tables:

- **admins**: Admin and TransfertSpace accounts
- **admin_configs**: Personalized configurations by admin
- **transactions**: History of all transactions

## Deployment

### Environment Variables

```bash
DATABASE_URL=postgresql://...
SESSION_SECRET=your_secret_key
```

### Server Deployment

1. Configure PostgreSQL
2. Install dependencies: `pip install -r requirements.txt`
3. Launch with Gunicorn: `gunicorn --bind=0.0.0.0:5000 --workers 4 main:app`
4. Configure a reverse proxy (Nginx/Apache) if necessary

## Security

⚠️ **Important for production**:
- **Change IMMEDIATELY** the default TransfertSpace password
- Use HTTPS for all communications
- Configure `SESSION_SECRET` with a secure random value
- Limit login attempts
- Perform regular database backups

## New Features (October 2025)

✨ **Latest improvements**:
- 🎨 Enhanced action buttons (Edit, Delete, Transactions)
- 🔄 Enhanced admin status toggle with feedback
- 🌍 Complete list of 54+ countries with dynamic currencies
- 📊 Extension to 10 transaction fee tiers
- 🔢 Automatic inverse exchange rate calculation
- 📝 Registration request form via WhatsApp
- 🏷️ Rebranding: SuperAdmin → TransfertSpace
- 💎 Enhanced UI/UX with modern design and better explanations

## Support

For any questions or issues:
- **Email**: moa@myoneart.com
- **WhatsApp**: +212699140001
- **Website**: [www.myoneart.com](https://www.myoneart.com)

---

**TransfertSpace**  
By **[MOA Digital Agency LLC](https://www.myoneart.com)**  
Developed by: **Aisance KALONJI**  
Easy, Beneficial & Fast Money Transfer
