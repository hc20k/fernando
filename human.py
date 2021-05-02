import speech_recognition as sr
import configparser
import os
from colored import fg, bg, attr
from fernando import Fernando

settings = {}
microphone_idx = -1

recognizer = None
bot = None

def configure_mic(skip_listing=False):
    global microphone_idx

    if os.path.exists("mic_idx.txt"):
        # load saved mic idx
        midx_fp = open("mic_idx.txt","r")
        microphone_idx = int(midx_fp.read())
        midx_fp.close()

        print(f"Loaded mic index from file.")
        return

    if len(sr.Microphone.list_microphone_names()) > 0:
        if not skip_listing:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"[{index}] {name}")
        
        print("-"*40)
        microphone_idx = int(input("[-] Type the index of your microphone here: "))

        if microphone_idx < 0 or microphone_idx > len(sr.Microphone.list_microphone_names())-1:
            print(f"[!] ERROR: Invalid index given. Please input a number from 0-{len(sr.Microphone.list_microphone_names())-1}")
            configure_mic(True)
            return
    elif len(sr.Microphone.list_microphone_names()) == 0:
        input("[!] ERROR: Please connect a microphone, then press enter.")
        configure_mic(True)
        return
    else:
        microphone_idx = 0

    print(f"[+] Using mic [{sr.Microphone.list_microphone_names()[microphone_idx]}]\n(This will be saved for future runs. To reselect an input device, delete the micidx.txt file in the root folder of this project.)")

    midx_fp = open("mic_idx.txt","w")
    midx_fp.write(str(microphone_idx))
    midx_fp.close()

def get_input_speech():
    global recognizer
    if recognizer is None:
        recognizer = sr.Recognizer()

    with sr.Microphone(microphone_idx) as src:
        audio = recognizer.listen(src)
    
    return recognizer.recognize_google(audio)


def init():
    global bot
    print("Fernando is waking up...")

    # setup fernando
    bot = Fernando()
    bot.load()
    print("[+] Loaded!")

    # configure microphone
    configure_mic()

    # converse
    response = bot.generate_response("Hello fernando")

    # text to speech
    bot.say(response)


if __name__ == "__main__":
    init()