#!/bin/bash
set -e

echo "Installing Image Resizer (Development)..."
pip3 install --user .

echo "Setting up nautilus extension..."
image-resizer-setup