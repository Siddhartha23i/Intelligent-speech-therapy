"""
Feedback Generation Module for Speech Therapy Platform

This module converts pronunciation scores into user-friendly feedback:
- Generating encouragement based on scores
- Creating detailed error descriptions
- Formatting feedback for display
"""

import json
import os
from typing import Dict, List


def load_phoneme_info():
    """
    Load phoneme information from JSON file.
    
    Returns:
        dict: Phoneme information dictionary
    """
    phoneme_file = 'data/phoneme_mapping.json'
    
    if os.path.exists(phoneme_file):
        with open(phoneme_file, 'r') as f:
            data = json.load(f)
            return data.get('phoneme_info', {})
    
    return {}


def generate_feedback(score_data, transcription, original_sentence):
    """
    Generate comprehensive feedback from scoring data.
    
    Args:
        score_data: Dictionary with pronunciation scores
        transcription: What the user actually said
        original_sentence: What they were supposed to say
    
    Returns:
        dict: Feedback dictionary with encouragement and specific errors
    """
    overall_score = score_data.get('overall_score', 0)
    weak_phonemes = score_data.get('weak_phonemes', [])
    mistakes = score_data.get('mistakes', [])
    fluency_score = score_data.get('fluency_score', 0)
    
    # Generate encouragement based on overall score
    if overall_score >= 90:
        encouragement = "🌟 Excellent pronunciation! You're doing fantastic!"
        level = "expert"
    elif overall_score >= 80:
        encouragement = "👏 Great job! Your pronunciation is very good!"
        level = "advanced"
    elif overall_score >= 70:
        encouragement = "👍 Good work! Just a few areas to polish."
        level = "intermediate"
    elif overall_score >= 60:
        encouragement = "💪 Keep practicing! You're making progress."
        level = "beginner"
    elif overall_score >= 50:
        encouragement = "📚 Don't give up! Focus on the areas highlighted below."
        level = "learning"
    else:
        encouragement = "🎯 Let's work together to improve! Start with the basics."
        level = "starting"
    
    # Compare transcription to original
    transcription_match = transcription.lower().strip() == original_sentence.lower().strip()
    
    # Generate mistakes summary
    mistakes_summary = []
    if mistakes:
        phoneme_info = load_phoneme_info()
        
        for mistake in mistakes[:5]:  # Limit to top 5 mistakes
            phoneme = mistake['phoneme']
            score = mistake['score']
            
            info = phoneme_info.get(phoneme, {})
            examples = info.get('example_words', [])
            tip = info.get('articulation_tip', '')
            
            mistake_text = f"**{phoneme}** sound (score: {score:.1f}/100)"
            if examples:
                mistake_text += f" - as in '{examples[0]}'"
            if tip:
                mistake_text += f"\n  💡 Tip: {tip}"
            
            mistakes_summary.append(mistake_text)
    
    # Generate weak phonemes summary
    weak_summary = []
    if weak_phonemes:
        phoneme_info = load_phoneme_info()
        
        # Count occurrences
        from collections import Counter
        phoneme_counts = Counter(weak_phonemes)
        
        for phoneme, count in phoneme_counts.most_common(5):
            info = phoneme_info.get(phoneme, {})
            examples = info.get('example_words', [])
            
            weak_text = f"**{phoneme}** sound"
            if count > 1:
                weak_text += f" ({count} times)"
            if examples:
                weak_text += f" - practice with: {', '.join(examples[:3])}"
            
            weak_summary.append(weak_text)
    
    # Create word-level errors by comparing sentences
    word_errors = []
    if not transcription_match and original_sentence:
        original_words = original_sentence.lower().split()
        transcribed_words = transcription.lower().split()
        
        # Simple word-by-word comparison
        for i, (orig, trans) in enumerate(zip(original_words, transcribed_words)):
            if orig != trans:
                word_errors.append({
                    'expected': orig,
                    'heard': trans,
                    'position': i
                })
    
    return {
        'encouragement': encouragement,
        'level': level,
        'overall_score': overall_score,
        'fluency_score': fluency_score,
        'transcription_match': transcription_match,
        'mistakes_summary': mistakes_summary,
        'weak_phonemes': weak_summary,
        'word_level_errors': word_errors,
        'total_errors': len(mistakes),
        'improvement_areas': weak_phonemes[:3] if weak_phonemes else []
    }


def format_feedback_for_display(feedback):
    """
    Format feedback dictionary for Streamlit display.
    
    Args:
        feedback: Feedback dictionary from generate_feedback
    
    Returns:
        dict: Formatted strings for display
    """
    # Main encouragement message
    main_message = feedback['encouragement']
    
    # Detailed feedback
    details = []
    
    # Add transcription accuracy
    if feedback['transcription_match']:
        details.append("✅ Your words were transcribed correctly!")
    elif feedback['word_level_errors']:
        details.append("⚠️ Some words were not clearly pronounced:")
        for error in feedback['word_level_errors'][:3]:
            details.append(f"  • Expected: '{error['expected']}', Heard: '{error['heard']}'")
    
    # Add mistakes
    if feedback['mistakes_summary']:
        details.append("\n🔴 **Sounds that need significant improvement:**")
        details.extend([f"  {i+1}. {m}" for i, m in enumerate(feedback['mistakes_summary'])])
    
    # Add weak phonemes
    if feedback['weak_phonemes']:
        details.append("\n🟡 **Sounds to practice more:**")
        details.extend([f"  • {w}" for w in feedback['weak_phonemes']])
    
    # Add positive note
    if feedback['overall_score'] >= 70:
        details.append(f"\n🎉 Great fluency! (Fluency score: {feedback['fluency_score']:.1f}/100)")
    
    return {
        'main_message': main_message,
        'detailed_feedback': '\n'.join(details) if details else 'Keep practicing!',
        'score_emoji': get_score_emoji(feedback['overall_score']),
        'level': feedback['level']
    }


def get_score_emoji(score):
    """
    Get emoji representation of score.
    
    Args:
        score: Overall score (0-100)
    
    Returns:
        str: Emoji
    """
    if score >= 90:
        return "🏆"
    elif score >= 80:
        return "🌟"
    elif score >= 70:
        return "👍"
    elif score >= 60:
        return "💪"
    elif score >= 50:
        return "📚"
    else:
        return "🎯"


def get_improvement_suggestions(weak_phonemes, score_data):
    """
    Generate specific improvement suggestions.
    
    Args:
        weak_phonemes: List of weak phoneme strings
        score_data: Score data dictionary
    
    Returns:
        list: List of actionable suggestions
    """
    suggestions = []
    phoneme_info = load_phoneme_info()
    
    # Get top 3 weakest phonemes
    phoneme_scores = score_data.get('phoneme_scores', [])
    sorted_scores = sorted(phoneme_scores, key=lambda x: x['score'])
    
    for phoneme_data in sorted_scores[:3]:
        phoneme = phoneme_data['phoneme']
        score = phoneme_data['score']
        
        info = phoneme_info.get(phoneme, {})
        
        suggestion = {
            'phoneme': phoneme,
            'score': score,
            'description': info.get('description', ''),
            'examples': info.get('example_words', []),
            'tip': info.get('articulation_tip', ''),
            'ipa': info.get('ipa', '')
        }
        
        suggestions.append(suggestion)
    
    return suggestions
