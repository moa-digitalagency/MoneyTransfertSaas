import json
import os
from flask import session

def load_translations(lang='fr'):
    """Load translations from JSON file"""
    file_path = os.path.join('translations', f'{lang}.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        with open('translations/fr.json', 'r', encoding='utf-8') as f:
            return json.load(f)

def get_locale():
    """Get current locale from session or default to French"""
    return session.get('lang', 'fr')

def get_translations():
    """Get translations for current language"""
    lang = get_locale()
    return load_translations(lang)

def set_locale(lang):
    """Set locale in session"""
    if lang in ['fr', 'en']:
        session['lang'] = lang
        return True
    return False

def translate(key, lang=None):
    """Translate a key using dot notation (e.g., 'database.page_title')"""
    if lang is None:
        lang = get_locale()
    translations = load_translations(lang)
    
    keys = key.split('.')
    value = translations
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return key
    return value

def init_i18n(app):
    """Initialize i18n support for Flask app"""
    
    @app.context_processor
    def inject_translations():
        lang = get_locale()
        translations = load_translations(lang)
        return {
            't': translations,
            '_': translate,
            'current_lang': lang
        }
    
    @app.route('/change-language/<lang>')
    def change_language(lang):
        from flask import redirect, request
        if set_locale(lang):
            referrer = request.referrer or '/'
            return redirect(referrer)
        return redirect('/')
