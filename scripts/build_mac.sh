
#!/usr/bin/env bash
# macOS build: PyInstaller + electron-builder (DMG)
set -e
echo "[1] Installing Python deps"
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt pyinstaller

echo "[2] Building Python binary (mac)"
pyinstaller --noconfirm --onefile --add-data "uploads:uploads" --add-data "backups:backups" app.py

echo "[3] Copying binary to electron/python-dist"
mkdir -p electron/python-dist
cp dist/app electron/python-dist/app

echo "[4] Installing npm deps and building"
cd electron
npm ci
npx electron-builder --mac dmg --publish never
