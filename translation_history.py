import sqlite3
from datetime import datetime
import os

class TranslationHistory:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'translations.db')
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT NOT NULL,
                    target_lang TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_translation(self, original_text, translated_text, source_lang="auto", target_lang="tr"):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO translations 
                (original_text, translated_text, source_lang, target_lang)
                VALUES (?, ?, ?, ?)
            ''', (original_text, translated_text, source_lang, target_lang))
            conn.commit()

    def get_recent_translations(self, limit=10):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT original_text, translated_text, timestamp
                FROM translations
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def get_statistics(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            stats = {}
            
            # Total translations
            cursor.execute('SELECT COUNT(*) FROM translations')
            stats['total_translations'] = cursor.fetchone()[0]
            
            # Translations today
            cursor.execute('''
                SELECT COUNT(*) FROM translations 
                WHERE date(timestamp) = date('now')
            ''')
            stats['translations_today'] = cursor.fetchone()[0]
            
            # Average length of original text
            cursor.execute('''
                SELECT AVG(LENGTH(original_text)) FROM translations
            ''')
            stats['avg_text_length'] = round(cursor.fetchone()[0] or 0, 2)
            
            return stats

    def clear_history(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM translations')
            conn.commit()
