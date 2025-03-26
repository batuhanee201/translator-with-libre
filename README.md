# 🌐 Translator with LibreTranslate

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0.2-green.svg)](https://flask.palletsprojects.com/)
[![LibreTranslate](https://img.shields.io/badge/LibreTranslate-Docker-blue.svg)](https://github.com/LibreTranslate/LibreTranslate)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A powerful Windows desktop translator application that runs in the background and provides instant translations with just a hotkey. Built with Python, Flask, and LibreTranslate for privacy-focused, offline translation capabilities.

## ✨ Features

- 🔥 **Instant Translation**: Press Ctrl+3 to translate any selected text
- 🔒 **Privacy First**: Uses LibreTranslate for offline translations
- 💾 **Translation History**: Saves all translations with timestamps
- 📊 **Statistics**: Track your translation usage and patterns
- 🎯 **System Tray Integration**: Runs quietly in the background
- 🎨 **Modern UI**: Clean and intuitive interface
- 🌍 **Multiple Languages**: Support for various language pairs
- 📱 **Responsive Design**: Adapts to different screen sizes

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Docker (for LibreTranslate)
- Windows OS

### Installation

1. Clone the repository:
```bash
git clone https://github.com/hardchenry/translator-with-libre.git
cd translator-with-libre
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start LibreTranslate Docker container:
```bash
docker run -d -p 5000:5000 libretranslate/libretranslate
```

4. Run the application:
```bash
python translator_app.py
```

### Using the Standalone Executable

1. Download the latest release from the [releases page](https://github.com/hardchenry/translator-with-libre/releases)
2. Make sure Docker is running
3. Double-click `Translator.exe`
4. The app will start and minimize to system tray

## 🎮 Usage

1. **Start Translation**:
   - Select any text
   - Press `Ctrl+3`
   - A translation window will appear

2. **View History**:
   - Click the system tray icon
   - Select "Show History"
   - Browse your past translations

3. **Exit Application**:
   - Press `Ctrl+Q`
   - Or right-click the system tray icon and select "Exit"

## 🏗️ Project Structure

```
translator-with-libre/
├── app.py                 # Flask server for translation API
├── windows_extension.py   # Windows hotkey and clipboard handling
├── translator_app.py      # Main desktop application
├── translation_history.py # SQLite database management
├── translator_ui.py      # Modern UI components
├── templates/            # HTML templates
│   ├── index.html
│   ├── loading.html
│   └── error.html
└── requirements.txt      # Python dependencies
```

## 🛠️ Technical Details

- **Backend**: Flask web server + LibreTranslate
- **Frontend**: Tkinter for native Windows UI
- **Database**: SQLite for translation history
- **Packaging**: PyInstaller for standalone executable
- **System Integration**: Windows hotkeys and clipboard access

## 📊 Statistics Features

- Total translations count
- Daily translation usage
- Average text length
- Most used language pairs
- Translation history with timestamps

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate) for the amazing offline translation engine
- [Flask](https://flask.palletsprojects.com/) for the lightweight web framework
- All contributors and users of this project

---
