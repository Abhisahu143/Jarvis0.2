"""
JARVIS - Just A Rather Very Intelligent System
A professional voice assistant with advanced features and natural language processing.
"""

import sys
import os
import json
import time
import datetime
import logging
import random
import webbrowser
import requests
import wikipedia
import pyautogui
import psutil
import speedtest
import wolframalpha
from pathlib import Path
from typing import Optional, Dict, Any
from gtts import gTTS
import pygame
import speech_recognition as sr
import tempfile
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import math
import threading
from tkinter import font as tkfont
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cv2
from scipy import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)

# Initialize pygame mixer
pygame.mixer.init()

class Jarvis:
    def __init__(self):
        """Initialize Jarvis with configuration and settings"""
        self.name = "Jarvis"
        self.user = "Sir"
        self.recognizer = sr.Recognizer()
        self.load_config()
        self.setup_apis()
        self.commands = self.load_commands()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
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
                "apis": {
                    "wolframalpha": "",
                    "openweathermap": "",
                    "newsapi": ""
                },
                "preferences": {
                    "voice_speed": 1.0,
                    "language": "en",
                    "temperature_unit": "celsius"
                }
            }
            self.save_config()
            print("Created default config.json. Please update it with your settings.")
    
    def save_config(self):
        """Save configuration to config.json"""
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def setup_apis(self):
        """Initialize API clients"""
        try:
            self.wolfram_client = wolframalpha.Client(self.config['apis']['wolframalpha'])
        except:
            self.wolfram_client = None
            logging.warning("WolframAlpha API not configured")

    def load_commands(self) -> Dict[str, Any]:
        """Load command definitions"""
        return {
            'greeting': ['hello', 'hi', 'hey', 'greetings'],
            'farewell': ['bye', 'goodbye', 'see you', 'exit', 'quit'],
            'time': ['time', 'what time', 'current time'],
            'date': ['date', 'what date', 'current date', 'day'],
            'weather': ['weather', 'temperature', 'forecast'],
            'search': ['search', 'look up', 'find', 'google'],
            'wikipedia': ['wikipedia', 'wiki', 'who is', 'what is'],
            'system': ['cpu', 'memory', 'battery', 'system'],
            'music': ['play music', 'play song', 'music'],
            'volume': ['volume up', 'volume down', 'mute'],
            'screenshot': ['screenshot', 'capture screen'],
            'reminder': ['remind me', 'set reminder', 'reminder'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'news': ['news', 'headlines', 'latest news'],
            'email': ['email', 'send email', 'check email'],
            'calculator': ['calculate', 'math', 'solve'],
            'translate': ['translate', 'translation'],
            'speedtest': ['speed test', 'internet speed', 'connection speed'],
            'open': ['open', 'launch', 'start', 'run'],
            'identity': ['who are you', 'what is your name', 'tell me about yourself', 'what can you do'],
            'user_identity': ['what is my name', 'who am i', 'what do you call me']
        }

    def speak(self, text: str) -> None:
        """Convert text to speech using gTTS and play with pygame"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name
            
            tts = gTTS(text=text, lang=self.config['preferences']['language'])
            tts.save(temp_filename)
            
            # Play audio using pygame
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_filename)
            
        except Exception as e:
            logging.error(f"Error in speech synthesis: {e}")
            print(f"Error in speech synthesis: {e}")

    def listen(self) -> Optional[str]:
        """Listen for user input and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language=self.config['preferences']['language'])
            print(f"User said: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            logging.error(f"Error in speech recognition: {e}")
            return None

    def get_time(self) -> str:
        """Get current time in a natural format"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def get_date(self) -> str:
        """Get current date in a natural format"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"

    def get_weather(self, city: str) -> str:
        """Get weather information for a city"""
        try:
            api_key = self.config['apis']['openweathermap']
            if not api_key:
                return "Weather API not configured. Please update config.json"
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                
                return f"The temperature in {city} is {temp}°C with {desc}. Humidity is {humidity}% and wind speed is {wind} m/s"
            return "Sorry, I couldn't get the weather information."
        except Exception as e:
            logging.error(f"Error getting weather: {e}")
            return "Sorry, I couldn't get the weather information."

    def get_system_info(self) -> str:
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            battery = psutil.sensors_battery()
            
            info = f"CPU usage is {cpu_percent}%. "
            info += f"Memory usage is {memory.percent}%. "
            
            if battery:
                info += f"Battery is at {battery.percent}%"
                if battery.power_plugged:
                    info += " and charging"
            else:
                info += "Battery information not available"
                
            return info
        except Exception as e:
            logging.error(f"Error getting system info: {e}")
            return "Sorry, I couldn't get the system information"

    def get_news(self) -> str:
        """Get latest news headlines"""
        try:
            api_key = self.config['apis']['newsapi']
            if not api_key:
                return "News API not configured. Please update config.json"
                
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url)
            news = response.json()
            
            if news["status"] == "ok":
                headlines = [article["title"] for article in news["articles"][:5]]
                return "Here are the top headlines: " + ". ".join(headlines)
            return "Sorry, I couldn't get the news"
        except Exception as e:
            logging.error(f"Error getting news: {e}")
            return "Sorry, I couldn't get the news"

    def calculate(self, query: str) -> str:
        """Calculate mathematical expressions"""
        try:
            if self.wolfram_client:
                res = self.wolfram_client.query(query)
                return next(res.results).text
            return "Calculator API not configured"
        except Exception as e:
            logging.error(f"Error in calculation: {e}")
            return "Sorry, I couldn't perform that calculation"

    def take_screenshot(self) -> str:
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return "Sorry, I couldn't take a screenshot"

    def check_internet_speed(self) -> str:
        """Check internet connection speed"""
        try:
            st = speedtest.Speedtest()
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000
            return f"Download speed is {download:.2f} Mbps and upload speed is {upload:.2f} Mbps"
        except Exception as e:
            logging.error(f"Error checking internet speed: {e}")
            return "Sorry, I couldn't check the internet speed"

    def process_command(self, query: str) -> None:
        """Process user commands"""
        if not query:
            return

        # Check for identity questions
        if any(word in query for word in self.commands['identity']):
            self.speak(f"I am {self.name}, your personal AI assistant. I can help you with various tasks like checking the weather, "
                      f"opening applications, searching the web, getting system information, and much more. "
                      f"I'm here to make your life easier and more efficient.")
            return

        # Check for user identity questions
        if any(word in query for word in self.commands['user_identity']):
            self.speak(f"You are {self.user}, my user and friend. I'm here to assist you with your daily tasks.")
            return

        # Check for greetings
        if any(word in query for word in self.commands['greeting']):
            self.speak(f"Hello {self.user}, how can I help you?")
            return

        # Check for farewell
        if any(word in query for word in self.commands['farewell']):
            self.speak(f"Goodbye {self.user}, have a great day!")
            sys.exit(0)

        # Time related
        if any(word in query for word in self.commands['time']):
            self.speak(self.get_time())
            return

        # Date related
        if any(word in query for word in self.commands['date']):
            self.speak(self.get_date())
            return

        # Weather related
        if any(word in query for word in self.commands['weather']):
            city = query.replace("weather in", "").replace("weather", "").strip()
            if city:
                self.speak(self.get_weather(city))
            else:
                self.speak("Please specify a city")
            return

        # System information
        if any(word in query for word in self.commands['system']):
            self.speak(self.get_system_info())
            return

        # News
        if any(word in query for word in self.commands['news']):
            self.speak(self.get_news())
            return

        # Calculator
        if any(word in query for word in self.commands['calculator']):
            self.speak(self.calculate(query))
            return

        # Screenshot
        if any(word in query for word in self.commands['screenshot']):
            self.speak(self.take_screenshot())
            return

        # Internet speed
        if any(word in query for word in self.commands['speedtest']):
            self.speak(self.check_internet_speed())
            return

        # Wikipedia search
        if any(word in query for word in self.commands['wikipedia']):
            try:
                query = query.replace("wikipedia", "").replace("wiki", "").strip()
                self.speak(f"Searching Wikipedia for {query}")
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            except Exception as e:
                logging.error(f"Error searching Wikipedia: {e}")
                self.speak("Sorry, I couldn't find that information")
            return

        # Web search
        if any(word in query for word in self.commands['search']):
            query = query.replace("search", "").replace("look up", "").strip()
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            self.speak(f"Searching for {query}")
            return

        # Application launching with enhanced support
        if any(word in query for word in self.commands['open']):
            app_name = query.split()[-1].strip().lower()
            try:
                # Common Windows applications
                common_apps = {
                    'notepad': 'notepad',
                    'calculator': 'calc',
                    'paint': 'mspaint',
                    'word': 'winword',
                    'excel': 'excel',
                    'powerpoint': 'powerpnt',
                    'outlook': 'outlook',
                    'cmd': 'cmd',
                    'powershell': 'powershell',
                    'task manager': 'taskmgr',
                    'control panel': 'control',
                    'settings': 'ms-settings:',
                    'file explorer': 'explorer',
                    'browser': 'start microsoft-edge:',
                    'edge': 'start  microsoft-edge:',
                    'chrome': 'start chrome',
                    'firefox': 'start firefox',
                    'opera': 'start opera',
                    'brave': 'start brave',
                    'vscode': 'code',
                    'visual studio code': 'code',
                    'terminal': 'wt',
                    'windows terminal': 'wt',
                    'photos': 'ms-photos:',
                    'camera': 'start microsoft.windows.camera:',
                    'store': 'ms-windows-store:',
                    'mail': 'start outlookmail:',
                    'calendar': 'outlookcal:',
                    'maps': 'bingmaps:',
                    'weather': 'msnweather:',
                    'news': 'msnnews:',
                    'sports': 'msnsports:',
                    'money': 'msnmoney:',
                    'music': 'mswindowsmusic:',
                    'movies': 'mswindowsvideo:',
                    'photoshop': 'photoshop',
                    'illustrator': 'illustrator',
                    'premiere': 'premiere',
                    'after effects': 'afterfx',
                    'audition': 'audition',
                    'lightroom': 'lightroom',
                    'bridge': 'bridge',
                    'acrobat': 'acrobat',
                    'reader': 'acrord32',
                    'teams': 'teams',
                    'zoom': 'zoom',
                    'skype': 'skype',
                    'discord': 'discord',
                    'spotify': 'spotify',
                    'vlc': 'vlc',
                    'media player': 'wmplayer',
                    'windows media player': 'wmplayer',
                    'groove music': 'mswindowsmusic:',
                    'movies & tv': 'mswindowsvideo:',
                    'photos': 'ms-photos:',
                    'camera': 'start microsoft.windows.camera:',
                    'alarms': 'ms-clock:',
                    'clock': 'ms-clock:',
                    'calendar': 'outlookcal:',
                    'mail': 'start outlookmail:',
                    'maps': 'bingmaps:',
                    'weather': 'msnweather:',
                    'news': 'msnnews:',
                    'sports': 'msnsports:',
                    'money': 'msnmoney:',
                    'store': 'ms-windows-store:',
                    'settings': 'ms-settings:',
                    'control panel': 'control',
                    'task manager': 'taskmgr',
                    'file explorer': 'explorer',
                    'this pc': 'explorer',
                    'my computer': 'explorer',
                    'documents': 'explorer shell:DocumentsLibrary',
                    'downloads': 'explorer shell:Downloads',
                    'pictures': 'explorer shell:PicturesLibrary',
                    'music': 'explorer shell:MusicLibrary',
                    'videos': 'explorer shell:VideosLibrary',
                    'desktop': 'explorer shell:Desktop',
                    'recycle bin': 'explorer shell:RecycleBinFolder',
                    'network': 'explorer shell:NetworkPlacesFolder',
                    'printers': 'explorer shell:PrintersFolder',
                    'fonts': 'explorer shell:Fonts',
                    'start menu': 'explorer shell:StartMenu',
                    'run': 'shell:AppsFolder',
                    'apps': 'shell:AppsFolder',
                    'programs': 'shell:ProgramFiles',
                    'program files': 'shell:ProgramFiles',
                    'program files (x86)': 'shell:ProgramFilesX86',
                    'system32': 'explorer shell:System',
                    'system': 'explorer shell:System',
                    'windows': 'explorer shell:Windows',
                    'users': 'explorer shell:UsersFilesFolder',
                    'user': 'explorer shell:UsersFilesFolder',
                    'public': 'explorer shell:CommonDocuments',
                    'shared': 'explorer shell:CommonDocuments',
                    'temp': 'explorer shell:Temp',
                    'temporary': 'explorer shell:Temp',
                    'recent': 'explorer shell:Recent',
                    'favorites': 'explorer shell:Favorites',
                    'links': 'explorer shell:Links',
                    'search': 'explorer shell:SearchHomeFolder',
                    'home': 'explorer shell:HomeFolder',
                    'personal': 'explorer shell:Personal',
                    'my documents': 'explorer shell:Personal',
                    'my pictures': 'explorer shell:My Pictures',
                    'my music': 'explorer shell:My Music',
                    'my videos': 'explorer shell:My Video',
                    'my computer': 'explorer shell:MyComputerFolder',
                    'computer': 'explorer shell:MyComputerFolder',
                    'network': 'explorer shell:NetworkPlacesFolder',
                    'printers': 'explorer shell:PrintersFolder',
                    'fonts': 'explorer shell:Fonts',
                    'start menu': 'explorer shell:StartMenu',
                    'run': 'shell:AppsFolder',
                    'apps': 'shell:AppsFolder',
                    'programs': 'shell:ProgramFiles',
                    'program files': 'shell:ProgramFiles',
                    'program files (x86)': 'shell:ProgramFilesX86',
                    'system32': 'explorer shell:System',
                    'system': 'explorer shell:System',
                    'windows': 'explorer shell:Windows',
                    'users': 'explorer shell:UsersFilesFolder',
                    'user': 'explorer shell:UsersFilesFolder',
                    'public': 'explorer shell:CommonDocuments',
                    'shared': 'explorer shell:CommonDocuments',
                    'temp': 'explorer shell:Temp',
                    'temporary': 'explorer shell:Temp',
                    'recent': 'explorer shell:Recent',
                    'favorites': 'explorer shell:Favorites',
                    'links': 'explorer shell:Links',
                    'search': 'explorer shell:SearchHomeFolder',
                    'home': 'explorer shell:HomeFolder',
                    'personal': 'explorer shell:Personal',
                    'my documents': 'explorer shell:Personal',
                    'my pictures': 'explorer shell:My Pictures',
                    'my music': 'explorer shell:My Music',
                    'my videos': 'explorer shell:My Video',
                    'my computer': 'explorer shell:MyComputerFolder',
                    'computer': 'explorer shell:MyComputerFolder'
                }

                if app_name in common_apps:
                    os.system(f'start {common_apps[app_name]}')
                    self.speak(f"Opening {app_name}")
                else:
                    # Try to open the application directly
                    try:
                        os.system(f'start {app_name}')
                        self.speak(f"Attempting to open {app_name}")
                    except:
                        self.speak(f"Sorry, I couldn't open {app_name}. The application might not be installed or the command is not recognized.")
            except Exception as e:
                logging.error(f"Error opening application: {e}")
                self.speak(f"Sorry, I couldn't open {app_name}")
            return

        # If no command matches
        self.speak("I'm not sure how to help with that. Could you please rephrase?")

class JarvisGUI:
    def __init__(self, root, jarvis_instance):
        self.root = root
        self.jarvis = jarvis_instance
        self.root.title("JARVIS AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#000000')
        
        # Make window fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')
        
        # Create canvas for animations
        self.canvas = tk.Canvas(self.main_frame, width=1200, height=800,
                              bg='#000000', highlightthickness=0)
        self.canvas.pack(expand=True, fill='both')
        
        # Initialize animation variables
        self.angle = 0
        self.pulse = 0
        self.pulse_growing = True
        self.rings = []
        self.particles = []
        self.voice_visualizer = []
        
        # Create custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=36, weight="bold")
        self.status_font = tkfont.Font(family="Helvetica", size=24)
        
        # Create title
        self.title_label = tk.Label(self.canvas,
                                  text="JARVIS",
                                  font=self.title_font,
                                  fg='#00ff88',
                                  bg='#000000')
        self.title_label.place(relx=0.5, rely=0.1, anchor='center')
        
        # Create status label
        self.status_label = tk.Label(self.canvas,
                                   text="Initializing...",
                                   font=self.status_font,
                                   fg='#00ff88',
                                   bg='#000000')
        self.status_label.place(relx=0.5, rely=0.9, anchor='center')
        
        # Create voice visualizer
        self.create_voice_visualizer()
        
        # Create command buttons
        self.create_command_buttons()
        
        # Start animations
        self.create_logo_animation()
        self.animate_particles()
        
        # Start voice recognition
        self.continuous_listen()

    def create_voice_visualizer(self):
        # Create matplotlib figure for voice visualization
        self.fig = Figure(figsize=(8, 2), facecolor='#000000')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#000000')
        self.ax.set_ylim(-1, 1)
        self.ax.set_xlim(0, 100)
        self.ax.axis('off')
        
        # Create canvas for matplotlib
        self.canvas_visualizer = FigureCanvasTkAgg(self.fig, master=self.canvas)
        self.canvas_visualizer.get_tk_widget().place(relx=0.5, rely=0.5, anchor='center')
        
        # Initialize line for visualization
        self.line, = self.ax.plot([], [], color='#00ff88', linewidth=2)
        
        # Start animation
        self.animate_voice_visualizer()

    def animate_voice_visualizer(self):
        # Generate random data for visualization
        data = np.random.randn(100)
        data = signal.savgol_filter(data, 5, 2)
        
        # Update line data
        self.line.set_data(range(100), data)
        self.canvas_visualizer.draw()
        
        # Schedule next update
        self.root.after(50, self.animate_voice_visualizer)

    def create_logo_animation(self):
        # Clear canvas
        self.canvas.delete("logo")
        
        center_x = 600
        center_y = 400
        
        # Create pulsing effect
        if self.pulse_growing:
            self.pulse += 0.5
            if self.pulse >= 20:
                self.pulse_growing = False
        else:
            self.pulse -= 0.5
            if self.pulse <= 0:
                self.pulse_growing = True
        
        # Draw multiple rotating rings
        for i in range(5):
            radius = 100 + i * 40 + self.pulse
            # Outer ring
            self.canvas.create_oval(center_x-radius, center_y-radius,
                                  center_x+radius, center_y+radius,
                                  outline='#0088ff',
                                  width=2,
                                  tags="logo")
            
            # Animated arc
            start_angle = self.angle + i * 30
            extent = 60
            self.canvas.create_arc(center_x-radius, center_y-radius,
                                  center_x+radius, center_y+radius,
                                  start=start_angle, extent=extent,
                                  outline='#00ff88', width=4,
                                  tags="logo")
        
        # Central core
        core_radius = 60 + self.pulse/2
        self.canvas.create_oval(center_x-core_radius, center_y-core_radius,
                              center_x+core_radius, center_y+core_radius,
                              fill='#0088ff', outline='#00ff88', width=2,
                              tags="logo")
        
        # Update animation
        self.angle = (self.angle + 1) % 360
        self.root.after(20, self.create_logo_animation)

    def animate_particles(self):
        # Clear old particles
        self.canvas.delete("particle")
        
        # Create new particles
        for _ in range(5):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            size = random.randint(2, 4)
            color = random.choice(['#00ff88', '#0088ff'])
            self.canvas.create_oval(x, y, x+size, y+size,
                                  fill=color, outline=color,
                                  tags="particle")
        
        # Schedule next update
        self.root.after(100, self.animate_particles)

    def create_command_buttons(self):
        commands_frame = ttk.Frame(self.canvas)
        commands_frame.place(relx=0.5, rely=0.8, anchor='center')
        
        commands = [
            ("Time", lambda: self.jarvis.process_command("time")),
            ("Weather", lambda: self.jarvis.process_command("weather")),
            ("News", lambda: self.jarvis.process_command("news")),
            ("System Info", lambda: self.jarvis.process_command("system")),
            ("Calculator", lambda: self.jarvis.process_command("calculator")),
            ("Screenshot", lambda: self.jarvis.process_command("screenshot"))
        ]
        
        for text, command in commands:
            btn = tk.Button(commands_frame,
                          text=text,
                          font=("Helvetica", 12, "bold"),
                          bg='#1a1a1a',
                          fg='#00ff88',
                          activebackground='#2a2a2a',
                          activeforeground='#00ff88',
                          relief='flat',
                          padx=20,
                          pady=10,
                          command=command)
            btn.pack(side='left', padx=5)

    def continuous_listen(self):
        def listen_thread():
            query = self.jarvis.listen()
            if query:
                self.status_label.config(text="Processing...")
                self.root.update()
                self.jarvis.process_command(query)
                self.status_label.config(text="Listening...")
            self.root.after(100, self.continuous_listen)
        
        threading.Thread(target=listen_thread, daemon=True).start()

def main():
    print("Initializing JARVIS...")
    
    # Create Tkinter root window
    root = tk.Tk()
    
    # Create Jarvis instance
    jarvis = Jarvis()
    
    # Create GUI
    gui = JarvisGUI(root, jarvis)
    
    # Welcome message
    jarvis.speak(f"Hello {jarvis.user}, I am {jarvis.name}, your personal assistant. How may I help you?")
    
    # Start GUI main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()