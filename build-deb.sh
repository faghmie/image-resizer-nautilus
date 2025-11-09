#!/bin/bash
set -e

echo "Building Debian package..."

# Check dependencies
if ! command -v dpkg-buildpackage >/dev/null 2>&1; then
    echo "Error: dpkg-buildpackage not found. Install devscripts:"
    echo "  sudo apt install devscripts debhelper dh-python"
    exit 1
fi

# Clean previous builds
rm -rf debian/
rm -f ../image-resizer-nautilus_*

# Copy debian packaging files
mkdir -p debian
cp -r packaging/debian/* debian/
chmod +x debian/rules

# Update version in changelog if needed
if [ ! -f debian/changelog ]; then
    cat > debian/changelog << EOF
image-resizer-nautilus (1.0.0-1) unstable; urgency=medium

  * Initial release.

 -- Faghmie Davids <faghmie@gmail.com>  $(date -R)
EOF
fi

# Build the package
dpkg-buildpackage -uc -us

echo "Debian package built:"
ls -la ../image-resizer-nautilus_*.deb