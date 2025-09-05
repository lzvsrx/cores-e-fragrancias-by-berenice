
Cores e Fragrâncias - Desktop package
-------------------------------------

Conteúdo:
- app.py (Streamlit improved UI)
- electron/ (main.js, package.json) - template to wrap the Streamlit app
- scripts/daily_backup.py - script to run as cron or systemd oneshot
- tests/ - pytest tests for basic DB functionality
- backups/, uploads/ - runtime folders for backups and images

How to build the Electron desktop app (quick):
1) Install Node.js and npm.
2) In the 'electron' folder run: npm install
3) Start the Streamlit app: python -m streamlit run app.py
4) In 'electron' run: npm start  (this will open the Electron window pointing to localhost:8501)

How to setup backup cron (example):
- open crontab: crontab -e
- add line (adjust path): 0 2 * * * /usr/bin/python3 /path/to/cores_fragrancias/scripts/daily_backup.py >> /var/log/cores_backup.log 2>&1

How to run tests:
- From project root: pytest -q

Notes:
- Electron template currently starts Streamlit separately; packaging into a single binary requires additional steps (pkg, electron-builder, or using tools like PyInstaller for python part).
- The barcode and QR generation require 'python-barcode' and 'qrcode' packages (in requirements.txt).


### Extra Features Added:
- Polling para aguardar Streamlit antes de abrir a janela Electron.
- electron-builder config (electron-builder.json) para gerar instaladores multiplataforma.
- Workflow GitHub Actions (.github/workflows/build.yml) para build automático (Windows, Mac, Linux).


## Electron build and CI

- `electron/main.js` now polls the Streamlit server until it's ready before opening the window.
- `electron/package.json` includes `pack` and `dist` scripts using `electron-builder`.
- GitHub Actions workflow at `.github/workflows/build-desktop.yml` builds a Linux AppImage and uploads it as an artifact.

Make sure to add appropriate icons to `assets/` before building (icon.png, icon.icns, icon.ico).


## Empacotamento com PyInstaller + Electron
Para gerar um binário e empacotar com Electron:
```bash
./build_full.sh dist
```
Isso irá:
1. Usar PyInstaller para empacotar `app.py` como binário único.
2. Copiar o binário para a pasta `electron/python-dist/`.
3. Executar `electron-builder` para gerar instaladores para seu sistema.

## Publicação no GitHub
Para criar e enviar o repositório:
```bash
./init_repo.sh cores-fragrancias
```
Depois siga as instruções exibidas no terminal para adicionar o remote e fazer o push.

## Ícones
Substitua os arquivos em `assets/`:
- icon.png (Linux)
- icon.ico (Windows)
- icon.icns (Mac)


## Integração Electron pronta
- `electron/main.js` executa o binário empacotado (se presente em `electron/python-dist/`) ou usa `streamlit run app.py` em modo dev.
- `electron/package.json` já tem configurações para `electron-builder` (insira ícones reais em `assets/`).

## UI Refinada
- `app.py` atualizado com layout de cards responsivos, previews maiores e modal-like expanders.

## Testes & CI
- `tests/` contém testes `pytest`.
- `.github/workflows/ci-tests.yml` executa os testes automaticamente no push / PR.



## Ícones substituídos
Coloquei ícones PNG/ICO/ICNS em `assets/` (substitua se quiser por versões oficiais).

## Workflow Multi-OS
Adicionado `.github/workflows/build-multi-os.yml` para gerar builds para Linux, Windows e macOS.

## Upload automático de backups para Google Drive
Script: `scripts/upload_backups_to_gdrive.py`
Exemplo de uso (após criar Service Account JSON and Drive Folder):
```bash
# cria backup (por exemplo via build script ou manual)
python3 scripts/daily_backup.py
# enviar backups mais recentes
python3 scripts/upload_backups_to_gdrive.py --creds /path/to/sa.json --folder-id your_drive_folder_id
```
Você também pode executar via build script:
```bash
./build_full.sh dist --upload-backups /path/to/sa.json your_drive_folder_id
```

