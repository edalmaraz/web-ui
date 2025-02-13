import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import json
import subprocess
import platform
from pathlib import Path

class WebUILauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Web UI Launcher")
        
        # Set window size and make it non-resizable
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', padding=5)
        style.configure('TButton', padding=5)
        style.configure('TEntry', padding=5)
        
        self.create_variables()
        self.create_widgets()
        self.load_settings()
        
    def create_variables(self):
        # Network settings
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.port_var = tk.StringVar(value="7788")
        
        # Theme settings
        self.themes = [
            "Ocean", "Default", "Soft", "Monochrome",
            "Glass", "Origin", "Citrus"
        ]
        self.theme_var = tk.StringVar(value="Ocean")
        self.dark_mode_var = tk.BooleanVar(value=False)
        
        # Browser settings
        self.use_own_browser_var = tk.BooleanVar(value=False)
        self.keep_browser_open_var = tk.BooleanVar(value=False)
        
        # Path variables
        system = platform.system()
        if system == "Windows":
            default_chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            default_userdata = str(Path.home() / "AppData/Local/Google/Chrome/User Data")
        elif system == "Darwin":  # macOS
            default_chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            default_userdata = str(Path.home() / "Library/Application Support/Google/Chrome")
        else:  # Linux
            default_chrome = "/usr/bin/google-chrome"
            default_userdata = str(Path.home() / ".config/google-chrome")
            
        self.chrome_path_var = tk.StringVar(value=default_chrome)
        self.chrome_userdata_var = tk.StringVar(value=default_userdata)
        
    def create_widgets(self):
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Network Settings
        self.create_section_label(main_frame, "Network Settings")
        
        ip_frame = ttk.Frame(main_frame)
        ip_frame.pack(fill=tk.X, pady=2)
        ttk.Label(ip_frame, text="IP Address:").pack(side=tk.LEFT)
        ttk.Entry(ip_frame, textvariable=self.ip_var).pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        port_frame = ttk.Frame(main_frame)
        port_frame.pack(fill=tk.X, pady=2)
        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT)
        ttk.Entry(port_frame, textvariable=self.port_var).pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # Theme Settings
        self.create_section_label(main_frame, "Theme Settings")
        
        theme_frame = ttk.Frame(main_frame)
        theme_frame.pack(fill=tk.X, pady=2)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, values=self.themes)
        theme_combo.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        dark_mode_frame = ttk.Frame(main_frame)
        dark_mode_frame.pack(fill=tk.X, pady=2)
        ttk.Checkbutton(dark_mode_frame, text="Dark Mode", variable=self.dark_mode_var).pack(side=tk.LEFT)
        
        # Browser Settings
        self.create_section_label(main_frame, "Browser Settings")
        
        chrome_path_frame = ttk.Frame(main_frame)
        chrome_path_frame.pack(fill=tk.X, pady=2)
        ttk.Label(chrome_path_frame, text="Chrome Path:").pack(side=tk.LEFT)
        ttk.Entry(chrome_path_frame, textvariable=self.chrome_path_var).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(chrome_path_frame, text="Browse", command=lambda: self.browse_file(self.chrome_path_var)).pack(side=tk.RIGHT)
        
        userdata_frame = ttk.Frame(main_frame)
        userdata_frame.pack(fill=tk.X, pady=2)
        ttk.Label(userdata_frame, text="User Data:").pack(side=tk.LEFT)
        ttk.Entry(userdata_frame, textvariable=self.chrome_userdata_var).pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(userdata_frame, text="Browse", command=lambda: self.browse_directory(self.chrome_userdata_var)).pack(side=tk.RIGHT)
        
        browser_options_frame = ttk.Frame(main_frame)
        browser_options_frame.pack(fill=tk.X, pady=2)
        ttk.Checkbutton(browser_options_frame, text="Use Own Browser", variable=self.use_own_browser_var).pack(side=tk.LEFT)
        ttk.Checkbutton(browser_options_frame, text="Keep Browser Open", variable=self.keep_browser_open_var).pack(side=tk.LEFT)
        
        # Preview Command
        self.create_section_label(main_frame, "Launch Command Preview")
        
        self.preview_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.preview_text.pack(fill=tk.X, pady=5)
        
        # Action Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Launch", command=self.launch_webui).pack(side=tk.RIGHT, padx=5)
        
        # Bind events for live preview updates
        for var in [self.ip_var, self.port_var, self.theme_var, self.dark_mode_var,
                   self.chrome_path_var, self.chrome_userdata_var,
                   self.use_own_browser_var, self.keep_browser_open_var]:
            var.trace_add('write', lambda *args: self.update_preview())
            
        self.update_preview()
        
    def create_section_label(self, parent, text):
        ttk.Label(parent, text=text, font=('TkDefaultFont', 10, 'bold')).pack(fill=tk.X, pady=(10,5))
        
    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)
            
    def browse_directory(self, var):
        directory = filedialog.askdirectory()
        if directory:
            var.set(directory)
            
    def update_preview(self):
        cmd = ["python", "webui.py"]
        
        # Add network options
        cmd.extend(["--ip", self.ip_var.get()])
        cmd.extend(["--port", self.port_var.get()])
        
        # Add theme options
        if self.theme_var.get() != "Ocean":
            cmd.extend(["--theme", self.theme_var.get()])
        
        if self.dark_mode_var.get():
            cmd.append("--dark-mode")
            
        # Preview environment variables
        env_vars = []
        if self.use_own_browser_var.get():
            env_vars.extend([
                f'CHROME_PATH="{self.chrome_path_var.get()}"',
                f'CHROME_USER_DATA="{self.chrome_userdata_var.get()}"'
            ])
        
        if self.keep_browser_open_var.get():
            env_vars.append('CHROME_PERSISTENT_SESSION=true')
            
        # Update preview text
        preview = ""
        if env_vars:
            preview += "Environment Variables:\n" + "\n".join(env_vars) + "\n\n"
        preview += "Launch Command:\n" + " ".join(cmd)
        
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(tk.END, preview)
        
    def save_settings(self):
        settings = {
            'ip': self.ip_var.get(),
            'port': self.port_var.get(),
            'theme': self.theme_var.get(),
            'dark_mode': self.dark_mode_var.get(),
            'chrome_path': self.chrome_path_var.get(),
            'chrome_userdata': self.chrome_userdata_var.get(),
            'use_own_browser': self.use_own_browser_var.get(),
            'keep_browser_open': self.keep_browser_open_var.get()
        }
        
        try:
            with open('launcher_settings.json', 'w') as f:
                json.dump(settings, f, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            
    def load_settings(self):
        try:
            if os.path.exists('launcher_settings.json'):
                with open('launcher_settings.json', 'r') as f:
                    settings = json.load(f)
                    
                self.ip_var.set(settings.get('ip', "127.0.0.1"))
                self.port_var.set(settings.get('port', "7788"))
                self.theme_var.set(settings.get('theme', "Ocean"))
                self.dark_mode_var.set(settings.get('dark_mode', False))
                self.chrome_path_var.set(settings.get('chrome_path', ""))
                self.chrome_userdata_var.set(settings.get('chrome_userdata', ""))
                self.use_own_browser_var.set(settings.get('use_own_browser', False))
                self.keep_browser_open_var.set(settings.get('keep_browser_open', False))
        except Exception as e:
            messagebox.showwarning("Warning", f"Failed to load settings: {str(e)}")
            
    def launch_webui(self):
        try:
            # Prepare environment variables
            env = os.environ.copy()
            
            if self.use_own_browser_var.get():
                env['CHROME_PATH'] = self.chrome_path_var.get()
                env['CHROME_USER_DATA'] = self.chrome_userdata_var.get()
                
            if self.keep_browser_open_var.get():
                env['CHROME_PERSISTENT_SESSION'] = 'true'
                
            # Prepare command
            cmd = [sys.executable, "webui.py",
                  "--ip", self.ip_var.get(),
                  "--port", self.port_var.get()]
            
            if self.theme_var.get() != "Ocean":
                cmd.extend(["--theme", self.theme_var.get()])
                
            if self.dark_mode_var.get():
                cmd.append("--dark-mode")
                
            # Launch WebUI
            subprocess.Popen(cmd, env=env)
            
            # Save settings
            self.save_settings()
            
            # Close launcher
            self.root.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch WebUI: {str(e)}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    launcher = WebUILauncher()
    launcher.run()
