# 🤖 JARVIS - Just A Rather Very Intelligent System

![JARVIS Banner](https://i.pinimg.com/736x/08/f1/af/08f1af0e594a9dca03135849cda51d1f.jpg)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](CONTRIBUTING.md)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Voice Commands](#voice-commands)
- [GUI Interface](#gui-interface)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

JARVIS is an advanced AI voice assistant built with Python, designed to provide a seamless and interactive experience for users. It combines natural language processing, voice recognition, and a modern GUI interface to create a powerful personal assistant that can help with various daily tasks.

## ✨ Features

### 🎯 Core Capabilities
- **Voice Recognition**: Natural language processing for voice commands
- **Text-to-Speech**: Clear and natural voice responses
- **Modern GUI**: Sleek, animated interface with real-time visualizations
- **System Integration**: Control system functions and applications
- **Web Integration**: Access to weather, news, and web searches
- **Mathematical Computing**: Advanced calculations using WolframAlpha
- **System Monitoring**: Real-time system resource monitoring

### 🔧 Technical Features
- Real-time voice visualization
- Dynamic GUI animations
- System resource monitoring
- Screenshot capabilities
- Internet speed testing
- Wikipedia integration
- Weather information
- News updates
- Application control
- File system navigation

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhisahu143/Jarvis0.2.git
cd Jarvis0.2
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys in `config.json`:
```json
{
    "apis": {
        "wolframalpha": "YOUR_WOLFRAM_ALPHA_KEY",
        "openweathermap": "YOUR_OPENWEATHERMAP_KEY",
        "newsapi": "YOUR_NEWS_API_KEY"
    }
}
```

## ⚙️ Configuration

The `config.json` file allows you to customize JARVIS:

```json
{
    "user": {
        "name": "Sir",
        "email": "",
        "password": ""
    },
    "paths": {
        "music": "",
        "documents": "",
        "downloads": ""
    },
    "preferences": {
        "voice_speed": 1.0,
        "language": "en",
        "temperature_unit": "celsius"
    }
}
```

## 🎮 Usage

1. Start JARVIS:
```bash
python jarvis.py
```

2. Use voice commands or the GUI interface to interact with JARVIS
3. The assistant will respond both verbally and through the GUI

## 🗣️ Voice Commands

### Basic Commands
- "Hello" / "Hi" - Greet JARVIS
- "What time is it?" - Get current time
- "What's the date?" - Get current date
- "Who are you?" - Learn about JARVIS

### System Commands
- "System information" - Get CPU, memory, and battery status
- "Take a screenshot" - Capture screen
- "Check internet speed" - Test connection speed

### Web Commands
- "Weather in [city]" - Get weather information
- "Search for [query]" - Web search
- "Tell me about [topic]" - Wikipedia search
- "Latest news" - Get news headlines

### Application Control
- "Open [application]" - Launch applications
- "Open [folder]" - Navigate to folders
- "Play music" - Control media playback

## 🖥️ GUI Interface

The GUI features:
- Real-time voice visualization
- Animated logo and particles
- Status indicators
- Quick command buttons
- Full-screen mode
- Dark theme with neon accents

## 🔬 Technical Details

### Architecture
- **Frontend**: Tkinter-based GUI with custom animations
- **Backend**: Python-based voice processing and command handling
- **APIs**: Integration with multiple external services
- **Audio**: Pygame for audio playback
- **Visualization**: Matplotlib for real-time graphs

### Key Components
- Voice recognition using SpeechRecognition
- Text-to-speech using gTTS
- System monitoring with psutil
- Web requests with requests
- GUI rendering with tkinter
- Data visualization with matplotlib

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the fictional JARVIS from Iron Man
- Built with Python and various open-source libraries
- Thanks to all contributors and users

---

<div align="center">
Made with ❤️ by [CodewithAbhi]
</div> 
