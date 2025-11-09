# Image Resizer Nautilus Extension

A powerful Nautilus file manager extension that adds a right-click context menu option to resize images with a modern GTK4 interface.


## Features

- **Right-click Integration**: Simply right-click on any image file in Nautilus and select "Resize Image..."
- **Modern GTK4 Interface**: Clean, native-looking dialog with intuitive controls
- **Multiple Resize Options**:
  - Preset sizes (25%, 50%, 75%, 100%, 150%, 200%)
  - Standard resolutions (QVGA, VGA, SVGA, XGA, HD, Full HD, 4K)
  - Custom dimensions with pixel-perfect control
- **Aspect Ratio Locking**: Maintain original proportions automatically
- **Format Conversion**: Save as PNG, JPEG, WebP, or keep original format
- **Progress Indication**: Visual feedback during resize operations
- **ImageMagick Powered**: Uses industry-standard ImageMagick for high-quality resizing

## Supported Formats

- JPEG/JPG
- PNG
- WebP
- GIF
- BMP
- TIFF
- SVG

## Requirements

### System Dependencies

**Essential:**
- `nautilus` - GNOME file manager
- `python3` - Python 3.6 or higher
- `python3-gi` - Python GObject introspection
- `imagemagick` - Image processing backend

**Optional:**
- `nautilus-python` - Python extension support (usually included with Nautilus)

### Python Dependencies
- `PyGObject` >= 3.38.0 - GTK4 bindings (automatically installed)

## Installation

### Method 1: From PyPI (Recommended)

```bash
# Install the package
pip install --user image-resizer-nautilus

# Set up the nautilus extension
image-resizer-setup
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://github.com/faghmie/image-resizer-nautilus
cd image-resizer-nautilus

# Install the package
pip install --user .

# Set up the nautilus extension
image-resizer-setup
```

### Method 3: Using Install Script (Development)

```bash
git clone https://github.com/faghmie/image-resizer-nautilus
cd image-resizer-nautilus

# Run the install script (handles everything)
python install.py
```

## Usage

### Using Nautilus Integration

1. **Open Nautilus** and navigate to any folder containing images
2. **Right-click** on an image file (JPEG, PNG, WebP, etc.)
3. **Select "Resize Image..."** from the context menu
4. **Choose your resize options** in the dialog:
   - Select a preset size or enter custom dimensions
   - Choose output format
   - Select destination filename
5. **Click "Resize Image"** to process

The resized image will be saved with "_resized" appended to the filename in the same directory.

### Using Command Line

You can also launch the resizer directly from the terminal:

```bash
image-resizer-gui /path/to/your/image.jpg
```

## Uninstallation

### Complete Removal

```bash
# Remove the nautilus extension
image-resizer-uninstall

# Uninstall the Python package
pip uninstall image-resizer-nautilus
```

### Quick Uninstall

```bash
# Run the complete uninstall script (if available from source)
./complete-uninstall.sh
```

## Troubleshooting

### Extension not appearing in context menu?

1. **Run the setup command:**
   ```bash
   image-resizer-setup
   ```

2. **Restart Nautilus:**
   ```bash
   nautilus -q
   ```

3. **Check the extension symlink:**
   ```bash
   ls -la ~/.local/share/nautilus-python/extensions/image-resizer-extension.py
   ```

### "ImageMagick not found" error?

Install ImageMagick on your system:

```bash
# Ubuntu/Debian
sudo apt install imagemagick

# Fedora/RHEL
sudo dnf install ImageMagick

# Arch Linux
sudo pacman -S imagemagick

# openSUSE
sudo zypper install imagemagick
```

### Permission errors?

- Use `--user` flag with pip for user installation
- For system-wide installation, use `sudo pip install` (not recommended)

### Resize operation fails?

- Check that the source image file is not corrupted
- Ensure you have write permissions to the destination directory
- Verify ImageMagick can process the image format

## Development

### Building from Source

```bash
# Clone the repository
git clone https://github.com/faghmie/image-resizer-nautilus
cd image-resizer-nautilus

# Install in development mode
pip install --user -e .

# Build distribution packages
python -m build
```

### Project Structure

```
image-resizer-nautilus/
├── src/image_resizer_nautilus/
│   ├── __init__.py              # Package initialization
│   ├── nautilus_extension.py    # Nautilus context menu provider
│   ├── image_resizer.py         # Main resize application
│   ├── extension_setup.py       # Setup script
│   └── uninstall.py            # Uninstall script
├── setup.py                    # Package configuration
├── pyproject.toml             # Modern packaging config
└── README.md                  # This file
```

### Available Commands

- `image-resizer-gui` - Launch the resize dialog directly
- `image-resizer-setup` - Set up the nautilus extension
- `image-resizer-uninstall` - Remove the nautilus extension

## FAQ

### Why do I need to run `image-resizer-setup` after installation?

For security reasons, Python packages cannot automatically modify system files or create symlinks during installation. The setup command ensures the nautilus extension is properly configured.

### Can I use this with other file managers?

No, this extension is specifically designed for Nautilus (GNOME Files). Other file managers like Nemo, Thunar, or Dolphin would require different extensions.

### How do I change the default output format?

The output format is selected each time you resize an image. You can choose to keep the original format or convert to PNG, JPEG, or WebP.

### Does this modify my original images?

No, the original images are never modified. Resized images are saved as new files with "_resized" appended to the filename.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are installed
3. Check the system logs for error messages
4. Create an issue on GitHub with detailed information

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- GNOME Project for Nautilus file manager
- ImageMagick team for powerful image processing capabilities
- GTK team for the excellent GUI toolkit
- Python packaging community for distribution tools

---

**Note**: This extension requires Nautilus with Python support. Most modern GNOME installations include this by default.