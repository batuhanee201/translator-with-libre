import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import json
from datetime import datetime

class TranslatorUI:
    def __init__(self, history_manager):
        self.history = history_manager
        self.root = None

    def show_translation(self, text, translated_text, source_lang="auto", target_lang="tr"):
        if self.root is not None:
            try:
                self.root.destroy()
            except:
                pass

        self.root = tk.Tk()
        self.root.title("Translator")
        self.root.configure(bg='#f0f0f0')
        
        # Save translation to history
        self.history.add_translation(text, translated_text, source_lang, target_lang)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure styles
        style = ttk.Style()
        style.configure("Title.TLabel", font=('Helvetica', 12, 'bold'), padding=5)
        style.configure("Text.TLabel", font=('Helvetica', 10), padding=5)
        style.configure("Stats.TLabel", font=('Helvetica', 9), foreground='#666666')
        
        # Original text section
        ttk.Label(main_frame, text="Original Text", style="Title.TLabel").grid(row=0, column=0, sticky=tk.W)
        text_frame = ttk.Frame(main_frame, relief='solid', padding=5)
        text_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(text_frame, text=text, wraplength=300, style="Text.TLabel").grid(row=0, column=0)
        
        # Translation section
        ttk.Label(main_frame, text="Translation", style="Title.TLabel").grid(row=2, column=0, sticky=tk.W)
        trans_frame = ttk.Frame(main_frame, relief='solid', padding=5)
        trans_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Label(trans_frame, text=translated_text, wraplength=300, style="Text.TLabel").grid(row=0, column=0)
        
        # Statistics section
        stats = self.history.get_statistics()
        stats_frame = ttk.Frame(main_frame)
        stats_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        stats_text = f"Total translations: {stats['total_translations']} | "
        stats_text += f"Today: {stats['translations_today']} | "
        stats_text += f"Avg. length: {stats['avg_text_length']}"
        
        ttk.Label(stats_frame, text=stats_text, style="Stats.TLabel").grid(row=0, column=0)
        
        # Recent translations button
        ttk.Button(main_frame, text="Show Recent Translations", 
                  command=self.show_history_window).grid(row=5, column=0, pady=10)
        
        # Close button
        ttk.Button(main_frame, text="Close", 
                  command=self.root.destroy).grid(row=6, column=0, pady=5)
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - width) // 2
        y = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f'+{x}+{y}')
        
        # Set window on top
        self.root.attributes('-topmost', True)
        self.root.mainloop()

    def show_history_window(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Recent Translations")
        history_window.configure(bg='#f0f0f0')
        
        # Configure styles
        style = ttk.Style()
        style.configure("History.TLabel", font=('Helvetica', 9), padding=3)
        
        # Create main frame
        main_frame = ttk.Frame(history_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add title
        ttk.Label(main_frame, text="Recent Translations", 
                 style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Get recent translations
        recent = self.history.get_recent_translations()
        
        # Add headers
        ttk.Label(main_frame, text="Original", style="Title.TLabel").grid(row=1, column=0, padx=5)
        ttk.Label(main_frame, text="Translation", style="Title.TLabel").grid(row=1, column=1, padx=5)
        
        # Add translations
        for i, (orig, trans, timestamp) in enumerate(recent, start=2):
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            time_str = dt.strftime('%Y-%m-%d %H:%M')
            
            frame = ttk.Frame(main_frame, relief='solid', padding=2)
            frame.grid(row=i, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=2)
            
            ttk.Label(frame, text=f"{time_str}\n{orig}", 
                     wraplength=200, style="History.TLabel").grid(row=0, column=0, padx=5)
            ttk.Label(frame, text=f"\n{trans}", 
                     wraplength=200, style="History.TLabel").grid(row=0, column=1, padx=5)
        
        # Center window
        history_window.update_idletasks()
        width = history_window.winfo_width()
        height = history_window.winfo_height()
        x = (history_window.winfo_screenwidth() - width) // 2
        y = (history_window.winfo_screenheight() - height) // 2
        history_window.geometry(f'+{x}+{y}')
        
        history_window.attributes('-topmost', True)
        
        # Close button
        ttk.Button(main_frame, text="Close", 
                  command=history_window.destroy).grid(row=len(recent)+2, column=0, columnspan=2, pady=10)
