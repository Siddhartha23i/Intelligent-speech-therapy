import json
import wave
from vosk import Model, KaldiRecognizer

class VoskAligner:
    def __init__(self, model_path="models/vosk-en"):
        self.model = Model(model_path)

    def align_words(self, audio_path):
        with wave.open(audio_path, "rb") as wf:
            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)

            results = []

            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    results.append(json.loads(rec.Result()))

            results.append(json.loads(rec.FinalResult()))
            return results
