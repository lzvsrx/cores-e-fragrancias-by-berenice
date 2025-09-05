
#!/usr/bin/env python3
"""Upload backups from backups/ to Google Drive using a Service Account JSON.

Usage:
  python upload_backups_to_gdrive.py --creds /path/to/service_account.json --folder-id DRIVE_FOLDER_ID

Notes:
- The service account must have access to the Drive (share the folder with the service account email)
- Requires google-api-python-client and google-auth-httplib2/google-auth libraries
  pip install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib
"""

import argparse, os, sys, glob, mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def get_args():
    p = argparse.ArgumentParser()
    p.add_argument('--creds', required=True, help='Service account JSON path')
    p.add_argument('--folder-id', required=True, help='Drive folder id to upload files to')
    return p.parse_args()

def main():
    args = get_args()
    BASE = os.path.dirname(os.path.dirname(__file__))
    BACKUP_DIR = os.path.join(BASE, 'backups')
    if not os.path.exists(BACKUP_DIR):
        print('No backups directory found at', BACKUP_DIR); sys.exit(1)
    creds = service_account.Credentials.from_service_account_file(args.creds, scopes=['https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)
    files = sorted(glob.glob(os.path.join(BACKUP_DIR, '*')), key=os.path.getmtime)
    for fpath in files:
        name = os.path.basename(fpath)
        media = MediaFileUpload(fpath, mimetype=mimetypes.guess_type(fpath)[0] or 'application/octet-stream', resumable=True)
        file_metadata = {'name': name, 'parents': [args.folder_id]}
        print('Uploading', name)
        created = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('Uploaded with id', created.get('id'))

if __name__ == '__main__':
    main()
