from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import voice
from tqdm import tqdm
import utils.modelutils as modelutils
from pathlib import Path
import sounddevice as sd
import numpy as np

class Fernando():
    def __init__(self):
        self.step = 0
        self.chat_history_ids = None
        pass

    def load(self):
        modelutils.check_model_paths(Path("encoder/saved_models/pretrained.pt"), Path("synthesizer/saved_models/pretrained/pretrained.pt"), Path("vocoder/saved_models/pretrained/pretrained.pt"))

        with tqdm(total=3) as bar:
            bar.set_description("Loading tokenizer")
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
            bar.update(1)
            bar.set_description("Loading GPT model")
            self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")
            bar.update(1)
            bar.set_description("Loading voice cloner")
            self.vc = voice.VCWrapper()
            self.vc.load("voc.wav")
            bar.update(1)
    
    def generate_response(self, query):
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = self.tokenizer.encode(query + self.tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1) if self.step > 0 else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens, 
        self.chat_history_ids = self.model.generate(bot_input_ids, max_length=1000, pad_token_id=self.tokenizer.eos_token_id)

        # pretty print last ouput tokens from bot
        return self.tokenizer.decode(self.chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    def say(self, text):
        wav = self.vc.generate_wav(text)

        # debug: save for testing because AUDIO IS BUGGED
        # import soundfile as sf
        # sf.write("output.wav", wav.astype(np.float32), self.vc.synthesizer.sample_rate)

        sd.stop()
        sd.play(wav, self.vc.synthesizer.sample_rate, blocking=True)

