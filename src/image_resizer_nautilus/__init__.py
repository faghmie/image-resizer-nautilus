"""Nautilus extension for resizing images with right-click menu"""

__version__ = "1.0.0"
__author__ = "Faghmie Davids"
__email__ = "faghmie@gmail.com"

import os
import subprocess
import sys

def _auto_setup():
    extension_path = os.path.expanduser("~/.local/share/nautilus-python/extensions/image-resizer-extension.py")
    
    if not os.path.exists(extension_path):
        try:
            package_dir = os.path.dirname(__file__)
            source_path = os.path.join(package_dir, 'nautilus_extension.py')
            
            if os.path.exists(source_path):
                target_dir = os.path.dirname(extension_path)
                os.makedirs(target_dir, exist_ok=True)
                
                if os.path.exists(extension_path):
                    os.remove(extension_path)
                
                os.symlink(source_path, extension_path)
                print("✅ Nautilus extension configured!")
                
                # Try to restart nautilus
                try:
                    subprocess.Popen(['nautilus', '-q'], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL)
                except:
                    pass
        except Exception:
            # Silent fail
            pass

# This runs when package is imported
_auto_setup()