#!/usr/bin/env python3

import sys
import os
import subprocess
import gi

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gio', '2.0')
from gi.repository import Gtk, Gio

class ImageResizer:
    """Main application class for image resizing"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.original_width = None
        self.original_height = None
        self.window = None
        self.app = None
        
    def get_image_dimensions(self):
        """Get original image dimensions using ImageMagick"""
        try:
            result = subprocess.run([
                'identify', '-format', '%wx%h', self.file_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                dimensions = result.stdout.strip().split('x')
                self.original_width = int(dimensions[0])
                self.original_height = int(dimensions[1])
                return True
        except:
            pass
        
        # Fallback to default dimensions if we can't get them
        self.original_width = 1920
        self.original_height = 1080
        return False

    def run(self):
        """Main application entry point"""
        if not self.get_image_dimensions():
            print("Warning: Could not get image dimensions, using defaults")
        
        self.app = Gtk.Application(application_id="com.example.resizer")
        self.app.hold()
        
        self.window = MainWindow(self, self.file_path, self.original_width, self.original_height)
        self.window.connect("close-request", self.on_close_request)
        self.window.show()
        
        return self.app.run(sys.argv)
    
    def on_close_request(self, win):
        """Handle window close request"""
        print("Window closing...")
        self.app.quit()
        return False


class MainWindow(Gtk.Window):
    """Main application window"""
    
    def __init__(self, resizer, file_path, original_width, original_height):
        super().__init__()
        self.resizer = resizer
        self.file_path = file_path
        self.original_width = original_width
        self.original_height = original_height
        self.is_resizing = False
        self.progress_timeout_id = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Initialize the user interface"""
        self.set_title(f"Resize Image: {os.path.basename(self.file_path)}")
        self.set_default_size(450, 450)  # Increased height for progress bar
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)
        self.set_child(main_box)
        
        # Create UI sections
        self.dimensions_section = DimensionsSection(self.original_width, self.original_height)
        self.preset_section = PresetSection()
        self.custom_size_section = CustomSizeSection(self.original_width, self.original_height)
        self.output_section = OutputSection(self.file_path)
        self.progress_section = ProgressSection()
        self.button_section = ButtonSection()
        
        # Connect signals between sections
        self.connect_signals()
        
        # Add sections to main window
        main_box.append(self.dimensions_section.widget)
        main_box.append(self.preset_section.widget)
        main_box.append(self.custom_size_section.widget)
        main_box.append(self.output_section.widget)
        main_box.append(self.progress_section.widget)
        main_box.append(self.button_section.widget)
        
        # Connect resize button
        self.button_section.resize_btn.connect('clicked', self.on_resize_clicked)
        self.button_section.cancel_btn.connect('clicked', self.on_cancel_clicked)
    
    def connect_signals(self):
        """Connect signals between different UI sections"""
        # Preset section to custom size section
        self.preset_section.combo.connect("notify::selected", 
                                         self.preset_section.on_preset_changed,
                                         self.custom_size_section,
                                         self.original_width,
                                         self.original_height)
        
        # Custom size section internal connections (updated to use spin buttons)
        self.custom_size_section.width_spin.connect("value-changed", 
                                                   self.custom_size_section.on_width_changed,
                                                   self.original_width,
                                                   self.original_height)
        self.custom_size_section.height_spin.connect("value-changed", 
                                                    self.custom_size_section.on_height_changed,
                                                    self.original_width,
                                                    self.original_height)
        
        # Output format changes
        self.output_section.format_combo.connect("notify::selected", 
                                               self.output_section.on_format_changed,
                                               self.file_path)
    
    def on_resize_clicked(self, btn):
        """Handle resize button click - now prompts for output file"""
        if self.is_resizing:
            return  # Prevent multiple clicks during resize
        
        width, height = self.custom_size_section.get_dimensions()
        format_index = self.output_section.format_combo.get_selected()
        
        # Validation
        if width is None and height is None:
            ResizeOperation.show_error('Please enter valid width and/or height values')
            return
        
        # Generate default output filename
        default_output_path = self.output_section.generate_default_output_path()
        
        # Show file chooser dialog
        self.show_save_dialog_async(default_output_path, width, height, format_index)
    
    def on_cancel_clicked(self, btn):
        """Handle cancel button click"""
        if not self.is_resizing:
            self.close()
    
    def show_save_dialog_async(self, default_path, width, height, format_index):
        """Show save file dialog asynchronously and handle response"""
        dialog = Gtk.FileDialog(
            title="Save Resized Image As",
            initial_name=os.path.basename(default_path) if default_path else "resized_image.png"
        )
        
        # Set up file filters
        filters = self.create_file_filters()
        dialog.set_filters(filters)
        
        # Set initial folder if default path has a directory
        if default_path and os.path.dirname(default_path):
            initial_folder = Gio.File.new_for_path(os.path.dirname(default_path))
            dialog.set_initial_folder(initial_folder)
        
        # Show dialog asynchronously
        dialog.save(self, None, self.on_save_dialog_finished, width, height, format_index)
    
    def on_save_dialog_finished(self, dialog, result, width, height, format_index):
        """Handle the save dialog response"""
        try:
            file = dialog.save_finish(result)
            if file:
                output_path = file.get_path()
                self.start_resize_operation(width, height, format_index, output_path)
        except Exception as e:
            print(f"Error with save dialog: {e}")
            # User cancelled the dialog or error occurred
            pass
    
    def create_file_filters(self):
        """Create file filters for the save dialog"""
        filters = Gio.ListStore.new(Gtk.FileFilter)
        
        # All image files filter
        filter_all = Gtk.FileFilter()
        filter_all.set_name("All image files")
        filter_all.add_pattern("*.png")
        filter_all.add_pattern("*.jpg")
        filter_all.add_pattern("*.jpeg")
        filter_all.add_pattern("*.webp")
        filter_all.add_pattern("*.gif")
        filter_all.add_pattern("*.bmp")
        filters.append(filter_all)
        
        # PNG filter
        filter_png = Gtk.FileFilter()
        filter_png.set_name("PNG images")
        filter_png.add_pattern("*.png")
        filters.append(filter_png)
        
        # JPEG filter
        filter_jpg = Gtk.FileFilter()
        filter_jpg.set_name("JPEG images")
        filter_jpg.add_pattern("*.jpg")
        filter_jpg.add_pattern("*.jpeg")
        filters.append(filter_jpg)
        
        # WebP filter
        filter_webp = Gtk.FileFilter()
        filter_webp.set_name("WebP images")
        filter_webp.add_pattern("*.webp")
        filters.append(filter_webp)
        
        return filters
    
    def start_resize_operation(self, width, height, format_index, output_path):
        """Start the resize operation with progress indication"""
        self.is_resizing = True
        self.progress_section.show_progress()
        self.button_section.set_buttons_sensitive(False)  # Disable buttons during resize
        
        # Start progress animation
        self.start_progress_animation()
        
        # Start resize in a separate thread to keep UI responsive
        import threading
        thread = threading.Thread(
            target=self.perform_resize_in_thread,
            args=(width, height, format_index, output_path)
        )
        thread.daemon = True
        thread.start()
    
    def start_progress_animation(self):
        """Start the progress bar pulsing animation"""
        from gi.repository import GLib
        
        def pulse_progress():
            if self.is_resizing:
                self.progress_section.progress_bar.pulse()
                return True  # Continue pulsing
            return False  # Stop pulsing
        
        # Pulse every 100ms
        self.progress_timeout_id = GLib.timeout_add(100, pulse_progress)
    
    def stop_progress_animation(self):
        """Stop the progress bar animation"""
        if self.progress_timeout_id:
            from gi.repository import GLib
            GLib.source_remove(self.progress_timeout_id)
            self.progress_timeout_id = None
    
    def perform_resize_in_thread(self, width, height, format_index, output_path):
        """Perform resize in a separate thread"""
        from gi.repository import GLib
        
        # Update status label
        def update_status(message):
            self.progress_section.status_label.set_label(message)
        
        GLib.idle_add(update_status, "Starting resize operation...")
        
        # Perform the resize operation
        success = ResizeOperation.perform_resize(
            self.file_path, 
            width, 
            height, 
            format_index, 
            output_path, 
            self
        )
        
        # Reset UI state
        def reset_ui():
            self.is_resizing = False
            self.stop_progress_animation()
            self.progress_section.hide_progress()
            self.button_section.set_buttons_sensitive(True)
            
            if success:
                GLib.idle_add(update_status, "Resize completed successfully!")
                # Close window after 2 seconds to let user see success message
                GLib.timeout_add(2000, self.close_after_success)
            else:
                GLib.idle_add(update_status, "Resize failed - check error messages")
        
        GLib.idle_add(reset_ui)
    
    def close_after_success(self):
        """Close the window after successful resize"""
        self.close()
        return False  # Don't repeat timeout
      
class ProgressSection:
    """Section for progress indication"""
    
    def __init__(self):
        self.widget = self.create_widget()
        self.hide_progress()
    
    def create_widget(self):
        """Create the progress widget"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_text("Resizing image...")
        self.progress_bar.set_halign(Gtk.Align.FILL)
        
        # Status label
        self.status_label = Gtk.Label(label="Preparing to resize...")
        self.status_label.set_halign(Gtk.Align.START)
        
        main_box.append(self.progress_bar)
        main_box.append(self.status_label)
        
        return main_box
    
    def show_progress(self):
        """Show progress bar and start animation"""
        self.widget.set_visible(True)
        self.progress_bar.set_fraction(0.0)
        self.status_label.set_label("Resizing image...")
    
    def hide_progress(self):
        """Hide progress bar"""
        self.widget.set_visible(False)



class DimensionsSection:
    """Section displaying original image dimensions"""
    
    def __init__(self, width, height):
        self.widget = self.create_widget(width, height)
    
    def create_widget(self, width, height):
        """Create the dimensions display widget"""
        if width and height:
            dim_label = Gtk.Label(label=f"Original: {width} x {height} pixels")
            dim_label.set_halign(Gtk.Align.START)
            return dim_label
        return Gtk.Label(label="Original dimensions: Unknown")


class PresetSection:
    """Section for preset size selection"""
    
    def __init__(self):
        self.widget, self.combo = self.create_widget()
    
    def create_widget(self):
        """Create the preset selection widget"""
        preset_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        preset_label = Gtk.Label(label="Preset size:")
        preset_label.set_halign(Gtk.Align.START)
        preset_label.set_size_request(100, -1)
        
        preset_combo = Gtk.DropDown.new_from_strings([
            "Select preset...",
            "25% (Quarter size)",
            "50% (Half size)", 
            "75% (Three quarters)",
            "100% (Original)",
            "150% (1.5x)",
            "200% (2x)",
            "320x240 (QVGA)",
            "640x480 (VGA)",
            "800x600 (SVGA)",
            "1024x768 (XGA)",
            "1280x720 (HD)",
            "1920x1080 (Full HD)",
            "3840x2160 (4K)"
        ])
        preset_combo.set_selected(0)
        
        preset_box.append(preset_label)
        preset_box.append(preset_combo)
        return preset_box, preset_combo
    
    def on_preset_changed(self, combo, pspec, custom_section, original_width, original_height):
        """Handle preset selection change"""
        preset_index = combo.get_selected()
        if preset_index > 0:  # Not "Select preset..."
            # Percentage presets (indices 1-6)
            if preset_index <= 6:
                percentages = [0, 25, 50, 75, 100, 150, 200]
                percentage = percentages[preset_index]
                
                if original_width and original_height:
                    new_width = int((original_width * percentage) / 100)
                    new_height = int((original_height * percentage) / 100)
            else:
                # Fixed dimension presets (indices 7-13)
                dimensions = [
                    (0, 0),  # placeholder for index 0
                    (320, 240),   # QVGA
                    (640, 480),   # VGA
                    (800, 600),   # SVGA
                    (1024, 768),  # XGA
                    (1280, 720),  # HD
                    (1920, 1080), # Full HD
                    (3840, 2160)  # 4K
                ]
                new_width, new_height = dimensions[preset_index - 6]
            
            custom_section.set_dimensions(new_width, new_height)
            
class CustomSizeSection:
    """Section for custom width/height input with SpinButton"""
    
    def __init__(self, original_width, original_height):
        self.original_width = original_width
        self.original_height = original_height
        self.widget, self.width_spin, self.height_spin, self.aspect_ratio_check = self.create_widget()
        self.setup_signals()
    
    def create_widget(self):
        """Create the custom size input widgets with SpinButton"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Label
        custom_label = Gtk.Label(label="Custom size:")
        custom_label.set_halign(Gtk.Align.START)
        main_box.append(custom_label)
        
        # Width and height spin buttons
        size_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        width_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        width_label = Gtk.Label(label="Width:")
        
        # Create width SpinButton
        width_adjustment = Gtk.Adjustment(
            value=0,
            lower=1,
            upper=10000,
            step_increment=1,
            page_increment=10,
            page_size=0
        )
        self.width_spin = Gtk.SpinButton(adjustment=width_adjustment)
        self.width_spin.set_width_chars(8)
        self.width_spin.set_numeric(True)
        self.width_spin.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.width_spin.set_tooltip_text("Width in pixels")
        
        width_box.append(width_label)
        width_box.append(self.width_spin)
        
        height_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        height_label = Gtk.Label(label="Height:")
        
        # Create height SpinButton
        height_adjustment = Gtk.Adjustment(
            value=0,
            lower=1,
            upper=10000,
            step_increment=1,
            page_increment=10,
            page_size=0
        )
        self.height_spin = Gtk.SpinButton(adjustment=height_adjustment)
        self.height_spin.set_width_chars(8)
        self.height_spin.set_numeric(True)
        self.height_spin.set_update_policy(Gtk.SpinButtonUpdatePolicy.IF_VALID)
        self.height_spin.set_tooltip_text("Height in pixels")
        
        height_box.append(height_label)
        height_box.append(self.height_spin)
        
        size_box.append(width_box)
        size_box.append(height_box)
        main_box.append(size_box)
        
        # Aspect ratio checkbox
        aspect_ratio_check = Gtk.CheckButton.new_with_label("Lock aspect ratio")
        aspect_ratio_check.set_active(True)
        aspect_ratio_check.set_halign(Gtk.Align.START)
        aspect_ratio_check.set_tooltip_text("Maintain original aspect ratio when one dimension is set")
        main_box.append(aspect_ratio_check)
        
        return main_box, self.width_spin, self.height_spin, aspect_ratio_check
    
    def setup_signals(self):
        """Set up signals for the spin buttons"""
        # Connect value-changed signals for aspect ratio calculations
        self.width_spin.connect("value-changed", self.on_width_changed, self.original_width, self.original_height)
        self.height_spin.connect("value-changed", self.on_height_changed, self.original_width, self.original_height)
    
    def set_dimensions(self, width, height):
        """Set width and height values"""
        # Temporarily block handlers to avoid recursion
        self.width_spin.handler_block_by_func(self.on_width_changed)
        self.height_spin.handler_block_by_func(self.on_height_changed)
        
        self.width_spin.set_value(width)
        self.height_spin.set_value(height)
        
        self.width_spin.handler_unblock_by_func(self.on_width_changed)
        self.height_spin.handler_unblock_by_func(self.on_height_changed)
    
    def on_width_changed(self, spin, original_width, original_height):
        """Handle width spin button changes with aspect ratio locking"""
        if (self.aspect_ratio_check.get_active() and 
            original_width and original_height and
            spin.get_value() > 0 and
            self.height_spin.get_value() == 0):
            try:
                new_width = spin.get_value()
                new_height = int((new_width * original_height) / original_width)
                self.height_spin.handler_block_by_func(self.on_height_changed)
                self.height_spin.set_value(new_height)
                self.height_spin.handler_unblock_by_func(self.on_height_changed)
            except (ValueError, ZeroDivisionError):
                pass
    
    def on_height_changed(self, spin, original_width, original_height):
        """Handle height spin button changes with aspect ratio locking"""
        if (self.aspect_ratio_check.get_active() and 
            original_width and original_height and
            spin.get_value() > 0 and
            self.width_spin.get_value() == 0):
            try:
                new_height = spin.get_value()
                new_width = int((new_height * original_width) / original_height)
                self.width_spin.handler_block_by_func(self.on_width_changed)
                self.width_spin.set_value(new_width)
                self.width_spin.handler_unblock_by_func(self.on_width_changed)
            except (ValueError, ZeroDivisionError):
                pass
    
    def get_dimensions(self):
        """Get the current width and height values as integers"""
        try:
            width_value = self.width_spin.get_value()
            height_value = self.height_spin.get_value()
            
            width = int(width_value) if width_value > 0 else None
            height = int(height_value) if height_value > 0 else None
            
            return width, height
        except (ValueError, TypeError):
            return None, None
    
    def clear_dimensions(self):
        """Clear both spin buttons"""
        self.width_spin.set_value(0)
        self.height_spin.set_value(0)
        
class OutputSection:
    """Section for output format configuration"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.widget, self.format_combo = self.create_widget()
    
    def create_widget(self):
        """Create the output format widget"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        
        # Format selection
        format_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        format_label = Gtk.Label(label="Output format:")
        format_label.set_size_request(100, -1)
        
        format_combo = Gtk.DropDown.new_from_strings([
            "Same as original",
            "PNG",
            "JPEG", 
            "WebP"
        ])
        format_combo.set_selected(0)
        
        format_box.append(format_label)
        format_box.append(format_combo)
        main_box.append(format_box)
        
        return main_box, format_combo
    
    def on_format_changed(self, combo, pspec, file_path):
        """Handle output format changes"""
        # Format change doesn't affect anything until save dialog
        pass
    
    def generate_default_output_path(self):
        """Generate default output path based on current settings"""
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        format_index = self.format_combo.get_selected()
        format_ext = [None, '.png', '.jpg', '.webp'][format_index]
        
        if format_ext:
            new_name = f"{base_name}_resized{format_ext}"
        else:
            ext = os.path.splitext(self.file_path)[1]
            new_name = f"{base_name}_resized{ext}"
        
        original_dir = os.path.dirname(self.file_path)
        return os.path.join(original_dir, new_name)

class ButtonSection:
    """Section containing action buttons"""
    
    def __init__(self):
        self.widget, self.cancel_btn, self.resize_btn = self.create_widget()
    
    def create_widget(self):
        """Create the button widgets"""
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.END)
        
        cancel_btn = Gtk.Button.new_with_label("Cancel")
        resize_btn = Gtk.Button.new_with_label("Resize Image")
        resize_btn.add_css_class("suggested-action")
        
        button_box.append(cancel_btn)
        button_box.append(resize_btn)
        
        return button_box, cancel_btn, resize_btn
    
    def set_buttons_sensitive(self, sensitive):
        """Enable or disable buttons"""
        self.cancel_btn.set_sensitive(sensitive)
        self.resize_btn.set_sensitive(sensitive)
        
class ResizeOperation:
    """Handles the actual image resize operation"""
    
    @staticmethod
    def perform_resize(file_path, width, height, format_index, output_path, parent_window):
        """Perform the actual image resize operation and return success status"""
        # Validation
        if width is None and height is None:
            ResizeOperation.show_error('Please enter valid width and/or height values')
            return False
        
        if not output_path:
            ResizeOperation.show_error('No output file selected')
            return False
        
        # Build resize parameter
        resize_param = ResizeOperation.build_resize_param(width, height)
        
        # Prepare output
        if not ResizeOperation.prepare_output_directory(output_path):
            return False
        
        # Check for existing file
        if os.path.exists(output_path):
            # We can't show dialog from thread, so we'll overwrite by default
            # or could use a different approach for confirmation
            pass
        
        # Execute resize
        return ResizeOperation.execute_resize(file_path, resize_param, output_path, parent_window)
    
    @staticmethod
    def build_resize_param(width, height):
        """Build the ImageMagick resize parameter"""
        if width is not None and height is not None:
            return f"{width}x{height}"
        elif width is not None:
            return str(width)
        elif height is not None:
            return f"x{height}"
        return ""
    
    @staticmethod
    def prepare_output_directory(output_path):
        """Create output directory if it doesn't exist"""
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
                return True
            except OSError as e:
                ResizeOperation.show_error(f'Cannot create directory: {e}')
                return False
        return True
    
    @staticmethod
    def execute_resize(file_path, resize_param, output_path, parent_window):
        """Execute the ImageMagick resize command and return success status"""
        try:
            ResizeOperation.show_notification('Resizing', 'Image resize in progress...')
            
            print(f"Resizing {file_path} to {resize_param}, saving to {output_path}")
            
            # Use subprocess to run ImageMagick convert command
            result = subprocess.run(
                ['convert', file_path, '-resize', resize_param, output_path],
                capture_output=True, 
                timeout=30, 
                text=True
            )
            
            if result.returncode == 0:
                success_message = f'Resized successfully!\nSaved as: {os.path.basename(output_path)}'
                print(success_message)
                ResizeOperation.show_success(success_message)
                return True
            else:
                error_message = f'Resize failed. Return code: {result.returncode}\nError: {result.stderr}'
                print(error_message)
                ResizeOperation.show_error(error_message)
                return False
                
        except FileNotFoundError:
            error_msg = 'ImageMagick not installed. Run: sudo dnf install ImageMagick'
            print(error_msg)
            ResizeOperation.show_error(error_msg)
            return False
        except subprocess.TimeoutExpired:
            error_msg = 'Resize operation timed out'
            print(error_msg)
            ResizeOperation.show_error(error_msg)
            return False
        except Exception as e:
            error_msg = f'Resize failed: {str(e)}'
            print(error_msg)
            ResizeOperation.show_error(error_msg)
            return False
    
    @staticmethod
    def show_notification(title, message):
        """Show a desktop notification"""
        try:
            subprocess.run(['notify-send', title, message], capture_output=True, timeout=5)
        except:
            print(f"Notification: {title} - {message}")
    
    @staticmethod
    def show_error(message):
        """Show an error notification"""
        try:
            subprocess.run(['notify-send', 'Error', message], capture_output=True, timeout=5)
        except:
            print(f"Error: {message}")
    
    @staticmethod
    def show_success(message):
        """Show a success notification"""
        try:
            subprocess.run(['notify-send', 'Success', message], capture_output=True, timeout=5)
        except:
            print(f"Success: {message}")
            
def main():
    if len(sys.argv) != 2:
        return 1
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        return 1
    
    resizer = ImageResizer(file_path)
    return resizer.run()

if __name__ == '__main__':
    sys.exit(main())