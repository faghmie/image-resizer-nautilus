#!/usr/bin/env python3
"""
Uninstall script for the nautilus extension.
Removes the symlink and restarts nautilus.
"""

import os
import subprocess
import sys

def main():
    """Remove the nautilus extension symlink"""
    print("Removing Image Resizer Nautilus Extension...")
    
    # Paths to check for the extension
    extension_paths = [
        os.path.expanduser("~/.local/share/nautilus-python/extensions/image-resizer-extension.py"),
        "/usr/share/nautilus-python/extensions/image-resizer-extension.py"
    ]
    
    removed = False
    
    for path in extension_paths:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"✅ Removed: {path}")
                removed = True
            except PermissionError:
                print(f"❌ Permission denied: {path}")
                print("   Try running with sudo for system-wide installation")
            except Exception as e:
                print(f"❌ Error removing {path}: {e}")
        else:
            print(f"ℹ️  Not found: {path}")
    
    if removed:
        # Restart nautilus to unload the extension
        print("🔄 Restarting nautilus...")
        try:
            subprocess.run(['nautilus', '-q'], capture_output=True, timeout=10)
            print("✅ Nautilus restarted")
        except:
            print("⚠️  Please restart nautilus manually: nautilus -q")
        
        print("✅ Uninstallation complete!")
    else:
        print("ℹ️  No extension files found to remove")
    
    return 0 if removed else 1

if __name__ == "__main__":
    sys.exit(main())