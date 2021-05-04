import speech_recognition as sr
import configparser
import os
from fernando import Fernando

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

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

        if microphone_idx > len(sr.Microphone.list_microphone_names()):
            print("Microphone index mismatch!")
            midx_fp.close()
        else:
            midx_fp.close()

            print(f"Loaded mic index from file. {sr.Microphone.list_microphone_names()[microphone_idx]}")
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
    
    try:
        recognized = recognizer.recognize_google(audio, language="en-EN")
    except BaseException as e:
        print("Speech recognition error: "+str(e))
        return None
    else:
        return recognized

    return None

def run_test():
    print("[+] Running test...")
    bot.say("Hi! My name is Fernando. You can talk to me just like you would talk to any other human!")

def init():
    global bot

    if not os.path.exists("voc.wav"):
        print("Error: Fernando's 'voc.wav' file doesn't exist. Please place a short .wav file of the voice you would like Fernando to have in the project root.")
        exit(-1)

    # configure microphone
    configure_mic()

    print("Fernando is waking up...")

    # setup fernando
    bot = Fernando()
    bot.load()
    print("[+] Loaded!")

    # test
    run_test()

    # converse
    while True:
        print("Fernando is listening...")
        input_speech = get_input_speech()
        if input_speech is None:
            print("Fernando didn't understand that, please try again.")
            continue
        
        print(f"You: {input_speech}")
        print("Fernando is thinking...")
        response = bot.generate_response(input_speech)
        bot.say(response)
        print(f"Fernando: {response}")

    # text to speech
    bot.say(response)


if __name__ == "__main__":
    init()