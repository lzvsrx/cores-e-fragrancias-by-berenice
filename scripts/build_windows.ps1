
# PowerShell build script for Windows: PyInstaller + electron-builder
param(
    [string]$buildType = "nsis" # or 'dir' for unpacked
)
Write-Host "[1] Installing Python dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

Write-Host "[2] Building Python binary with PyInstaller..."
pyinstaller --noconfirm --onefile --add-data "uploads;uploads" --add-data "backups;backups" app.py

Write-Host "[3] Copying binary to electron/python-dist..."
New-Item -ItemType Directory -Force -Path .\electron\python-dist | Out-Null
Copy-Item -Path .\dist\app.exe -Destination .\electron\python-dist\ -Force

Write-Host "[4] Installing npm deps..."
Push-Location electron
npm ci
Write-Host "[5] Building Electron app..."
if ($buildType -eq "nsis") {
    npx electron-builder --win nsis --publish never
} else {
    npx electron-builder --dir
}
Pop-Location
Write-Host "Build finished. Check electron\\dist for artifacts."
