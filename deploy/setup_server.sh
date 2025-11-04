#!/usr/bin/env bash
# Prep script to run on a fresh Ubuntu server to install Docker and some helpers
# Run as sudo: sudo ./deploy/setup_server.sh

set -euo pipefail

echo "==> Updating apt and installing prerequisites"
apt-get update -y
apt-get install -y ca-certificates curl gnupg lsb-release apt-transport-https software-properties-common

echo "==> Installing Docker Engine"
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "==> Enabling and starting docker service"
systemctl enable --now docker

echo "==> Adding $SUDO_USER (if present) to docker group"
if [ -n "${SUDO_USER:-}" ]; then
  usermod -aG docker "$SUDO_USER" || true
fi

echo "==> Creating folder for Let's Encrypt certs (if you plan to use certbot)" 
mkdir -p /etc/letsencrypt

echo "==> Setup complete. You may need to re-login for docker group membership to apply."
echo "Then, from the project folder, run: ./deploy/up.sh"
