
#!/usr/bin/env python3
# Simple backup script: copies app.db to backups with timestamp and optionally uploads to Google Drive (not implemented here)
import shutil, os, datetime, sys
BASE = os.path.dirname(os.path.dirname(__file__))
DB = os.path.join(BASE, 'app.db')
BACKUP_DIR = os.path.join(BASE, 'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)
if not os.path.exists(DB):
    print('Database not found:', DB)
    sys.exit(1)
ts = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
dst = os.path.join(BACKUP_DIR, f'app_backup_{ts}.db')
shutil.copy2(DB, dst)
print('Backup created at', dst)
