#!/bin/bash
# Doppelklick zum Starten

# NVM laden
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Node 20 verwenden (für node-pty Kompatibilität)
nvm use 20 2>/dev/null || true

# Fallback: Direkt auf nvm Node 20 zeigen
export PATH="$HOME/.nvm/versions/node/v20.19.5/bin:$PATH"

# Ins Projektverzeichnis wechseln
cd "$(dirname "$0")"

echo "================================"
echo "   Evolving Dashboard Starter   "
echo "================================"
echo ""

# Zeige Node Version
echo "Node: $(node --version 2>/dev/null || echo 'nicht gefunden')"
echo ""

# Prüfe ob npm vorhanden
if ! command -v npm &> /dev/null; then
    echo "FEHLER: npm nicht gefunden!"
    echo ""
    read -p "Drücke Enter zum Schließen..."
    exit 1
fi

# Prüfe ob bereits läuft
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "Dashboard läuft bereits!"
    open http://localhost:3000
    sleep 2
    exit 0
fi

# Starte Server
echo "Starte Evolving Dashboard..."
echo ""
mkdir -p logs

# Server im Hintergrund starten
nohup npm run dev > logs/server.log 2>&1 &
SERVER_PID=$!

echo "Server-Prozess gestartet (PID: $SERVER_PID)"
echo "Warte auf Server..."
echo ""

# Warte bis Server bereit (max 30 Sekunden)
for i in {1..30}; do
    sleep 1
    if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
        echo ""
        echo "Dashboard gestartet!"
        echo "URL: http://localhost:3000"
        open http://localhost:3000
        sleep 2
        exit 0
    fi
    printf "."
done

echo ""
echo ""
echo "Server braucht länger als erwartet."
echo "Prüfe logs/server.log für Details."
echo ""
echo "Versuche trotzdem Browser zu öffnen..."
open http://localhost:3000

read -p "Drücke Enter zum Schließen..."
