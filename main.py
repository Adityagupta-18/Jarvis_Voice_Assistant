# c:\Users\Aditya\OneDrive\Desktop\python\Project_Jarvis\.venv\Scripts\Activate.ps1
import speech_recognition as sr
import pyttsx3
import webbrowser
import winsound
import stored_data as sd
import subprocess
import datetime
import wikipedia
import pywhatkit
import pyautogui

def speak(Text):
    engine = pyttsx3.init()
    engine.say(Text)
    engine.runAndWait()
    engine.stop()

def timenow():
    now=datetime.datetime.now()
    now_12=now.strftime("%I:%M: %p")
    return now_12

def greet():
    hour=datetime.datetime.now().hour
    if hour<12 and hour>4:
        speak("good morning sir")
    elif hour<16:
        speak("good afternoon sir")
    else:
        speak("good evening sir")
def controls(k,press=1):
    return pyautogui.press(k,presses=press) 

# removing extra words from inst
def cleanquery(order):
    order=order.lower()
    for i in sd.phrases:
        if order.startswith(i):
            order=order.replace(i,"",1)

    word=order.split()
    fil=[w for w in word if w not in sd.words]
    return " ".join(fil).strip()

def order(inst):
    # youtube video controls
    if 'volume' in inst.lower() or 'mute' in inst.lower():
        if 'increase' in inst.lower() or 'up' in inst.lower():
            controls('up',2)
        elif 'decrease' in inst.lower() or 'down' in inst.lower():
            controls('down',2)
        elif 'mute' in inst.lower() or 'zero' in inst.lower():
            controls('down',20)
        elif 'max' in inst.lower():
            controls('up',20)
    elif any(p in inst.lower() for p in ["pause", "stop","hold"]):
        controls('k')
    elif 'resume' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        controls('k')
    elif 'next video' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        pyautogui.hotkey('shift','n')
    elif 'previous video' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        pyautogui.hotkey('shift','p')

      
    #   Sytem apps / websites
    elif 'start' in inst.lower() or 'open' in inst.lower():
        optn=inst.lower().split(" ")[1]
        if optn not in sd.sys.keys():
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            # opening web results
            if optn in sd.web.keys():
                speak(f'opening {optn}')
                webbrowser.open(f'https://{optn}.com')
            else:
                speak("showing similar results")
                optn=inst.lower()[4:]
                webbrowser.open(f'https://www.google.com/search?q={optn}')
        else:
            if 'drive' in optn:
                speak(f'opening drive {optn}')
                subprocess.Popen(f"start {optn}:",shell=True)
            else:
                # opening sytem apps
                winsound.Beep(6000, 500)  # 1kHz, 200ms
                cmdprom=sd.sys[optn]
                speak(f"opening {optn}")
                subprocess.Popen(f"start {cmdprom}",shell=True)
                #     subprocess.Popen(["calc"]) another way to open system apps via  cmd


# youtube video play
    elif 'play' in inst.lower() or "youtube" in inst.lower():
        inst = inst.lower().replace("play", "",1).strip()
        if len(inst)<3:
            pass
        else:
            speak(f'playing {inst}')
            pywhatkit.playonyt(inst)
    
    #   Date and time
    elif 'time' in inst.lower():
        speak(timenow())
    elif 'date' in inst.lower():
        date=datetime.date.today()
        speak(date)
    elif ((("what" in inst.lower()) or
           ("what's" in inst.lower()) or 
           ("the" in  inst.lower())) and "day" in inst.lower()):
        day=datetime.date.today()
        speak(f'its {day.strftime("%A")}')  # Day

    elif 'show' in inst.lower() or 'search' in inst.lower():
        inst = inst.lower().replace("show", "").replace("search", "").strip()
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        speak('showing google result')
        webbrowser.open(f'https://www.google.com/search?q={inst}')

    else:
        try:
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            print("Fetching information...")
            query=cleanquery(inst)
            print(query)
            outp=wikipedia.summary(f"{query}",sentences=2)
            speak("according to wikipedia...")
            print(outp)
            speak(outp)
        except wikipedia.exceptions.DisambiguationError as e:
            outp = wikipedia.summary(e.options[0], sentences=2)
            speak("according to wikipedia...")
            print(outp)
            speak(outp)
        except Exception as e:
            speak("showing google search results")
            webbrowser.open(f'https://www.google.com/search?q={inst}')


if __name__=='__main__':
    print("Activating...")
    speak('Initializing jarvis...')
    greet()
    r=sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source:
                print("speak now...")
                # r.adjust_for_ambient_noise(source, duration=1.2)
                audio = r.listen(source,timeout=2,phrase_time_limit=2)
            uservoice = r.recognize_google(audio)
            print(uservoice)
            if 'jarvis' in uservoice.lower():
                speak("yes sir")
                print("recognising task ...")
                with sr.Microphone() as source:
                    audio = r.listen(source,timeout=6,phrase_time_limit=6)
                userorder = r.recognize_google(audio)
                print(userorder)
                order(userorder)
        except Exception as e:
            print(format(e))