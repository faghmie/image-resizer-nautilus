#!/bin/bash
set -e

echo "Building RPM package..."

# Create build directory
BUILD_DIR="rpm-build"
mkdir -p $BUILD_DIR/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy spec file
cp packaging/rpm/image-resizer-nautilus.spec $BUILD_DIR/SPECS/

# Create source tarball
tar czf $BUILD_DIR/SOURCES/image-resizer-nautilus-1.0.0.tar.gz \
    --exclude=.git \
    --exclude=*.pyc \
    --exclude=__pycache__ \
    --exclude=*.egg-info \
    --exclude=build \
    --exclude=dist \
    --transform 's,^,image-resizer-nautilus-1.0.0/,' \
    .

# Build RPM
rpmbuild -ba \
    --define "_topdir $(pwd)/$BUILD_DIR" \
    $BUILD_DIR/SPECS/image-resizer-nautilus.spec

echo "RPM package built:"
find $BUILD_DIR/RPMS -name "*.rpm" -type f