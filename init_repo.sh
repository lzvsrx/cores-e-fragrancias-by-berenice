#!/usr/bin/env bash
# Script para inicializar repositório e enviar para GitHub
# Uso: ./init_repo.sh <NOME_REPO>
set -e
if [ -z "$1" ]; then
  echo "Uso: ./init_repo.sh <NOME_REPO>"
  exit 1
fi
REPO=$1
git init
git add .
git commit -m "Primeiro commit - Cores e Fragrâncias Desktop"
git branch -M main
echo "Agora crie o repositório no GitHub e execute:"
echo "git remote add origin git@github.com:SEU_USUARIO/$REPO.git"
echo "git push -u origin main"
