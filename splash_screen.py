"""
OptiBlink Splash Screen Module
Displays a splash screen with the OptiBlink logo during application startup.
"""

import tkinter as tk
from tkinter import ttk
import os
import sys
import threading
import time
from PIL import Image, ImageTk

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SplashScreen:
    def __init__(self, duration=3.0):
        """
        Initialize splash screen
        
        Args:
            duration (float): How long to show the splash screen in seconds
        """
        self.duration = duration
        self.root = None
        self.progress_var = None
        self.progress_bar = None
        self.status_label = None
        
    def create_splash(self):
        """Create and configure the splash screen window"""
        self.root = tk.Tk()
        self.root.title("OptiBlink")
        
        # Remove window decorations and make it stay on top
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        # Set window size and center it
        width = 500
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configure background
        self.root.configure(bg='white')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Try to load and display the logo
        try:
            # Convert ICO to displayable format
            logo_path = resource_path("optiblink-logo.ico")
            if os.path.exists(logo_path):
                # Load the ICO file and convert to PhotoImage
                pil_image = Image.open(logo_path)
                # Resize if needed (keep aspect ratio)
                pil_image = pil_image.resize((120, 120), Image.Resampling.LANCZOS)
                logo_image = ImageTk.PhotoImage(pil_image)
                
                logo_label = tk.Label(main_frame, image=logo_image, bg='white')
                logo_label.image = logo_image  # Keep a reference
                logo_label.pack(pady=(20, 10))
            else:
                # Fallback if logo not found
                logo_label = tk.Label(main_frame, text="🔍", font=('Arial', 48), 
                                    fg='#3498db', bg='white')
                logo_label.pack(pady=(20, 10))
        except Exception as e:
            # Fallback if image loading fails
            logo_label = tk.Label(main_frame, text="🔍", font=('Arial', 48), 
                                fg='#3498db', bg='white')
            logo_label.pack(pady=(20, 10))
        
        # Application name
        title_label = tk.Label(main_frame, text="OptiBlink", 
                             font=('Arial', 24, 'bold'), 
                             fg='#2c3e50', bg='white')
        title_label.pack(pady=(0, 5))
        
        # Subtitle
        subtitle_label = tk.Label(main_frame, text="Eye Tracking & Blink Detection", 
                                font=('Arial', 12), 
                                fg='#34495e', bg='white')
        subtitle_label.pack(pady=(0, 20))
        
        # Loading label
        loading_label = tk.Label(main_frame, text="Loading Progress:", 
                               font=('Arial', 10, 'bold'), 
                               fg='#2c3e50', bg='white')
        loading_label.pack(pady=(10, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        
        # Create a custom style for purple progress bar
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better customization
        style.configure("Purple.Horizontal.TProgressbar",
                       background='#8e44ad',  # Purple color
                       troughcolor='#ecf0f1',  # Light gray background
                       borderwidth=2,
                       relief='solid',
                       lightcolor='#9b59b6',  # Lighter purple
                       darkcolor='#7d3c98')   # Darker purple
        
        self.progress_bar = ttk.Progressbar(main_frame, 
                                          variable=self.progress_var,
                                          maximum=100,
                                          length=400,
                                          mode='determinate',
                                          style="Purple.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=(20, 10))
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Initializing...", 
                                   font=('Arial', 12, 'bold'), 
                                   fg='#000000', bg='white',
                                   width=40, height=3)  # Fixed width and height
        self.status_label.pack(pady=(15, 20))
        
        # Version info
        version_label = tk.Label(main_frame, text="v1.0", 
                               font=('Arial', 8), 
                               fg='#95a5a6', bg='white')
        version_label.pack(side='bottom', pady=(10, 0))
        
        return self.root
    
    def update_progress(self, value, status_text=""):
        """Update progress bar and status text"""
        if self.progress_var and self.status_label and self.root:
            try:
                self.progress_var.set(value)
                if status_text:
                    # Force text update with multiple methods
                    self.status_label.config(text=status_text)
                    self.status_label.update()
                self.root.update_idletasks()
                self.root.update()
            except Exception as e:
                print(f"Error updating progress: {e}")
    
    def show_splash(self, callback=None):
        """
        Show the splash screen with animated progress
        
        Args:
            callback: Function to call when splash screen is done
        """
        if not self.root:
            self.create_splash()
        
        # Show the window
        self.root.deiconify()
        self.root.update()
        
        # Animate progress
        steps = [
            (10, "Loading modules..."),
            (25, "Initializing camera..."),
            (40, "Loading AI models..."),
            (60, "Setting up eye tracking..."),
            (80, "Configuring interface..."),
            (95, "Finalizing setup..."),
            (100, "Ready!")
        ]
        
        step_duration = self.duration / len(steps)
        
        for progress, status in steps:
            print(f"Updating progress: {progress}% - {status}")  # Debug output
            self.update_progress(progress, status)
            time.sleep(step_duration)
        
        # Keep final state visible briefly
        time.sleep(0.5)
        
        # Close splash screen
        self.close_splash()
        
        # Call callback if provided
        if callback:
            callback()
    
    def close_splash(self):
        """Close the splash screen"""
        if self.root:
            self.root.destroy()
            self.root = None

def show_splash_screen(duration=3.0, callback=None):

    splash = SplashScreen(duration)
    splash.show_splash(callback)

def show_splash_screen_threaded(duration=3.0, callback=None):
    """
    Show splash screen in a separate thread (non-blocking)
    
    Args:
        duration (float): Duration in seconds
        callback: Function to call when done
    """
    def run_splash():
        splash = SplashScreen(duration)
        splash.show_splash(callback)
    
    thread = threading.Thread(target=run_splash, daemon=True)
    thread.start()
    return thread

def show_emergency_contact_dialog():
    """
    Show a dialog window asking for user's emergency contact
    
    Returns:
        dict: Contains 'contact' and 'whatsapp_preference' or None if cancelled
    """
    import tkinter as tk
    from tkinter import messagebox, simpledialog
    
    # Create main dialog window
    dialog = tk.Tk()
    dialog.title("Emergency Contact Setup")
    dialog.geometry("450x550")
    dialog.resizable(False, False)
    
    # Center the window
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    x = (screen_width - 450) // 2
    y = (screen_height - 550) // 2
    dialog.geometry(f"450x550+{x}+{y}")
    
    # Configure background
    dialog.configure(bg='white')
    dialog.attributes('-topmost', True)
    
    # Result storage
    result = {'contact': '', 'whatsapp_preference': False, 'cancelled': True}
    
    # Main frame
    main_frame = tk.Frame(dialog, bg='white', padx=30, pady=15)
    main_frame.pack(expand=True, fill='both')
    
    # Logo
    try:
        # Load and display the OptiBlink logo
        logo_path = resource_path("optiblink-logo.ico")
        if os.path.exists(logo_path):
            # Load the ICO file and convert to PhotoImage
            pil_image = Image.open(logo_path)
            # Resize for dialog (smaller than splash screen)
            pil_image = pil_image.resize((80, 80), Image.Resampling.LANCZOS)
            logo_image = ImageTk.PhotoImage(pil_image)
            
            logo_label = tk.Label(main_frame, image=logo_image, bg='white')
            logo_label.image = logo_image  # Keep a reference
            logo_label.pack(pady=(10, 15))
        else:
            # Fallback if logo not found
            logo_label = tk.Label(main_frame, text="🔍", font=('Arial', 32), 
                                fg='#3498db', bg='white')
            logo_label.pack(pady=(10, 15))
    except Exception as e:
        # Fallback if image loading fails
        logo_label = tk.Label(main_frame, text="🔍", font=('Arial', 32), 
                            fg='#3498db', bg='white')
        logo_label.pack(pady=(10, 15))
    
    # Title
    title_label = tk.Label(main_frame, text="Welcome to OptiBlink.\nEmergency Contact Setup", 
                          font=('Arial', 16, 'bold'), 
                          fg='#2c3e50', bg='white')
    title_label.pack(pady=(0, 10))
    
    # Description
    desc_label = tk.Label(main_frame, 
                         text="OptiBlink can send emergency alerts when needed.\nPlease provide your emergency contact information.", 
                         font=('Arial', 10), 
                         fg='#34495e', bg='white',
                         justify='center')
    desc_label.pack(pady=(0, 20))
    
    # Phone number frame
    phone_frame = tk.Frame(main_frame, bg='white')
    phone_frame.pack(fill='x', pady=(0, 15))
    
    phone_label = tk.Label(phone_frame, text="Emergency Contact Number:", 
                          font=('Arial', 10, 'bold'), 
                          fg='#2c3e50', bg='white')
    phone_label.pack(anchor='w')
    
    phone_entry = tk.Entry(phone_frame, font=('Arial', 11), width=30, relief='solid', bd=1)
    phone_entry.pack(fill='x', pady=(5, 0))
    phone_entry.insert(0, "+91 ")  # Default country code
    
    # Example text
    example_label = tk.Label(phone_frame, text="Example: +91 9876543210", 
                            font=('Arial', 9), 
                            fg='#7f8c8d', bg='white')
    example_label.pack(anchor='w', pady=(2, 0))
    
    # WhatsApp preference frame
    whatsapp_frame = tk.Frame(main_frame, bg='white')
    whatsapp_frame.pack(fill='x', pady=(10, 20))
    
    whatsapp_var = tk.BooleanVar()
    whatsapp_check = tk.Checkbutton(whatsapp_frame, 
                                   text="Prefer WhatsApp Web for emergency alerts", 
                                   variable=whatsapp_var,
                                   font=('Arial', 10), 
                                   fg='#2c3e50', bg='white',
                                   activebackground='white')
    whatsapp_check.pack(anchor='w')
    
    # Button frame
    button_frame = tk.Frame(main_frame, bg='white')
    button_frame.pack(side='bottom', fill='x', pady=(20, 10))
    
    def ok_proceed():
        contact = phone_entry.get().strip()
        if len(contact) < 10:
            messagebox.showerror("Invalid Contact", "Please enter a valid phone number with at least 10 digits.")
            return
        
        result['contact'] = contact
        result['whatsapp_preference'] = whatsapp_var.get()
        result['cancelled'] = False
        dialog.destroy()
    
    def cancel_close():
        result['cancelled'] = True
        dialog.destroy()
    
    # Buttons
    ok_btn = tk.Button(button_frame, text="OK", 
                      command=ok_proceed,
                      font=('Arial', 10, 'bold'),
                      bg='white', fg='black',
                      relief='solid', bd=1,
                      highlightbackground='#27ae60',
                      padx=30, pady=8,
                      cursor='hand2')
    ok_btn.pack(side='right', padx=(10, 0))
    
    cancel_btn = tk.Button(button_frame, text="Cancel", 
                          command=cancel_close,
                          font=('Arial', 10,'bold'),
                          bg='white', fg='black',
                          relief='solid', bd=1,
                          highlightbackground='#e74c3c',
                          padx=30, pady=8,
                          cursor='hand2')
    cancel_btn.pack(side='right')
    
    # Focus on phone entry
    phone_entry.focus_set()
    phone_entry.selection_range(len(phone_entry.get()), len(phone_entry.get()))  # Move cursor to end
    
    # Handle window close
    def on_closing():
        result['cancelled'] = True
        dialog.destroy()
    
    dialog.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Run dialog
    dialog.mainloop()
    
    return result if not result['cancelled'] else None

if __name__ == "__main__":
    # Test the splash screen
    show_splash_screen(duration=3.0)
    
