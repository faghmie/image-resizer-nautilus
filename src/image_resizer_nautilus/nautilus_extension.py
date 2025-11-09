#!/usr/bin/env python3

import os
import subprocess

# Import without version specification
from gi.repository import GObject, Nautilus
from gi.repository import Notify

class ImageContextMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    
    def __init__(self):
        Notify.init("Image Resizer")
        pass
    
    def get_file_items(self, files):
        """Return menu items for file selection"""
        if len(files) != 1:
            return []
            
        file_info = files[0]
        
        # Check if it's a local file
        if file_info.get_uri_scheme() != 'file':
            return []
            
        filename = file_info.get_name()
        if not filename:
            return []
            
        # Check if it's an image
        image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg')
        if not filename.lower().endswith(image_extensions):
            return []
        
        # Create menu item
        item = Nautilus.MenuItem(
            name="ImageResize",
            label="Resize Image...",
            tip="Open resize options dialog"
        )
        item.connect('activate', self._launch_resizer, file_info)
        
        return [item]
    
    def get_background_items(self, file):
        return []
    
    def notify(self, message):
        notification = Notify.Notification.new(
            "Hello World",
            message,
            "dialog-information"  # Optional icon name
        )
        notification.show()
            
    def _launch_resizer(self, menu, file_info):
        """Launch the standalone resizer script"""
        try:
            file_path = file_info.get_location().get_path()
            
            
            if file_path and os.path.exists(file_path):
                # Get the directory where this script is located
                current_dir = os.path.dirname(os.path.realpath(__file__))
                script_path = os.path.join(current_dir, 'image_resizer.py')
                
                # Alternative: if the script is in a known location
                # script_path = os.path.expanduser('~/.local/share/nautilus-python/extensions/image-resizer.py')
                
                if os.path.exists(script_path):
                    # Use the system Python to run the script
                    subprocess.Popen(['python3', script_path, file_path])
                else:
                    print(f"Resizer script not found at: {script_path}")
        except Exception as e:
            print(f"Error launching resizer: {e}")