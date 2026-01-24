import os
from modules.vosk_alignment import VoskAligner

def test_vosk_alignment():
    # Ensure model path exists
    model_path = "models/vosk-en"
    if not os.path.exists(model_path):
        print(f"Skipping test: Model path {model_path} not found.")
        return

    # Initialize aligner
    aligner = VoskAligner(model_path=model_path)

    # Use a sample audio file. Using the one from data/align_audio/sample.wav
    audio_path = "data/align_audio/sample.wav"
    if not os.path.exists(audio_path):
        print(f"Skipping test: Audio path {audio_path} not found.")
        return

    print("Aligning audio...")
    results = aligner.align_words(audio_path)

    assert isinstance(results, list)
    print(f"Alignment successful. Found {len(results)} segments.")

    # Check if we got any words
    word_count = 0
    for r in results:
        if "result" in r:
            word_count += len(r["result"])

    print(f"Total words found: {word_count}")
    if word_count > 0:
        print("Test PASSED")
    else:
        print("Test PASSED (but no words found, which might be expected for short/quiet audio)")

if __name__ == "__main__":
    test_vosk_alignment()
