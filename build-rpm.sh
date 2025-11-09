#!/bin/bash
set -e

echo "🔨 Building RPM package for Image Resizer Nautilus Extension"
echo "============================================================"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf rpm-build/

# Create build directory
BUILD_DIR="rpm-build"
mkdir -p $BUILD_DIR/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

echo "📁 Build directory: $BUILD_DIR"

# Copy spec file
if [ -f "packaging/rpm/image-resizer-nautilus.spec" ]; then
    cp packaging/rpm/image-resizer-nautilus.spec $BUILD_DIR/SPECS/
    echo "✅ Copied spec file"
else
    echo "❌ Spec file not found: packaging/rpm/image-resizer-nautilus.spec"
    exit 1
fi

# Create source tarball
echo "📦 Creating source tarball..."
tar czf $BUILD_DIR/SOURCES/image-resizer-nautilus-1.0.0.tar.gz \
    --exclude=.git \
    --exclude=*.pyc \
    --exclude=__pycache__ \
    --exclude=*.egg-info \
    --exclude=build \
    --exclude=dist \
    --exclude=rpm-build \
    --exclude=debian \
    --exclude=packaging \
    --transform 's,^,image-resizer-nautilus-1.0.0/,' \
    .

if [ $? -eq 0 ]; then
    echo "✅ Source tarball created"
    echo "   Size: $(du -h $BUILD_DIR/SOURCES/image-resizer-nautilus-1.0.0.tar.gz | cut -f1)"
else
    echo "❌ Failed to create source tarball"
    exit 1
fi

# Build RPM
echo "🏗️  Building RPM package..."
if rpmbuild -ba \
    --define "_topdir $(pwd)/$BUILD_DIR" \
    $BUILD_DIR/SPECS/image-resizer-nautilus.spec; then
    
    echo "✅ RPM package built successfully!"
    echo ""
    echo "📦 Built packages:"
    find $BUILD_DIR/RPMS -name "*.rpm" -type f | while read file; do
        echo "   - $file"
        ls -lh "$file"
    done
    find $BUILD_DIR/SRPMS -name "*.rpm" -type f | while read file; do
        echo "   - $file (source)"
        ls -lh "$file"
    done
else
    echo "❌ RPM build failed"
    echo ""
    echo "🔧 Troubleshooting tips:"
    echo "   1. Check if all dependencies are installed:"
    echo "      sudo dnf install rpm-build python3-devel python3-setuptools"
    echo "   2. Try building with more verbose output:"
    echo "      rpmbuild -ba --define '_topdir $(pwd)/$BUILD_DIR' $BUILD_DIR/SPECS/image-resizer-nautilus.spec --verbose"
    exit 1
fi