#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# deploy.sh — Automated deployment for Ubuntu Lightsail
# ═══════════════════════════════════════════════════════════════
# Usage (on the Lightsail instance):
#   chmod +x scripts/deploy.sh
#   ./scripts/deploy.sh <GITHUB_REPO_URL>
#
# Example:
#   ./scripts/deploy.sh https://github.com/username/calculadora.git
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

# ── Colors ────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log()   { echo -e "${GREEN}[✔]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✘]${NC} $1"; exit 1; }
info()  { echo -e "${CYAN}[→]${NC} $1"; }

# ── Variables ─────────────────────────────────────────────────
REPO_URL="${1:-}"
APP_DIR="/opt/numcalc"
COMPOSE_FILE="docker-compose.yml"

if [ -z "$REPO_URL" ]; then
    error "Usage: $0 <GITHUB_REPO_URL>"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${CYAN}   Numerical Methods Calculator — Deploy Script    ${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""

# ══════════════════════════════════════════════════════════════
# STEP 1: System updates
# ══════════════════════════════════════════════════════════════
info "Step 1/6: Updating system packages..."
sudo apt-get update -qq
sudo apt-get upgrade -y -qq
log "System updated"

# ══════════════════════════════════════════════════════════════
# STEP 2: Install Docker if not present
# ══════════════════════════════════════════════════════════════
info "Step 2/6: Checking Docker installation..."

if ! command -v docker &> /dev/null; then
    warn "Docker not found. Installing..."
    
    # Install prerequisites
    sudo apt-get install -y -qq \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Add Docker GPG key
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
        sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Add Docker repo
    echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/ubuntu \
        $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin

    # Allow current user to run docker without sudo
    sudo usermod -aG docker "$USER"
    
    log "Docker installed successfully"
    warn "NOTE: You may need to log out and back in for docker group to take effect."
    warn "If 'docker compose' fails, run: newgrp docker"
else
    log "Docker already installed: $(docker --version)"
fi

# Verify Docker Compose
if ! docker compose version &> /dev/null; then
    error "Docker Compose plugin not found. Install it with: sudo apt-get install docker-compose-plugin"
fi
log "Docker Compose: $(docker compose version --short)"

# ══════════════════════════════════════════════════════════════
# STEP 3: Clone or update repository
# ══════════════════════════════════════════════════════════════
info "Step 3/6: Setting up application code..."

if [ -d "$APP_DIR/.git" ]; then
    warn "Repository exists. Pulling latest changes..."
    cd "$APP_DIR"
    git fetch origin
    git reset --hard origin/main || git reset --hard origin/master
    log "Repository updated"
else
    warn "Cloning repository for the first time..."
    sudo mkdir -p "$APP_DIR"
    sudo chown "$USER:$USER" "$APP_DIR"
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
    log "Repository cloned to $APP_DIR"
fi

# ══════════════════════════════════════════════════════════════
# STEP 4: Configure environment
# ══════════════════════════════════════════════════════════════
info "Step 4/6: Configuring environment..."

if [ ! -f "$APP_DIR/.env" ]; then
    cp "$APP_DIR/.env.example" "$APP_DIR/.env"
    
    # Generate a secure random SECRET_KEY
    SECRET=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || \
             openssl rand -hex 32)
    
    sed -i "s/CHANGE-ME-generate-with-python-c-import-secrets-secrets-token-hex-32/$SECRET/" "$APP_DIR/.env"
    
    log "Environment file created with secure SECRET_KEY"
    warn "Review .env file: nano $APP_DIR/.env"
else
    log "Environment file already exists (preserved)"
fi

# ══════════════════════════════════════════════════════════════
# STEP 5: Build and start containers
# ══════════════════════════════════════════════════════════════
info "Step 5/6: Building and starting containers..."

cd "$APP_DIR"

# Stop existing containers if running
docker compose down --remove-orphans 2>/dev/null || true

# Build and start
docker compose up --build -d

log "Containers started"

# ══════════════════════════════════════════════════════════════
# STEP 6: Verify deployment
# ══════════════════════════════════════════════════════════════
info "Step 6/6: Verifying deployment..."

# Wait for healthcheck
echo -n "  Waiting for app to be healthy "
MAX_WAIT=60
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if docker compose ps app 2>/dev/null | grep -q "healthy"; then
        break
    fi
    echo -n "."
    sleep 3
    WAITED=$((WAITED + 3))
done
echo ""

if [ $WAITED -ge $MAX_WAIT ]; then
    warn "App did not become healthy in ${MAX_WAIT}s. Checking logs..."
    docker compose logs --tail=30 app
    echo ""
    warn "Nginx logs:"
    docker compose logs --tail=10 nginx
    error "Deployment may have issues. Check logs above."
fi

log "App is healthy!"

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com 2>/dev/null || \
            curl -s http://ifconfig.me 2>/dev/null || \
            echo "YOUR_SERVER_IP")

# ── Summary ──────────────────────────────────────────────────
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}   ✅ DEPLOYMENT SUCCESSFUL!                       ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${CYAN}App URL:${NC}        http://${PUBLIC_IP}"
echo -e "  ${CYAN}Health Check:${NC}   http://${PUBLIC_IP}/api/health"
echo -e "  ${CYAN}API Methods:${NC}    http://${PUBLIC_IP}/api/methods"
echo -e "  ${CYAN}App Directory:${NC}  ${APP_DIR}"
echo ""
echo -e "  ${YELLOW}Useful commands:${NC}"
echo -e "    docker compose logs -f          # Follow logs"
echo -e "    docker compose ps               # Container status"
echo -e "    docker compose restart           # Restart services"
echo -e "    docker compose down              # Stop everything"
echo -e "    docker compose up --build -d     # Rebuild & restart"
echo ""
