#!/bin/bash

# Script de mise à jour du VPS après un git pull
# Usage: bash update_vps.sh

# Arrêt en cas d'erreur
set -euo pipefail

echo "🔄 Début de la mise à jour..."

# Vérifier que les outils nécessaires sont installés
command -v pip >/dev/null 2>&1 || { echo "❌ Erreur: pip n'est pas installé"; exit 1; }
command -v pm2 >/dev/null 2>&1 || { echo "❌ Erreur: pm2 n'est pas installé"; exit 1; }

# 1. Activer l'environnement virtuel si nécessaire
if [ -d "venv" ]; then
    echo "✓ Activation de l'environnement virtuel..."
    source venv/bin/activate
else
    echo "⚠️  Avertissement: Pas d'environnement virtuel trouvé"
fi

# 2. Installer/Mettre à jour les dépendances
echo "📦 Installation des dépendances..."
if pip install -r requirements.txt --upgrade; then
    echo "✓ Dépendances installées avec succès"
else
    echo "❌ Erreur lors de l'installation des dépendances"
    exit 1
fi

# 3. Appliquer les migrations si nécessaire
echo "🗄️  Vérification et application des migrations..."
if [ -f "migrate_add_suspension_fields.py" ]; then
    if python migrate_add_suspension_fields.py; then
        echo "✓ Migrations appliquées avec succès"
    else
        echo "⚠️  Avertissement: Erreur lors de la migration (peut-être déjà appliquée)"
    fi
else
    echo "ℹ️  Aucun script de migration trouvé"
fi

# 4. Redémarrer l'application avec PM2
echo "🔄 Redémarrage de l'application..."
if pm2 restart MoneyTransfertSaas; then
    echo "✓ Application redémarrée avec succès"
else
    echo "❌ Erreur lors du redémarrage de l'application"
    exit 1
fi

echo ""
echo "✅ Mise à jour terminée avec succès!"
echo ""
echo "📊 Status de l'application:"
pm2 status MoneyTransfertSaas
echo ""
echo "💡 Pour voir les logs: pm2 logs MoneyTransfertSaas"
