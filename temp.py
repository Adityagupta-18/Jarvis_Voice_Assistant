import winsound
import datetime
# winsound.Beep(6000, 500)  # 1kHz, 200ms
import datetime
import subprocess
import stored_data as sd
import datetime
import webbrowser
import wikipedia
import pyjokes
import pywhatkit
inst=input("enter: ")
inst = inst.lower().replace("play", "",1).strip()
print(inst)
pywhatkit.playonyt(inst)