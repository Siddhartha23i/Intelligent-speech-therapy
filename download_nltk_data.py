"""
Download required NLTK data for speech therapy platform
Run this once to set up all necessary NLTK resources
"""

import nltk
import sys

def download_nltk_data():
    """Download all required NLTK data packages"""
    
    packages = [
        'averaged_perceptron_tagger_eng',  # For POS tagging (English)
        'averaged_perceptron_tagger',      # For POS tagging (general)
        'cmudict',                         # CMU Pronouncing Dictionary
        'punkt',                           # Sentence tokenizer
        'brown',                           # Brown corpus (optional but useful)
    ]
    
    print("=" * 60)
    print("Downloading NLTK Data for Speech Therapy Platform")
    print("=" * 60)
    print()
    
    failed = []
    
    for package in packages:
        try:
            print(f"📦 Downloading '{package}'...", end=" ")
            nltk.download(package, quiet=True)
            print("✅")
        except Exception as e:
            print(f"❌ Failed: {e}")
            failed.append(package)
    
    print()
    print("=" * 60)
    
    if failed:
        print(f"❌ {len(failed)} package(s) failed to download:")
        for pkg in failed:
            print(f"   - {pkg}")
        print()
        print("You may need to download these manually:")
        print(">>> import nltk")
        for pkg in failed:
            print(f">>> nltk.download('{pkg}')")
        return False
    else:
        print("✅ All NLTK data downloaded successfully!")
        print()
        print("You can now use the speech therapy platform.")
        return True

if __name__ == "__main__":
    success = download_nltk_data()
    sys.exit(0 if success else 1)
