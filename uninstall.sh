#!/bin/bash

set -e

echo "Uninstalling Image Resizer Nautilus Extension..."

# Remove the symlink from user directory
USER_EXTENSION_PATH="$HOME/.local/share/nautilus-python/extensions/image-resizer-extension.py"
if [ -L "$USER_EXTENSION_PATH" ] || [ -f "$USER_EXTENSION_PATH" ]; then
    echo "Removing extension symlink: $USER_EXTENSION_PATH"
    rm -f "$USER_EXTENSION_PATH"
fi

# Remove the symlink from system directory (if installed with sudo)
SYSTEM_EXTENSION_PATH="/usr/share/nautilus-python/extensions/image-resizer-extension.py"
if [ -L "$SYSTEM_EXTENSION_PATH" ] || [ -f "$SYSTEM_EXTENSION_PATH" ]; then
    echo "Removing extension symlink: $SYSTEM_EXTENSION_PATH"
    sudo rm -f "$SYSTEM_EXTENSION_PATH"
fi

# Try to uninstall the Python package
echo "Uninstalling Python package..."
pip3 uninstall -y image-resizer-nautilus || true

# Restart nautilus to unload the extension
echo "Restarting nautilus..."
nautilus -q 2>/dev/null || true

echo "Uninstallation complete!"
echo "The image resizer extension has been removed."