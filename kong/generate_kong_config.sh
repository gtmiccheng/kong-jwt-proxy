#!/usr/bin/env bash
set -euo pipefail

# Generate kong.yml from template using envsubst
# Reads variables from .env file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if .env exists
if [[ ! -f ../.env ]]; then
    echo "Error: .env file not found. Copy .env.example to .env and configure it."
    exit 1
fi

# Check if template exists
if [[ ! -f kong.template.yml ]]; then
    echo "Error: kong.template.yml not found."
    exit 1
fi

# Load .env and export variables for envsubst
set -a
source ../.env
set +a

# Run envsubst to substitute variables
envsubst < kong.template.yml > kong.yml

echo "Generated kong.yml from template with .env variables"