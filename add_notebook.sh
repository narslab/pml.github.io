#!/bin/bash
# add_notebook.sh - Script to add a new notebook to the Jekyll site

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <notebook_file.ipynb> <title>"
    echo "Example: $0 assets/notebooks/my-notebook.ipynb \"My Notebook Title\""
    exit 1
fi

NOTEBOOK_PATH="$1"
TITLE="$2"

# Check if notebook exists
if [ ! -f "$NOTEBOOK_PATH" ]; then
    echo "❌ Notebook file $NOTEBOOK_PATH not found"
    exit 1
fi

# Extract notebook name without path and extension
NOTEBOOK_NAME=$(basename "$NOTEBOOK_PATH" .ipynb)
NOTEBOOK_FILENAME=$(basename "$NOTEBOOK_PATH")

# Create slug for URL
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

echo "📓 Adding notebook: $TITLE"
echo "   File: $NOTEBOOK_PATH"
echo "   Slug: $SLUG"

# Convert notebook to HTML
echo "🔄 Converting notebook to HTML..."
python convert_notebooks_v2.py "$NOTEBOOK_PATH"

# Get next nav order
NEXT_ORDER=$(ls notebooks/*.md 2>/dev/null | wc -l)
NEXT_ORDER=$((NEXT_ORDER + 1))

# Create notebook page
NOTEBOOK_PAGE="notebooks/${SLUG}.md"
cat > "$NOTEBOOK_PAGE" << EOF
---
layout: notebook
title: "$TITLE"
description: "Description for $TITLE notebook."
notebook_path: "$NOTEBOOK_PATH"
notebook_html: "notebooks/${NOTEBOOK_NAME}.html"
nav_order: $NEXT_ORDER
parent: Notebooks
---

## Notebook Contents

This notebook covers:

- Topic 1
- Topic 2
- Topic 3

Use the buttons above to download the notebook or open it in your preferred environment.
EOF

echo "✅ Created notebook page: $NOTEBOOK_PAGE"
echo "📝 Edit the description and topics in $NOTEBOOK_PAGE"
echo "🔗 Link to notebook: /notebooks/${SLUG}/"

# Build site to test
echo "🏗️  Testing build..."
bundle exec jekyll build > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "To link this notebook in your modules, use:"
    echo ": **NOTEBOOK**{: .label .label-activity}[$TITLE](/notebooks/${SLUG}/)"
else
    echo "❌ Build failed. Check your configuration."
    exit 1
fi
