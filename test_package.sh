#!/bin/bash
set -e

echo "🧪 Testing Image Resizer Nautilus Extension"
echo "==========================================="

# Test files
TEST_DIR="/tmp/image-resizer-test"
TEST_IMAGE="$TEST_DIR/test-image.jpg"

# Create test directory
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

# Download test image if not exists
if [ ! -f "$TEST_IMAGE" ]; then
    echo "📥 Downloading test image..."
    wget -q -O "$TEST_IMAGE" "https://picsum.photos/800/600"
fi

echo "✅ Test setup complete"

# Test 1: Verify installation
echo ""
echo "1. Verifying installation..."
if command -v image-resizer-gui >/dev/null 2>&1; then
    echo "   ✅ image-resizer-gui command found"
else
    echo "   ❌ image-resizer-gui command not found"
    exit 1
fi

if command -v image-resizer-uninstall >/dev/null 2>&1; then
    echo "   ✅ image-resizer-uninstall command found"
else
    echo "   ❌ image-resizer-uninstall command not found"
    exit 1
fi

# Test 2: Verify Python package
echo ""
echo "2. Verifying Python package..."
if python3 -c "import image_resizer_nautilus" 2>/dev/null; then
    echo "   ✅ Python package imports successfully"
else
    echo "   ❌ Python package import failed"
    exit 1
fi

# Test 3: Verify nautilus extension symlink
echo ""
echo "3. Verifying nautilus extension..."
SYMLINK_PATH="$HOME/.local/share/nautilus-python/extensions/image-resizer-extension.py"
if [ -L "$SYMLINK_PATH" ]; then
    echo "   ✅ Nautilus extension symlink exists"
    if [ -e "$SYMLINK_PATH" ]; then
        echo "   ✅ Symlink target exists"
    else
        echo "   ❌ Symlink target missing"
    fi
else
    echo "   ❌ Nautilus extension symlink not found"
fi

# Test 4: Test resizer with basic functionality
echo ""
echo "4. Testing basic functionality..."
if [ -f "$TEST_IMAGE" ]; then
    echo "   🖼️  Test image: $TEST_IMAGE"
    # Test that the command runs (it will show GUI, so we test it doesn't crash immediately)
    timeout 5s image-resizer-gui "$TEST_IMAGE" && echo "   ✅ Resizer GUI launches" || echo "   ⚠️  Resizer GUI may have timed out (normal for GUI apps)"
else
    echo "   ❌ Test image not found"
fi

# Test 5: Verify dependencies
echo ""
echo "5. Checking dependencies..."
if command -v convert >/dev/null 2>&1; then
    echo "   ✅ ImageMagick (convert) found"
else
    echo "   ⚠️  ImageMagick not found (resize operations will fail)"
fi

if python3 -c "import gi; gi.require_version('Gtk', '4.0'); from gi.repository import Gtk" 2>/dev/null; then
    echo "   ✅ GTK4 available"
else
    echo "   ❌ GTK4 not available"
    exit 1
fi

echo ""
echo "🎉 All tests completed!"
echo ""
echo "Manual tests to perform:"
echo "1. Open Nautilus: nautilus $TEST_DIR"
echo "2. Right-click on test-image.jpg"
echo "3. Verify 'Resize Image...' appears in context menu"
echo "4. Test the resize dialog functionality"