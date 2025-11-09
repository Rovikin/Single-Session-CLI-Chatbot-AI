#!/usr/bin/env bash
set -e

# ============================================
# Installer untuk Single-Session-CLI-Chatbot-AI
# ============================================

REPO_URL="https://github.com/Rovikin/Single-Session-CLI-Chatbot-AI.git"
INSTALL_DIR="$HOME/Single-Session-CLI-Chatbot-AI"

echo "[*] Update & upgrade Termux packages..."
pkg update -y
pkg upgrade -y

echo "[*] Install dependencies Termux..."
if [ -f "$INSTALL_DIR/dependencies.txt" ]; then
    while read pkgname; do
        if [ ! -z "$pkgname" ]; then
            pkg install -y "$pkgname"
        fi
    done < "$INSTALL_DIR/dependencies.txt"
fi

echo "[*] Install Python packages..."
pip install --upgrade pip
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    pip install -r "$INSTALL_DIR/requirements.txt"
fi

# Clone repo jika belum ada
if [ ! -d "$INSTALL_DIR" ]; then
    echo "[*] Clone repo..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

echo "[*] Set permission untuk script..."
chmod +x ai.py

echo "[*] Instalasi selesai! Jalankan script dengan: python ai.py"
