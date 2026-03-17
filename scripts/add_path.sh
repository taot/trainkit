#! /usr/bin/env bash

SCRIPT_DIR="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PROJ_DIR="$(dirname "$SCRIPT_DIR")"

file="$HOME/.bashrc"

line1="TRAINKIT_DIR=\"$PROJ_DIR\""
line2='export PATH="$PATH:$TRAINKIT_DIR/bin"'

if ! grep -Fxq "$line1" "$file"; then
    printf '\n%s\n' "$line1" >> "$file"
fi

if ! grep -Fxq "$line2" "$file"; then
    printf '%s\n' "$line2" >> "$file"
fi