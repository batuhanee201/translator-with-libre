# Local Translator App

A Python-based translator application using LibreTranslate locally.

## Setup Instructions

1. Install LibreTranslate locally:
   ```
   docker pull libretranslate/libretranslate
   ```

2. Run LibreTranslate container:
   ```
   docker run -t -p 5000:5000 libretranslate/libretranslate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

The web interface will be available at http://localhost:8080
