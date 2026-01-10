"""
Audio Processing Module for Speech Therapy Platform

This module handles all audio-related operations including:
- Audio preprocessing (normalization, trimming, noise reduction)
- Speech-to-text transcription using Whisper
- Text-to-phoneme conversion
- Phoneme-to-audio alignment
- MFCC feature extraction
"""

import streamlit as st
import librosa
import numpy as np
import torch
import torchaudio
import soundfile as sf
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from g2p_en import G2p
from typing import List, Dict, Tuple
import os
import tempfile


@st.cache_resource
def load_whisper_model():
    """
    Load and cache the Whisper model for speech-to-text transcription.
    
    Returns:
        pipeline: Hugging Face pipeline for automatic speech recognition
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    
    model_id = "openai/whisper-base"
    
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        low_cpu_mem_usage=True,
        use_safetensors=True
    )
    model.to(device)
    
    processor = AutoProcessor.from_pretrained(model_id)
    
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=False,
        torch_dtype=torch_dtype,
        device=device,
    )
    
    return pipe


@st.cache_resource
def load_g2p_model():
    """
    Load and cache the grapheme-to-phoneme converter.
    
    Returns:
        G2p: Grapheme-to-phoneme converter instance
    """
    import nltk
    # Ensure required NLTK data is downloaded
    required_packages = [
        ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
        ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
        ('corpora/cmudict', 'cmudict'),
        ('tokenizers/punkt', 'punkt')
    ]
    
    for resource_path, package_name in required_packages:
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(package_name)
            
    return G2p()


def preprocess_audio(audio_file, target_sr=16000):
    """
    Preprocess audio file for analysis.
    
    Args:
        audio_file: Audio file (bytes, file path, or file-like object)
        target_sr: Target sample rate (default: 16000 Hz)
    
    Returns:
        tuple: (audio_array, sample_rate)
    """
    try:
        # Handle different audio input types
        if isinstance(audio_file, bytes):
            # Save bytes to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
                tmp.write(audio_file)
                tmp_path = tmp.name
            
            # Load audio
            audio_array, sr = librosa.load(tmp_path, sr=target_sr, mono=True)
            
            # Clean up temp file
            os.unlink(tmp_path)
        elif isinstance(audio_file, str):
            # Load from file path
            audio_array, sr = librosa.load(audio_file, sr=target_sr, mono=True)
        else:
            # Assume file-like object
            audio_array, sr = librosa.load(audio_file, sr=target_sr, mono=True)
        
        # Normalize audio to [-1, 1] range
        if audio_array.max() > 0:
            audio_array = audio_array / np.abs(audio_array).max()
        
        # Trim silence from start and end
        audio_array, _ = librosa.effects.trim(
            audio_array,
            top_db=20,  # Threshold in dB below reference
            frame_length=2048,
            hop_length=512
        )
        
        # Apply simple high-pass filter to reduce low-frequency noise
        audio_array = librosa.effects.preemphasis(audio_array, coef=0.97)
        
        # Ensure audio is not empty
        if len(audio_array) == 0:
            raise ValueError("Audio is empty after preprocessing")
        
        return audio_array, sr
    
    except Exception as e:
        raise Exception(f"Error preprocessing audio: {str(e)}")


def transcribe_audio(audio_array, sample_rate=16000):
    """
    Transcribe audio to text using Whisper model.
    
    Args:
        audio_array: Audio data as numpy array
        sample_rate: Sample rate of the audio (default: 16000)
    
    Returns:
        str: Transcribed text
    """
    try:
        # Load model
        pipe = load_whisper_model()
        
        # Ensure audio is float32 for Whisper
        if audio_array.dtype != np.float32:
            audio_array = audio_array.astype(np.float32)
        
        # Resample if necessary
        if sample_rate != 16000:
            audio_array = librosa.resample(
                audio_array,
                orig_sr=sample_rate,
                target_sr=16000
            )
        
        # Transcribe
        result = pipe(audio_array)
        transcription = result["text"].strip()
        
        return transcription
    
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")


def text_to_phonemes(text):
    """
    Convert text to phoneme sequence.
    
    Args:
        text: Input text string
    
    Returns:
        list: List of phoneme strings
    """
    try:
        g2p = load_g2p_model()
        
        # Convert to phonemes
        phonemes = g2p(text)
        
        # Filter out spaces and punctuation
        phonemes = [p for p in phonemes if p not in [' ', ',', '.', '!', '?', ';', ':']]
        
        return phonemes
    
    except Exception as e:
        raise Exception(f"Error converting text to phonemes: {str(e)}")


def align_phonemes_to_audio(audio_array, phonemes, sample_rate=16000):
    """
    Align phonemes to audio segments using time-based division.
    
    Args:
        audio_array: Audio data as numpy array
        phonemes: List of phoneme strings
        sample_rate: Sample rate of the audio
    
    Returns:
        list: List of dictionaries with phoneme alignment data
    """
    try:
        if len(phonemes) == 0:
            return []
        
        # Calculate duration per phoneme (simple equal division)
        total_duration = len(audio_array) / sample_rate
        duration_per_phoneme = total_duration / len(phonemes)
        
        alignments = []
        
        for i, phoneme in enumerate(phonemes):
            # Calculate start and end times
            start_time = i * duration_per_phoneme
            end_time = (i + 1) * duration_per_phoneme
            
            # Convert to sample indices
            start_sample = int(start_time * sample_rate)
            end_sample = int(end_time * sample_rate)
            
            # Extract audio segment
            audio_segment = audio_array[start_sample:end_sample]
            
            # Store alignment data
            alignment = {
                'phoneme': phoneme,
                'start_time': start_time,
                'end_time': end_time,
                'audio_segment': audio_segment,
                'sample_rate': sample_rate
            }
            
            alignments.append(alignment)
        
        return alignments
    
    except Exception as e:
        raise Exception(f"Error aligning phonemes to audio: {str(e)}")


def extract_phoneme_features(audio_segment, sample_rate=16000, n_mfcc=13):
    """
    Extract MFCC features from an audio segment.
    
    Args:
        audio_segment: Audio segment as numpy array
        sample_rate: Sample rate of the audio
        n_mfcc: Number of MFCC coefficients to extract
    
    Returns:
        numpy.ndarray: Feature vector of shape (n_mfcc,)
    """
    try:
        # Handle empty or very short segments
        if len(audio_segment) < 512:
            # Pad with zeros
            audio_segment = np.pad(
                audio_segment,
                (0, 512 - len(audio_segment)),
                mode='constant'
            )
        
        # Extract MFCCs
        mfccs = librosa.feature.mfcc(
            y=audio_segment,
            sr=sample_rate,
            n_mfcc=n_mfcc,
            n_fft=512,
            hop_length=256
        )
        
        # Compute mean across time dimension
        feature_vector = np.mean(mfccs, axis=1)
        
        return feature_vector
    
    except Exception as e:
        raise Exception(f"Error extracting features: {str(e)}")


def process_audio_full_pipeline(audio_file, expected_sentence=None):
    """
    Run the full audio processing pipeline.
    
    Args:
        audio_file: Audio file to process
        expected_sentence: Optional expected sentence for comparison
    
    Returns:
        dict: Complete processing results
    """
    try:
        # Step 1: Preprocess audio
        audio_array, sr = preprocess_audio(audio_file)
        
        # Step 2: Transcribe audio
        transcription = transcribe_audio(audio_array, sr)
        
        # Step 3: Convert expected or transcribed text to phonemes
        text_for_phonemes = expected_sentence if expected_sentence else transcription
        phonemes = text_to_phonemes(text_for_phonemes)
        
        # Step 4: Align phonemes to audio
        alignments = align_phonemes_to_audio(audio_array, phonemes, sr)
        
        # Step 5: Extract features for each phoneme
        for alignment in alignments:
            features = extract_phoneme_features(
                alignment['audio_segment'],
                alignment['sample_rate']
            )
            alignment['features'] = features
        
        # Return comprehensive results
        return {
            'success': True,
            'audio_array': audio_array,
            'sample_rate': sr,
            'transcription': transcription,
            'phonemes': phonemes,
            'alignments': alignments,
            'audio_duration': len(audio_array) / sr
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
