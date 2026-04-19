import os
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
import time

def speak(Text):
    engine = pyttsx3.init()
    engine.say(Text)
    engine.runAndWait()
    engine.stop()

def voiceinput(t=2,pl=2):
    with sr.Microphone() as source:
        # r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source,timeout=t,phrase_time_limit=pl)
    return r.recognize_google(audio)

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

# Sending whatsapp mesg
def sendmsg(name,msg):
    subprocess.Popen('start whatsapp:',shell=True)
    time.sleep(1)
    pyautogui.hotkey('ctrl','f')
    pyautogui.hotkey('ctrl','backspace')
    pyautogui.write(name)
    time.sleep(1.3)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(msg)
    time.sleep(0.5)
    pyautogui.press('enter')

# opening files
def filesearch(filename,filepath,skip=None):
    for root, dirs, files in os.walk(filepath):
        if skip and any(root.startswith(s) for s in skip):
            continue
        for file in files:
            if filename.lower() in file.lower():
                return os.path.join(root, file)
    return None

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
            # opening sytem apps
        if optn in sd.sys.keys():
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            cmdprom=sd.sys[optn]
            speak(f"opening {optn}")
            subprocess.Popen(f"start {cmdprom}",shell=True)
            #     subprocess.Popen(["calc"]) another way to open system apps via  cmd

            # opens websites
        elif optn in sd.web.keys():
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            speak(f'opening {optn}')
            webbrowser.open(f'https://{optn}.com')
        
        else:
            if 'drive' in optn:
                if len(optn)>2:
                    speak("please specify drive")
                else:
                    speak(f'opening {optn} drive')
                    subprocess.Popen(f"start {optn}:",shell=True)
            else:
                for p in sd.paths:
                    fpath=filesearch(optn,p)
                    if fpath:
                        speak(f'opening {optn}')
                        subprocess.Popen(f'start "" "{fpath}"',shell=True)
                        break
                else:
                    fpath=filesearch(optn,r"C:\Users\Aditya",skip=sd.paths)
                    if fpath:
                        speak(f'opening {optn}')
                        subprocess.Popen(f'start "" "{fpath}"',shell=True)
                    else:
                        speak("showing similar results")
                        optn=inst.lower()[4:]
                        webbrowser.open(f'https://www.google.com/search?q={optn}')


# youtube video play
    elif 'play' in inst.lower() or "youtube" in inst.lower():
        inst = inst.lower().replace("play", "",1).strip()
        if len(inst)<3:
            pass
        else:
            speak(f'playing {inst}')
            pywhatkit.playonyt(inst)


    # seding whatsapp mesg
    elif 'send'in inst.lower() or 'whatsapp' in inst.lower():
        try:
            if 'to' in inst.lower():
                inst=inst.replace("send","").replace("whatsapp","").strip()
                name=inst.split("to")[1].strip()
                speak(f'do you want to send to {name} ?')
                cnfname=voiceinput(t=3,pl=3)
                if 'correct' in cnfname.lower():
                    mesg=inst.split("to")[0].strip()
                    speak(f'do you want to send {mesg} ?')
                    cnfmsg=voiceinput(t=3,pl=3)
                    if 'correct' in cnfmsg.lower():
                        sendmsg(name,mesg)
                    else:
                        print("message cancelled")
                        speak('message cancelled')
                else:
                    print("name not recognised")
                    speak("sorry didn't recognised")

            else:
                speak('To whom sir ?')
                print("Listening for name...")
                name = voiceinput()
                print(name)
                speak(f'repeat correct if the name is {name} ?')
                print("Listening for name confirmation...")
                namecnf=voiceinput(t=3,pl=3)
                if 'correct' in namecnf.lower():
                    speak(f"what's the message sir ?")
                    msg=voiceinput(t=6,pl=6)
                    print(msg)
                    speak(f'repeat correct if the message is {msg} ?')
                    print("Listening for message confirmation...")
                    msgcnf=voiceinput(t=3,pl=3)
                    if 'correct' in msgcnf.lower():
                        subprocess.Popen('start whatsapp:',shell=True)
                        time.sleep(1.5)
                        sendmsg(name,msg)
                    else:
                        print("message cancelled")
                        speak('message cancelled')
                else:
                    print("name not recognised")
                    speak("sorry didn't recognised")
        except Exception as e:
            print(format(e))
            speak("didn't recognised")

    
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
            print("speak now...")
            uservoice = voiceinput()
            print(uservoice)
            if 'jarvis' in uservoice.lower():
                speak("yes sir")
                print("recognising task ...")
                userorder = voiceinput(t=6,pl=6)
                print(userorder)
                order(userorder)
        except Exception as e:
            print(format(e))