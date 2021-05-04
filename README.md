# fernando
A conversational AI that uses Dialo-GPT2, speech recognition, and Real Time Voice Cloning to be as human-like as possible.

## Steps to run
1. Run `pip install -r requirements.txt` to fetch all of the dependencies.
2. Get the pretrained models here: [Link](https://github.com/CorentinJ/Real-Time-Voice-Cloning/wiki/Pretrained-models)
2. Run the `human.py` file to talk to fernando!

Uses the encoder, vocoder, and synthesizer from Real Time Voice Cloning:

https://github.com/CorentinJ/Real-Time-Voice-Cloning

---

### Challenges

I did end up running into a few challenges while developing this project. It was surprisingly easy to create a wrapper module for Real Time Voice Cloning in order to use it with Fernando, but the only issue I ran into was with the sounddevice module, and I ended up having to uninstall it and [installing a specific version of sounddevice.](https://stackoverflow.com/q/62412684) After that, it imported fine, but I couldn't hear any sounds from my speakers so I had to try it on another computer.

Another challenge I ran into was with the SpeechRecognition module, it kept giving me obscure errors and it would crash the program frequently. So I ended up using try/except statements to handle those errors, and now it works fine.

### Final notes

I really enjoyed developing Fernando, although he might not be very intelligent his responses can be pretty funny at times. In the future with faster computers I'm sure the voice cloning and text generation will be almost instant, and a lot smarter than Fernando is. It would open up a world of opportunities if a computer could intelligently and quickly communicate with humans.