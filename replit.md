# Money Transfer Calculator: Dynamic Multi-Country Support

## Overview

This web-based application facilitates money transfers between any two user-configured countries. It allows administrators to dynamically select source and destination countries and their respective currencies from an extensive list. The system automatically adjusts all calculations, display elements, and messaging based on these selections. Users can calculate transfer amounts in both directions (send amount to receive amount, or desired receive amount to required send amount), choose reception methods, and initiate transfer requests via WhatsApp. The application aims to provide a flexible, user-friendly, and administratively configurable platform for international money transfers, with a strong focus on African markets.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Technology**: Vanilla JavaScript with Tailwind CSS for styling.
- **Design Pattern**: Single-page application (SPA) with dynamic DOM manipulation.
- **UI/UX Decisions**: Gradient background, card-based layout for a modern, mobile-first, and responsive interface.

### Backend Architecture
- **Framework**: Flask (Python).
- **Architecture Pattern**: Modular MVC-style structure utilizing Flask Blueprints for clear separation of concerns (main routes, admin routes).
- **Code Organization**: Core logic is distributed across `routes`, `models` (for transaction and WhatsApp messaging), `utils` (for calculations and security), `config` (for settings), and `data` (for country and currency information).
- **Country & Currency System**: A comprehensive database of 54+ countries and their currencies (including multiple currencies per country where applicable) allows for dynamic configuration via the admin panel.

### Exchange Rate & Calculation System
- **Configuration**: Exchange rates and tiered transaction fees are configurable via the admin panel and stored in `config.json`.
- **Bidirectional Calculation**: Supports two modes: calculating received amount from send amount, and calculating required send amount from desired receive amount.
- **Rounding Strategy**: All monetary amounts use ceiling rounding (`math.ceil`) to round up to the nearest cent, ensuring transparency. Iterative adjustment is used in receive-mode to handle fee tier boundaries.
- **Dynamic Adaptability**: All calculations, labels, and currency symbols automatically update based on the dynamically selected countries and currencies.

### Admin Panel
- **Access & Authentication**: Accessed via a discreet link, secured with SHA-256 hashed password authentication and CSRF protection.
- **Capabilities**: Administrators can select Country 1 and Country 2, configure their currencies, modify exchange rates and tiered transaction fees for both directions, set up dual WhatsApp contacts, update promotional content, and change the admin password.

### Security Considerations
- Admin password hashing (SHA-256).
- CSRF protection on admin forms.
- Session-based authentication for the admin panel.

## External Dependencies

### Frontend
- **Tailwind CSS**: Loaded via CDN for utility-first styling.

### Backend
- **Python Standard Library**: `urllib.parse` for URL encoding.

### Integration Services
- **WhatsApp**: Utilizes the `wa.me` API for sending pre-filled transfer requests. Features a dual contact system allowing different WhatsApp numbers and contact names for each transfer direction.

### Data Storage
- **PostgreSQL**: Used for transaction history, storing details of all WhatsApp transfer requests. This includes date/time, direction, amounts, currencies, reception method, and contact details.

### Reception Methods
- **Configurable per country**, e.g., Airtel Money and Equity Bank for RDC (USD), Cash and CIH Bank for Morocco (MAD).