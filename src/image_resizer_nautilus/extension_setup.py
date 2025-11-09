#!/usr/bin/env python3
"""
Setup script for the nautilus extension.
Run this after installing the package to create the symlink.
"""

import os
import subprocess
import sys

def main():
    """Create the nautilus extension symlink"""
    try:
        # Import the package to get its location
        import image_resizer_nautilus
        
        package_dir = os.path.dirname(image_resizer_nautilus.__file__)
        source_path = os.path.join(package_dir, 'nautilus_extension.py')
        
        if not os.path.exists(source_path):
            print("❌ Error: Could not find nautilus_extension.py")
            return 1
        
        # Target path for the symlink
        target_dir = os.path.expanduser("~/.local/share/nautilus-python/extensions")
        target_path = os.path.join(target_dir, "image-resizer-extension.py")
        
        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)
        
        # Remove existing symlink or file
        if os.path.exists(target_path):
            if os.path.islink(target_path):
                os.unlink(target_path)
                print("📝 Removed existing symlink")
            else:
                os.remove(target_path)
                print("📝 Removed existing file")
        
        # Create the symlink
        os.symlink(source_path, target_path)
        print(f"✅ Created symlink: {target_path}")
        
        # Verify the symlink works
        if os.path.exists(target_path):
            print("✅ Symlink verified and working")
        else:
            print("❌ Symlink created but target not accessible")
            return 1
        
        # Restart nautilus to load the extension
        print("🔄 Restarting nautilus...")
        try:
            subprocess.run(['nautilus', '-q'], capture_output=True, timeout=10)
            print("✅ Nautilus restarted successfully")
        except subprocess.TimeoutExpired:
            print("⚠️  Nautilus restart timed out (may still work)")
        except Exception as e:
            print(f"⚠️  Could not restart nautilus automatically: {e}")
            print("   Please restart nautilus manually: nautilus -q")
        
        print("\n🎉 Setup complete!")
        print("You can now right-click on image files in Nautilus to resize them.")
        return 0
        
    except ImportError:
        print("❌ Error: image-resizer-nautilus package not found")
        print("   Make sure the package is installed: pip install image-resizer-nautilus")
        return 1
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())