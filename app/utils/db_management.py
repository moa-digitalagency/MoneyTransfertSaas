import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
        self.github_repo = "https://github.com/moa-digitalagency/MoneyTransfertSaas.git"
        
    def create_backup(self):
        """Crée un backup de la base de données PostgreSQL"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = self.backup_dir / f'db_backup_{timestamp}.sql'
            
            db_url = os.environ.get('DATABASE_URL')
            if not db_url:
                return {'success': False, 'error': 'DATABASE_URL non trouvé'}
            
            pg_user = os.environ.get('PGUSER', 'postgres')
            pg_password = os.environ.get('PGPASSWORD', 'password')
            pg_host = os.environ.get('PGHOST', 'helium')
            pg_database = os.environ.get('PGDATABASE', 'heliumdb')
            pg_port = os.environ.get('PGPORT', '5432')
            
            env = os.environ.copy()
            env['PGPASSWORD'] = pg_password
            
            cmd = [
                'pg_dump',
                '-h', pg_host,
                '-p', pg_port,
                '-U', pg_user,
                '-d', pg_database,
                '-F', 'p',
                '-f', str(backup_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                backup_size = backup_file.stat().st_size
                return {
                    'success': True,
                    'file': str(backup_file),
                    'size': backup_size,
                    'timestamp': timestamp
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr or 'Erreur lors du backup'
                }
        except Exception as e:
            logger.error(f"Erreur backup: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def list_backups(self):
        """Liste tous les backups disponibles"""
        try:
            backups = []
            for backup_file in sorted(self.backup_dir.glob('db_backup_*.sql'), reverse=True):
                stat = backup_file.stat()
                backups.append({
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
            return {'success': True, 'backups': backups}
        except Exception as e:
            logger.error(f"Erreur liste backups: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def restore_backup(self, backup_filename):
        """Restaure un backup de la base de données"""
        try:
            backup_file = self.backup_dir / backup_filename
            if not backup_file.exists():
                return {'success': False, 'error': 'Fichier de backup non trouvé'}
            
            pg_user = os.environ.get('PGUSER', 'postgres')
            pg_password = os.environ.get('PGPASSWORD', 'password')
            pg_host = os.environ.get('PGHOST', 'helium')
            pg_database = os.environ.get('PGDATABASE', 'heliumdb')
            pg_port = os.environ.get('PGPORT', '5432')
            
            env = os.environ.copy()
            env['PGPASSWORD'] = pg_password
            
            cmd = [
                'psql',
                '-h', pg_host,
                '-p', pg_port,
                '-U', pg_user,
                '-d', pg_database,
                '-f', str(backup_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {'success': True, 'message': 'Backup restauré avec succès'}
            else:
                return {'success': False, 'error': result.stderr or 'Erreur lors de la restauration'}
        except Exception as e:
            logger.error(f"Erreur restauration: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def check_git_status(self):
        """Vérifie le statut du dépôt Git"""
        try:
            if not Path('.git').exists():
                return {'success': False, 'error': 'Pas un dépôt Git'}
            
            # Get current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True)
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
            # Get current commit
            commit_result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                                         capture_output=True, text=True)
            current_commit = commit_result.stdout.strip() if commit_result.returncode == 0 else 'unknown'
            
            # Check for updates
            subprocess.run(['git', 'fetch', 'origin'], capture_output=True)
            status_result = subprocess.run(['git', 'status', '-uno'], 
                                         capture_output=True, text=True)
            
            has_updates = 'Your branch is behind' in status_result.stdout
            
            return {
                'success': True,
                'branch': current_branch,
                'commit': current_commit,
                'has_updates': has_updates,
                'status': status_result.stdout
            }
        except Exception as e:
            logger.error(f"Erreur git status: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def pull_from_github(self):
        """Pull les dernières mises à jour depuis GitHub"""
        try:
            # Create backup before pull
            backup_result = self.create_backup()
            if not backup_result['success']:
                return {'success': False, 'error': f"Échec du backup: {backup_result.get('error')}"}
            
            # Pull from GitHub
            pull_result = subprocess.run(['git', 'pull', 'origin'], 
                                        capture_output=True, text=True)
            
            if pull_result.returncode == 0:
                return {
                    'success': True,
                    'message': 'Mise à jour effectuée avec succès',
                    'backup': backup_result,
                    'output': pull_result.stdout
                }
            else:
                return {
                    'success': False,
                    'error': pull_result.stderr or 'Erreur lors du pull',
                    'backup': backup_result
                }
        except Exception as e:
            logger.error(f"Erreur pull GitHub: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def run_migrations(self):
        """Exécute les migrations de base de données"""
        try:
            # Check for migration files
            migration_files = list(Path('.').glob('migrate_*.py'))
            
            if not migration_files:
                return {'success': True, 'message': 'Aucune migration à exécuter'}
            
            results = []
            for migration_file in sorted(migration_files):
                result = subprocess.run(['python', str(migration_file)], 
                                      capture_output=True, text=True)
                results.append({
                    'file': migration_file.name,
                    'success': result.returncode == 0,
                    'output': result.stdout if result.returncode == 0 else result.stderr
                })
            
            all_success = all(r['success'] for r in results)
            return {
                'success': all_success,
                'migrations': results,
                'message': 'Migrations exécutées' if all_success else 'Certaines migrations ont échoué'
            }
        except Exception as e:
            logger.error(f"Erreur migrations: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def update_with_migrations(self):
        """Met à jour le code et exécute les migrations avec backup automatique"""
        try:
            # 1. Create backup
            backup_result = self.create_backup()
            if not backup_result['success']:
                return {
                    'success': False,
                    'error': f"Échec du backup: {backup_result.get('error')}",
                    'step': 'backup'
                }
            
            # 2. Pull from GitHub
            pull_result = self.pull_from_github()
            if not pull_result['success']:
                return {
                    'success': False,
                    'error': pull_result.get('error'),
                    'backup': backup_result,
                    'step': 'pull'
                }
            
            # 3. Run migrations
            migration_result = self.run_migrations()
            
            return {
                'success': migration_result['success'],
                'backup': backup_result,
                'pull': pull_result,
                'migrations': migration_result,
                'message': 'Mise à jour complète effectuée avec succès' if migration_result['success'] else 'Mise à jour terminée avec des erreurs'
            }
        except Exception as e:
            logger.error(f"Erreur update_with_migrations: {str(e)}")
            return {'success': False, 'error': str(e)}
