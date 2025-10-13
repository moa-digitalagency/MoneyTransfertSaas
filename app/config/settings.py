import json
import os

CONFIG_FILE = 'config.json'

def load_config():
    """Charge la configuration depuis le fichier JSON"""
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    """Sauvegarde la configuration dans le fichier JSON"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
