#!/bin/bash
# Runs on the EC2 server during deployment.
# Called by GitHub Actions over SSH.
set -e

APP_DIR="/home/ubuntu/app"
REPO_URL="${REPO_URL}"  # injected by GitHub Actions

echo "==> Ensuring app directory exists"
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# First deploy: clone. Subsequent deploys: pull.
if [ ! -d ".git" ]; then
  echo "==> Cloning repository"
  git clone "$REPO_URL" .
else
  echo "==> Pulling latest changes"
  git pull origin main
fi

echo "==> Writing .env file"
# .env content is injected as an env var by GitHub Actions
echo "$ENV_FILE_CONTENT" > .env

echo "==> Copying production compose + nginx config"
# These are already in the repo at the paths below
# (docker-compose.prod.yml and nginx/nginx.conf)

echo "==> Pulling/building images and restarting services"
docker compose -f docker-compose.prod.yml pull --ignore-pull-failures || true
docker compose -f docker-compose.prod.yml up --build -d --remove-orphans

echo "==> Cleaning up unused Docker resources"
docker system prune -f

echo "==> Done. Services running:"
docker compose -f docker-compose.prod.yml ps

