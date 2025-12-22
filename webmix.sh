#!/bin/bash
set -e

URL=$1
OUTPUT_FILE=${2:-"webmix.md"}

if [ -z "$URL" ]; then
    echo "Usage: $0 <url> [output_file]"
    exit 1
fi

# Create a temporary directory
WORK_DIR=$(mktemp -d)
echo "Created temporary directory: $WORK_DIR"

# Ensure cleanup on exit
trap 'rm -rf "$WORK_DIR"' EXIT

echo "Mirroring $URL..."
# Using options to ensure we get a good local copy restricted to the subfolder if applicable
wget \
    --recursive \
    --no-parent \
    --page-requisites \
    --convert-links \
    --adjust-extension \
    --wait=1 \
    --random-wait \
    --execute robots=off \
    --user-agent="Mozilla/5.0 (compatible; Webmix/0.1; +https://github.com/yourusername/webmix)" \
    -P "$WORK_DIR" \
    "$URL"

echo "Aggregating content..."
# Run webmix on the downloaded directory
# We assume this script is run from the project root where poetry is configured

# Determine the command to run
if [ -n "$WEBMIX_CMD" ]; then
    # 1. Explicit override (Testing)
    CMD="$WEBMIX_CMD"
elif [ -n "$VIRTUAL_ENV" ]; then
    # 2. Already in a venv (Dev/Manual usage)
    CMD="python3 -m webmix.main"
else
    # 3. Standalone usage (User)
    CMD="uv run webmix"
fi

$CMD "$WORK_DIR" --output "$OUTPUT_FILE"

echo "Done! Output saved to $OUTPUT_FILE"
