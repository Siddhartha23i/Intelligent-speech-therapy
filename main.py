from modules.vosk_alignment import VoskAligner

# Initialize aligner once
aligner = VoskAligner()

audio = "data/align_audio/sample.wav"

results = aligner.align_words(audio)

print("\nWORD TIMESTAMPS:")
for r in results:
    if "result" in r:
        for w in r["result"]:
            print(w["word"], w["start"], w["end"])
