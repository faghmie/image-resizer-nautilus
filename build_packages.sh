#!/bin/bash
set -e

echo "Building distribution packages..."

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Install build tools if not present
if ! python3 -c "import build" 2>/dev/null; then
    echo "Installing build tools..."
    pip3 install build
fi

# Build source distribution and wheel
echo "Building packages..."
python3 -m build

echo "✅ Build complete! Packages in dist/ directory:"
ls -la dist/

# Optional: Check package
if command -v twine >/dev/null 2>&1; then
    echo "Checking package with twine..."
    twine check dist/*
else
    echo "Install twine to check packages: pip3 install twine"
fi