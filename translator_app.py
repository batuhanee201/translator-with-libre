import sys
import os
import keyboard
import requests
import threading
import time
from translation_history import TranslationHistory
from translator_ui import TranslatorUI
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import signal
import atexit

class TranslatorApp:
    def __init__(self):
        self.flask_process = None
        self.libretranslate_process = None
        self.history_manager = TranslationHistory()
        self.ui = TranslatorUI(self.history_manager)
        self.running = True
        self.root = tk.Tk()
        self.setup_ui()
        self.start_services()
        self.setup_hotkeys()

    def setup_ui(self):
        self.root.title("Translator")
        self.root.geometry("300x400")
        self.root.iconify()  # Minimize window
        
        # System tray icon
        self.create_system_tray()
        
        # Hide the main window
        self.root.withdraw()

    def create_system_tray(self):
        # Add system tray icon and menu
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.menu_frame, text="Translator is running in background").pack(pady=10)
        ttk.Label(self.menu_frame, text="Press Ctrl+3 to translate selected text").pack(pady=5)
        ttk.Button(self.menu_frame, text="Show History", command=self.show_history).pack(pady=5)
        ttk.Button(self.menu_frame, text="Exit", command=self.quit_app).pack(pady=5)

    def start_services(self):
        try:
            # Start LibreTranslate
            libretranslate_cmd = "docker run -d -p 5000:5000 libretranslate/libretranslate"
            self.libretranslate_process = subprocess.Popen(
                libretranslate_cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            # Start Flask server
            flask_cmd = f"python {os.path.join(os.path.dirname(__file__), 'app.py')}"
            self.flask_process = subprocess.Popen(
                flask_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for services to start
            time.sleep(5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start services: {str(e)}")
            self.quit_app()

    def setup_hotkeys(self):
        keyboard.add_hotkey('ctrl+3', self.translate_selected)
        keyboard.add_hotkey('ctrl+q', self.quit_app)

    def translate_selected(self):
        # Save current clipboard content
        import pyperclip
        old_clipboard = pyperclip.paste()
        
        # Get selected text
        keyboard.send('ctrl+c')
        time.sleep(0.1)
        text = pyperclip.paste()
        
        # Restore clipboard
        pyperclip.copy(old_clipboard)
        
        if text.strip():
            try:
                # Translate text
                response = requests.post(
                    "http://localhost:8080/translate",
                    json={"text": text, "source_lang": "auto", "target_lang": "tr"}
                )
                if response.status_code == 200:
                    translated = response.json()["translation"]
                    self.ui.show_translation(text, translated)
                else:
                    messagebox.showerror("Error", "Translation failed")
            except Exception as e:
                messagebox.showerror("Error", f"Translation error: {str(e)}")

    def show_history(self):
        self.ui.show_history_window()

    def quit_app(self):
        self.running = False
        
        # Stop services
        if self.flask_process:
            self.flask_process.terminate()
        if self.libretranslate_process:
            self.libretranslate_process.terminate()
        
        # Stop Docker container
        try:
            subprocess.run("docker stop $(docker ps -q --filter ancestor=libretranslate/libretranslate)", 
                         shell=True, check=False)
        except:
            pass
        
        self.root.quit()
        self.root.destroy()
        os._exit(0)

    def run(self):
        # Register cleanup
        atexit.register(self.quit_app)
        
        # Start main loop
        self.root.protocol("WM_DELETE_WINDOW", self.root.iconify)
        self.root.mainloop()

def main():
    app = TranslatorApp()
    app.run()

if __name__ == "__main__":
    main()
