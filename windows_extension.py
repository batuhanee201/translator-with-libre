import keyboard
import pyperclip
import requests
import time
import sys
from translation_history import TranslationHistory
from translator_ui import TranslatorUI

TRANSLATION_SERVER = "http://localhost:8080"
history_manager = TranslationHistory()
ui = TranslatorUI(history_manager)
running = True

def get_selected_text():
    # Save current clipboard content
    old_clipboard = pyperclip.paste()
    
    # Simulate Ctrl+C to copy selected text
    keyboard.send('ctrl+c')
    # Wait a bit for the clipboard to update
    time.sleep(0.1)
    
    # Get the text from clipboard
    text = pyperclip.paste()
    
    # Restore original clipboard content
    pyperclip.copy(old_clipboard)
    
    return text

def translate_text(text):
    try:
        response = requests.post(f"{TRANSLATION_SERVER}/translate", 
                               json={"text": text, "source_lang": "auto", "target_lang": "tr"})
        if response.status_code == 200:
            return response.json()["translation"]
        return "Translation error"
    except Exception as e:
        return f"Error: {str(e)}"

def on_hotkey():
    text = get_selected_text()
    if text.strip():
        translated = translate_text(text)
        ui.show_translation(text, translated)

def on_quit():
    global running
    running = False

def main():
    print("Translator extension started. Press Ctrl+3 to translate selected text.")
    print("Press Ctrl+Q to quit.")
    
    keyboard.add_hotkey('ctrl+3', on_hotkey)
    keyboard.add_hotkey('ctrl+q', on_quit)
    
    while running:
        time.sleep(0.1)

if __name__ == "__main__":
    main()
