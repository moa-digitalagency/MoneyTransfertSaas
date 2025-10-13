import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    """Charge la configuration depuis le fichier JSON"""
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'countries': {
                'country1': {'code': 'RDC', 'currency_code': 'USD'},
                'country2': {'code': 'MA', 'currency_code': 'MAD'}
            },
            'rates': {
                'country1_to_country2': 10.0,
                'country2_to_country1': 0.1
            },
            'transaction_fees': {
                'country1_to_country2': [],
                'country2_to_country1': []
            },
            'whatsapp': {
                'country1_to_country2': {'phone': '', 'contact_name': ''},
                'country2_to_country1': {'phone': '', 'contact_name': ''}
            }
        }
    except json.JSONDecodeError:
        raise ValueError(f"Le fichier {CONFIG_FILE} contient du JSON invalide")

def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
