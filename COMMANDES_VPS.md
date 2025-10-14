# 🚀 Commandes pour mettre à jour le VPS

## Problème rencontré
L'erreur `TypeError: replace() argument 2 must be str, not Undefined` survient après un `git pull` car le template utilise `.currency` au lieu de `.currency_code`.

Cette erreur a été **corrigée** dans le code.

## 📋 Étapes de mise à jour sur le VPS

### Option 1: Script automatique (Recommandé) ✅

```bash
# 1. Se connecter au VPS
ssh root@votre-vps

# 2. Aller dans le dossier du projet
cd /root/MoneyTransfertSaas

# 3. Faire le git pull
git pull origin main

# 4. Rendre le script exécutable (première fois seulement)
chmod +x update_vps.sh

# 5. Lancer le script de mise à jour
bash update_vps.sh
```

Le script va automatiquement:
- ✅ Activer l'environnement virtuel
- ✅ Installer/mettre à jour les dépendances
- ✅ Appliquer les migrations si nécessaire
- ✅ Redémarrer l'application PM2

---

### Option 2: Commandes manuelles

Si vous préférez exécuter les commandes une par une:

```bash
# 1. Se connecter au VPS et aller dans le dossier
cd /root/MoneyTransfertSaas

# 2. Faire le git pull
git pull origin main

# 3. Activer l'environnement virtuel
source venv/bin/activate

# 4. Mettre à jour les dépendances
pip install -r requirements.txt --upgrade

# 5. Appliquer les migrations (si nécessaire)
python migrate_add_suspension_fields.py

# 6. Redémarrer l'application
pm2 restart MoneyTransfertSaas

# 7. Vérifier le statut
pm2 status
pm2 logs MoneyTransfertSaas --lines 50
```

---

## 🔍 Vérification après mise à jour

```bash
# Voir les logs en temps réel
pm2 logs MoneyTransfertSaas

# Vérifier le statut
pm2 status

# Tester l'accès à /admin/
curl -I http://localhost:5000/admin/
```

---

## 🆘 En cas de problème persistant

Si l'erreur persiste après la mise à jour:

```bash
# 1. Arrêter complètement l'application
pm2 stop MoneyTransfertSaas
pm2 delete MoneyTransfertSaas

# 2. Nettoyer le cache Python
find . -type d -name "__pycache__" -exec rm -r {} +

# 3. Redémarrer l'application
cd /root/MoneyTransfertSaas
source venv/bin/activate
pm2 start "gunicorn --bind 0.0.0.0:5000 --workers 4 main:app" --name MoneyTransfertSaas
pm2 save
```

---

## 📝 Ce qui a été corrigé

1. **Erreur dans le template** (ligne 183 et 192 de `admin_panel.html`):
   - ❌ Avant: `config.countries.country1.currency`
   - ✅ Après: `config.countries.country1.currency_code`

2. **Amélioration des taux de change**:
   - Précision augmentée de 6 à 8 décimales
   - Ajout d'un toggle pour calcul automatique/manuel des taux inverses

3. **Script de mise à jour automatique** créé: `update_vps.sh`

---

## 💡 Note importante

Après chaque `git pull` sur le VPS, lancez toujours:
```bash
bash update_vps.sh
```

Cela garantit que:
- Les dépendances sont à jour
- Les migrations sont appliquées
- L'application est correctement redémarrée
