#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Script de aprovisionamiento para AWS EC2 (Amazon Linux 2 / Ubuntu)
# ═══════════════════════════════════════════════════════════════

set -e

# 1. Update system packages
if [ -x "$(command -v apt-get)" ]; then
    echo "Ubuntu detected..."
    sudo apt-get update -y
    sudo apt-get install -y docker.io docker-compose git
elif [ -x "$(command -v yum)" ]; then
    echo "Amazon Linux detected..."
    sudo yum update -y
    sudo amazon-linux-extras install docker -y
    sudo yum install git -y
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
else
    echo "Unsupported OS"
    exit 1
fi

# 2. Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $(whoami)

# 3. Clone Repository (Update URL if private)
REPO_URL="https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods.git"
APP_DIR="/home/$(whoami)/numcalc"

if [ -d "$APP_DIR" ]; then
    echo "Directory exists. Pulling latest changes..."
    cd $APP_DIR
    git pull origin main
else
    echo "Cloning repository..."
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR
fi

# 4. Build and deploy
echo "Building and starting containers..."
sudo docker-compose down || true
sudo docker-compose up -d --build

echo "Deployment complete! App is running on port 5000."
