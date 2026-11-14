#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if an input file was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-mov-file>"
    exit 1
fi

INPUT="$1"
FILENAME=$(basename -- "$INPUT")
BASENAME="${FILENAME%.*}"

# Ensure the demo output directory exists
mkdir -p demo

OUTPUT="demo/${BASENAME}.gif"

echo "Converting $INPUT -> $OUTPUT..."

# Run ffmpeg with high-quality scaling and palette generation for crisp pixel art/screen recordings
ffmpeg -i "$INPUT" -vf "fps=15,scale=320:-1:flags=lanczos" -y "$OUTPUT"

echo "Done! Saved to $OUTPUT"
