#!/usr/bin/env bash
# Build script: PyInstaller + Electron + electron-builder
set -e

echo "[1/4] Criando binário Python com PyInstaller..."
pip install pyinstaller
pyinstaller --noconfirm --onefile --add-data "uploads:uploads" --add-data "backups:backups" app.py

echo "[2/4] Movendo binário para pasta electron..."
mkdir -p electron/python-dist
cp dist/app electron/python-dist/

echo "[3/4] Instalando dependências do Electron..."
cd electron
npm install

echo "[4/4] Empacotando com electron-builder..."
npx electron-builder --${1:-dir}  # passe 'dist' para criar instalador

# Optional: upload backups to Google Drive
if [ "$2" = "--upload-backups" ]; then
  echo "Uploading backups to Google Drive..."
  # usage: ./build_full.sh dist --upload-backups /path/to/creds.json DRIVE_FOLDER_ID
  CREDS="$3"
  FOLDER_ID="$4"
  if [ -z "$CREDS" ] || [ -z "$FOLDER_ID" ]; then
    echo "Provide creds JSON path and DRIVE_FOLDER_ID"
  else
    python3 scripts/upload_backups_to_gdrive.py --creds "$CREDS" --folder-id "$FOLDER_ID"
  fi
fi
