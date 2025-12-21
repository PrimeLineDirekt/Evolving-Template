#!/bin/bash
# Doppelklick zum Stoppen

echo "Stoppe Evolving Dashboard..."

pkill -f "tsx server.ts" 2>/dev/null
pkill -f "next-server" 2>/dev/null

sleep 1

echo "Dashboard gestoppt."
sleep 2
