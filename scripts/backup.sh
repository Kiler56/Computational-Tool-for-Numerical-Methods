#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# backup.sh — Backup SQLite database from Docker volume
# ═══════════════════════════════════════════════════════════════
# Usage:
#   chmod +x scripts/backup.sh
#   ./scripts/backup.sh
#
# Cron (daily at 2 AM):
#   0 2 * * * /opt/numcalc/scripts/backup.sh >> /var/log/numcalc-backup.log 2>&1
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

# ── Configuration ─────────────────────────────────────────────
APP_DIR="/opt/numcalc"
BACKUP_DIR="/opt/numcalc/backups"
VOLUME_NAME="numcalc-app-data"
MAX_BACKUPS=7               # Keep last N backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# ── Colors ────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${GREEN}[✔]${NC} $1"; }
warn()  { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${YELLOW}[!]${NC} $1"; }
error() { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] ${RED}[✘]${NC} $1"; exit 1; }

# ── Create backup directory ───────────────────────────────────
mkdir -p "$BACKUP_DIR"

# ── Backup ────────────────────────────────────────────────────
BACKUP_FILE="$BACKUP_DIR/numcalc_db_${TIMESTAMP}.tar.gz"

log "Starting backup..."

# Copy SQLite file from Docker volume using a temporary container
docker run --rm \
    -v "${VOLUME_NAME}:/data:ro" \
    -v "${BACKUP_DIR}:/backup" \
    alpine:3.19 \
    tar czf "/backup/numcalc_db_${TIMESTAMP}.tar.gz" -C /data .

if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "Backup created: $BACKUP_FILE ($SIZE)"
else
    error "Backup file was not created!"
fi

# ── Cleanup old backups ──────────────────────────────────────
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "numcalc_db_*.tar.gz" -type f | wc -l)

if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
    REMOVE_COUNT=$((BACKUP_COUNT - MAX_BACKUPS))
    warn "Removing $REMOVE_COUNT old backup(s) (keeping last $MAX_BACKUPS)..."
    
    find "$BACKUP_DIR" -name "numcalc_db_*.tar.gz" -type f -printf '%T+ %p\n' | \
        sort | head -n "$REMOVE_COUNT" | awk '{print $2}' | \
        xargs rm -f
    
    log "Old backups cleaned up"
fi

# ── Summary ──────────────────────────────────────────────────
log "Backup complete. Total backups: $(find "$BACKUP_DIR" -name "numcalc_db_*.tar.gz" -type f | wc -l)"
