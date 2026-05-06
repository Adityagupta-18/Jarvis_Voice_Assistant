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
import pyperclip

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
    time.sleep(2)
    pyautogui.hotkey('ctrl','f')
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')
    pyautogui.write(name)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.write(msg)
    time.sleep(0.5)

def sendfile(name,loc):
    subprocess.Popen('start whatsapp:',shell=True)
    time.sleep(2)
    pyautogui.hotkey('ctrl','f')
    pyautogui.hotkey('ctrl','a')
    pyautogui.press('backspace')
    pyautogui.write(name)
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.hotkey('shift','tab')
    pyautogui.hotkey('shift','tab')
    time.sleep(1)
    pyperclip.copy(loc)
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(1.5)
    pyautogui.hotkey('ctrl','v')
    time.sleep(1.5)
    pyautogui.press('enter')
    time.sleep(2)

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
    elif 'forward' in inst.lower():
        controls('l')
    elif 'backward' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        controls('j')
    elif 'next video' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        pyautogui.hotkey('shift','n')
    elif 'previous video' in inst.lower():
        winsound.Beep(6000, 500)  # 1kHz, 200ms
        pyautogui.hotkey('shift','p')

      
#   Sytem apps / websites
    elif 'start' in inst.lower() or 'open' in inst.lower():
        optn=inst.lower().split(" ")[1]
        optn2=inst.lower().split(" ")[1:]
        optn2=" ".join(optn2)
            # opening sytem apps
        if optn in sd.sys.keys():
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            cmdprom=sd.sys[optn]
            speak(f"opening {optn}")
            subprocess.Popen(f"start {cmdprom}",shell=True)

            # opens websites
        elif optn in sd.web.keys():
            winsound.Beep(6000, 500)  # 1kHz, 200ms
            speak(f'opening {optn}')
            webbrowser.open(f'https://{optn}.com')
        
        # system search
        else:
            if 'drive' in optn:
                if len(optn)>2:
                    speak("please specify drive")
                else:
                    speak(f'opening {optn} drive')
                    subprocess.Popen(f"start {optn}:",shell=True)
            else:
                # system file search
                speak('searching file')
                for p in sd.paths:
                    fpath=filesearch(optn,p)
                    if fpath:
                        speak(f'opening {optn2}')
                        subprocess.Popen(f'explorer /select,"{fpath}"', shell=True)
                        time.sleep(1.5)
                        subprocess.Popen(f'start "" "{fpath}"',shell=True)
                        break
                else:
                    fpath=filesearch(optn,r"C:\Users\Aditya",skip=sd.paths)
                    if fpath:
                        speak(f'opening {optn2}')
                        subprocess.Popen(f'explorer /select,"{fpath}"', shell=True)
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
            if 'message' in inst.lower():
                speak('To whom sir ... name ?')
                print("Listening for name...")
                name = voiceinput()
                print(name)
                speak(f"what's the message sir ?")
                print('listening for message ...')
                msg=voiceinput(t=14,pl=20)
                print(msg)
                speak(f'repeat correct if you wamt to send {msg} to {name}')
                print('please confirm by saying correct...')
                msgcnf=voiceinput(t=3,pl=3)
                print(msgcnf)
                if 'correct' in msgcnf.lower():
                    print("sending")
                    speak('sending')
                    sendmsg(name,msg)
                    speak('should i send please confirm ?')
                    lastcnf=voiceinput()
                    if 'correct' in lastcnf.lower():
                        pyautogui.press('enter')
                        speak('message sent')
                    else:
                        pyautogui.hotkey('ctrl','a')
                        pyautogui.press('backspace')
                else:
                    print("message cancelled")
                    speak('message cancelled')
            
            # sending document
            elif 'file' in inst.lower() or 'document' in inst.lower():
                speak('whats the file name')
                print('whats the file name')
                fname=voiceinput(3,3)
                fname=fname.split(" ")[0]
                print(fname)
                speak('searching file')
                for p in sd.paths:
                    fpath=filesearch(fname,p)
                    if fpath:
                        subprocess.Popen(f'explorer /select,"{fpath}"', shell=True)
                        time.sleep(1.5)
                        speak('do you want me to send this file')
                        break
                else:
                    fpath=filesearch(fname,r"C:\Users\Aditya",skip=sd.paths)
                    if fpath:
                        subprocess.Popen(f'explorer /select,"{fpath}"', shell=True)
                        time.sleep(1.5)
                        speak('do you want me to send this file')
                        subprocess.Popen(f'start "" "{fpath}"',shell=True)
                    else:
                        speak('file not found')
                        print('file not found')
                if fpath:
                    speak('speak correct if yes ')
                    print('speak correct if yes ')
                    fcnf=voiceinput()
                    if 'correct' in fcnf.lower():
                        print('to whom sir ?')
                        speak('to whom sir ?')
                        name=voiceinput()
                        print(name)
                        speak(f'do you want to send this to {name}')
                        speak('please confirm')
                        print('please confirm by saying correct')
                        ncnf=voiceinput()
                        if 'correct' in ncnf.lower():
                            sendfile(name,fpath)
                            speak('should i send please confirm ?')
                            lastcnf=voiceinput()
                            if 'correct' in lastcnf.lower():
                                pyautogui.press('enter')
                                speak('file sent')
                    else:
                        print('sending cancelled')
                        speak('sending cancelled')
            else:
                print("didn't recognised")
                speak("didn't recognised")

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
                userorder = voiceinput(t=7,pl=10)
                print(userorder)
                order(userorder)
        except Exception as e:
            print(format(e))