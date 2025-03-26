from flask import Flask, render_template, request, jsonify
import requests
import time

app = Flask(__name__)
LIBRETRANSLATE_URL = "http://localhost:5000"

def is_service_ready():
    try:
        response = requests.get(f"{LIBRETRANSLATE_URL}/languages")
        return response.status_code == 200
    except:
        return False

@app.route('/')
def index():
    # Check if LibreTranslate service is ready
    if not is_service_ready():
        return render_template('loading.html')
    
    try:
        # Get available languages from LibreTranslate
        languages = requests.get(f"{LIBRETRANSLATE_URL}/languages").json()
        return render_template('index.html', languages=languages)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/check_status')
def check_status():
    return jsonify({"ready": is_service_ready()})

@app.route('/translate', methods=['POST'])
def translate():
    if not is_service_ready():
        return jsonify({"error": "Translation service is not ready yet"}), 503
        
    try:
        data = request.get_json()
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')

        # Call LibreTranslate API
        response = requests.post(f"{LIBRETRANSLATE_URL}/translate", json={
            "q": text,
            "source": source_lang,
            "target": target_lang
        })
        
        if response.status_code != 200:
            return jsonify({"error": "Translation service error"}), response.status_code
            
        translation = response.json()
        return jsonify({"translation": translation.get("translatedText", "")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8080, debug=True)
