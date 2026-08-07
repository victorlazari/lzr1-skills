#!/bin/bash

# validate-lua.sh
# Deterministic script to run `luac -p` or `luacheck` for syntax validation.

set -e

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <lua_file>"
    exit 1
fi

LUA_FILE="$1"

if [ ! -f "$LUA_FILE" ]; then
    echo "Error: File '$LUA_FILE' not found."
    exit 1
fi

if command -v luacheck >/dev/null 2>&1; then
    echo "Running luacheck on '$LUA_FILE'..."
    luacheck "$LUA_FILE"
elif command -v luac >/dev/null 2>&1; then
    echo "Running luac -p on '$LUA_FILE'..."
    luac -p "$LUA_FILE"
else
    echo "Error: Neither 'luacheck' nor 'luac' is installed."
    exit 1
fi

echo "Validation successful."
exit 0
