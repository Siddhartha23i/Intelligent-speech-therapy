"""
Simple audio recorder for creating test files
Run this to record test audio samples for the speech therapy platform
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime

def record_audio(duration=5, sample_rate=16000):
    """
    Record audio from microphone
    
    Args:
        duration: Recording duration in seconds (default: 5)
        sample_rate: Sample rate in Hz (default: 16000)
    """
    print(f"🎙️  Recording for {duration} seconds...")
    print("📢 Speak now!")
    
    # Record audio
    audio = sd.rec(int(duration * sample_rate), 
                   samplerate=sample_rate, 
                   channels=1, 
                   dtype=np.float32)
    sd.wait()  # Wait until recording is finished
    
    print("✅ Recording complete!")
    return audio, sample_rate

def save_audio(audio, sample_rate, filename=None):
    """Save recorded audio to a WAV file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_audio_{timestamp}.wav"
    
    filepath = f"uploads/{filename}"
    sf.write(filepath, audio, sample_rate)
    print(f"💾 Saved to: {filepath}")
    return filepath

def main():
    """Main recording interface"""
    print("=" * 60)
    print("🎤 Audio Test Recorder - Speech Therapy Platform")
    print("=" * 60)
    print("\nSample sentences to practice:")
    print("1. The quick brown fox jumps over the lazy dog.")
    print("2. She sells seashells by the seashore.")
    print("3. How much wood would a woodchuck chuck?")
    print("4. Peter Piper picked a peck of pickled peppers.")
    print("5. The rain in Spain stays mainly in the plain.")
    print("\n" + "=" * 60)
    
    try:
        # Get recording duration
        duration_input = input("\n⏱️  Recording duration in seconds (default=5, press Enter): ")
        duration = int(duration_input) if duration_input.strip() else 5
        
        # Record
        audio, sample_rate = record_audio(duration=duration)
        
        # Save
        filename_input = input("\n📝 Filename (press Enter for auto-generated): ")
        filename = filename_input.strip() if filename_input.strip() else None
        save_audio(audio, sample_rate, filename)
        
        # Ask to record another
        again = input("\n🔄 Record another? (y/n): ")
        if again.lower() == 'y':
            main()
        else:
            print("\n👋 Goodbye!")
            
    except KeyboardInterrupt:
        print("\n\n❌ Recording cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Make sure you have a microphone connected!")

if __name__ == "__main__":
    main()
