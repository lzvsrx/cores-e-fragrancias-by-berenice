
#!/usr/bin/env bash
# backup_zip_encrypt.sh
# Creates a timestamped ZIP of backups/ and app.db then optionally encrypts with openssl (AES-256-CBC).
set -e
OUTDIR=backups
TS=$(date -u +"%Y%m%d%H%M%S")
ZIPNAME="backup_${TS}.zip"
zip -r "${OUTDIR}/${ZIPNAME}" backups app.db || true
echo "Created ${OUTDIR}/${ZIPNAME}"
if [ -n "$1" ]; then
  PASS="$1"
  openssl enc -aes-256-cbc -salt -in "${OUTDIR}/${ZIPNAME}" -out "${OUTDIR}/${ZIPNAME}.enc" -k "${PASS}"
  echo "Encrypted to ${OUTDIR}/${ZIPNAME}.enc"
fi
