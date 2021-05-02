from encoder.params_model import model_embedding_size as speaker_embedding_size
from utils.argutils import print_args
from utils.modelutils import check_model_paths
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import argparse
import torch
import sys
import os


class VCWrapper():
    def __init__(self):
        self.embed = None
        self.synthesizer = None
        pass
    
    def load(self,voice_wav_path):
        encoder.load_model(Path("encoder/saved_models/pretrained.pt"))
        self.synthesizer = Synthesizer(Path("synthesizer/saved_models/pretrained/pretrained.pt"))
        vocoder.load_model(Path("vocoder/saved_models/pretrained/pretrained.pt"))

        preprocessed_wav = encoder.preprocess_wav(voice_wav_path)
        self.embed = encoder.embed_utterance(preprocessed_wav)

    def generate_wav(self, text):
        embeds = [self.embed]
        texts = [text]

        specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
        spec = specs[0]

        generated_wav = vocoder.infer_waveform(spec)
        generated_wav = np.pad(generated_wav, (0, self.synthesizer.sample_rate), mode="constant")
        return generated_wav
        
        
