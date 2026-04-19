# Jarvis_Voice_Assistant  
Jarvis - Python Voice Assistant  

Jarvis is a Python-based voice assistant capable of performing system operations, web automation, media playback, and answering user queries through voice commands.  

# Working Principle
Jarvis continuously listens for the wake word `Jarvis`.  
Once detected, it temporarily activates and listens for a command.  
The spoken input is converted into text using speech recognition.  
The system then analyzes the command and routes it to the appropriate module, such as:

- System control  
- Web automation  
- Media handling  
- Information retrieval  
- File opening / searching  
- Whatsapp messaging service
After executing the task, Jarvis returns to standby mode, waiting for the next wake word.

# How to Use
Jarvis operates using a wake-word mechanism.

1. Start the application.
2. Say the wake word: `Jarvis`
3. Jarvis will respond with an acknowledgement tone or message.
4. After the response, speak your command clearly.
Jarvis will then process the command and perform the requested action.

# Requirements
Jarvis requires Python 3.8 to 3.11 and is designed to run on Windows 10 or Windows 11. A working microphone and an active internet connection are necessary for voice recognition and web-based features.

The project depends on common Python libraries such as SpeechRecognition, pyttsx3, pywhatkit, pyautogui, wikipedia, and pyaudio. These can be installed using the provided requirements file.

For the WhatsApp messaging feature, WhatsApp Desktop must be installed and logged in on the system.

It is recommended to use a virtual environment to manage dependencies and ensure smooth execution.

# Features  
System Control  
Open system applications such as Calculator, File Explorer, and others 
Open websites, play, pause, controls volumes of video playing on youtube  
Launch desktop applications using predefined paths  
Search any system files  
Send messages via whatsapp  
 
# Web Automation  
Open frequently used websites like YouTube, Google, and ChatGPT  
Automatically perform a Google search if the requested website is not recognized  

# Media Control  
Play any song or video on YouTube using dynamic search  
Pause and resume playback  
Control volume (increase/decrease)  
Skip forward and backward  

# Search and Information  
Perform Google searches for general queries  
Fetch summaries from Wikipedia for informational questions  

# Input Processing  
Cleans and processes user commands by removing unnecessary words  
Extracts relevant keywords for better accuracy  

# Tech Stack  
Python  
SpeechRecognition  
pyttsx3 (Text-to-Speech)  
pywhatkit (YouTube automation)  
pyautogui (Keyboard automation)  
wikipedia (Information retrieval)  

# How It Works  
Captures voice input from the user  
Converts speech to text  
Processes the command using keyword-based logic  
Executes the appropriate action:  
System operation  
Web navigation  
Media control  
Information retrieval  

# Usage  
python main.py  

# Example commands:  
"Open YouTube"  
"Play lo-fi music"  
"Pause video"  
"Search Python tutorial"  
"Who is Elon Musk"  
