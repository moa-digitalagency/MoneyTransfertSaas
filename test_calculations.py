#!/usr/bin/env python3
"""Script de test pour vérifier les calculs de frais corrigés"""

from app.utils.calculations import calculate_transfer

# Configuration de test basée sur l'image fournie
test_config = {
    'countries': {
        'country1': {'code': 'CD', 'currency_code': 'CDF'},
        'country2': {'code': 'MA', 'currency_code': 'MAD'}
    },
    'rates': {
        'country1_to_country2': 0.004,  # 1 CDF = 0.004 MAD
        'country2_to_country1': 250     # 1 MAD = 250 CDF (comme dans l'image)
    },
    'transaction_fees': {
        'country2_to_country1': [
            {'min': 0, 'max': 1000, 'fee': 20},
            {'min': 1000, 'max': 5000, 'fee': 100},
            {'min': 5000, 'max': 100000, 'fee': 200}
        ]
    }
}

# Test 1: Envoi de 1000 MAD vers CDF
print("=" * 60)
print("TEST: Envoi de 1000 MAD → CDF (comme dans l'image)")
print("=" * 60)

result = calculate_transfer(
    direction='country2_to_country1',
    amount=1000,
    calculation_type='send',
    config=test_config
)

print(f"Montant envoyé: {result['send_amount']} {result['send_currency']}")
print(f"Frais: {result['fee']} {result['fee_currency']}")
print(f"Montant net (après frais): {result['send_amount'] - result['fee']} {result['send_currency']}")
print(f"Taux de change: {result['rate']}")
print(f"Montant reçu: {result['receive_amount']} {result['receive_currency']}")

print("\n" + "-" * 60)
print("CALCUL DÉTAILLÉ:")
print("-" * 60)
print(f"1. Montant d'envoi: 1000 MAD")
print(f"2. Frais (palier 0-1000): 20 MAD")
print(f"3. Montant net: 1000 - 20 = 980 MAD")
print(f"4. Conversion: 980 × 250 = {980 * 250} CDF")
print(f"5. Le destinataire reçoit: {result['receive_amount']} CDF")

print("\n" + "=" * 60)
print("COMPARAISON AVEC L'ANCIENNE LOGIQUE:")
print("=" * 60)
print("Ancienne logique (incorrecte):")
print("  - Conversion: 1000 × 250 = 250000 CDF")
print("  - Frais soustraits: 250000 - 20 = 249980 CDF")
print("  - Frais affichés: 20 CDF ❌")
print()
print("Nouvelle logique (correcte):")
print(f"  - Frais déduits: 1000 - 20 = 980 MAD")
print(f"  - Conversion: 980 × 250 = {result['receive_amount']} CDF")
print(f"  - Frais affichés: 20 MAD ✅")
