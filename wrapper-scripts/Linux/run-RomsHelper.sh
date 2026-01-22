#!/usr/bin/env bash

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

BIN="$DIR/RomsHelper"

if [ ! -x "$BIN" ]; then
    echo "RomsHelper binary not found or not executable"
    read -p "Press Enter to exit... "
    exit 1
fi

if command -v x-terminal-emulator >/dev/null 2>&1; then
    exec x-terminal-emulator -e "$BIN"
elif command -v gnome-terminal >/dev/null 2>&1; then
    exec gnome-terminal -- "$BIN"
elif command -v konsole >/dev/null 2>&1; then
    exec konsole -e "$BIN"
elif command -v xfce4-terminal >/dev/null 2>&1; then
    exec xfce4-terminal --command "$BIN"
elif command -v xterm >/dev/null 2>&1; then
    exec xterm -e "$BIN"
else
    echo "No supported terminal emulator found."
    echo "Please run RomsHelper from a terminal."
    read -p "Press Enter to exit..."
    exit 1
fi