import librosa
import soundfile as sf
import numpy as np

def preprocess_audio(input_path, output_path):
    audio, sr = librosa.load(input_path, sr=16000)

    # Normalize
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    # Remove silence
    audio, _ = librosa.effects.trim(audio, top_db=20)

    sf.write(output_path, audio, sr)
    return output_path
