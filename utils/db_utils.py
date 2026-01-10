"""
Database Utilities for Speech Therapy Platform

This module handles all database operations:
- Database initialization
- Session saving
- User history retrieval
- Statistics calculation
"""

import sqlite3
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import os


def get_db_path():
    """Get the database file path."""
    return 'database/user_data.db'


def init_database():
    """
    Initialize the SQLite database with required tables.
    
    Returns:
        sqlite3.Connection: Database connection
    """
    db_path = get_db_path()
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            sentence TEXT,
            transcription TEXT,
            overall_score REAL,
            fluency_score REAL,
            audio_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create phoneme_scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phoneme_scores (
            score_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            phoneme TEXT NOT NULL,
            score REAL NOT NULL,
            error_type TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        )
    ''')
    
    # Create user_weak_phonemes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_weak_phonemes (
            user_id TEXT NOT NULL,
            phoneme TEXT NOT NULL,
            frequency INTEGER DEFAULT 1,
            last_occurrence TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, phoneme),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    return conn


def ensure_user_exists(conn, user_id):
    """
    Ensure user exists in database, create if not.
    
    Args:
        conn: Database connection
        user_id: User identifier
    """
    cursor = conn.cursor()
    
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO users (user_id, created_at, last_active) VALUES (?, ?, ?)',
            (user_id, datetime.now(), datetime.now())
        )
        conn.commit()


def save_session(conn, user_id, sentence, transcription, score_data, audio_path=None):
    """
    Save a practice session to the database.
    
    Args:
        conn: Database connection
        user_id: User identifier
        sentence: Expected sentence
        transcription: User's transcription
        score_data: Dictionary with scoring results
        audio_path: Optional path to saved audio file
    
    Returns:
        int: Session ID
    """
    cursor = conn.cursor()
    
    # Ensure user exists
    ensure_user_exists(conn, user_id)
    
    # Insert session
    cursor.execute('''
        INSERT INTO sessions (user_id, timestamp, sentence, transcription, 
                            overall_score, fluency_score, audio_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datetime.now(),
        sentence,
        transcription,
        score_data.get('overall_score', 0),
        score_data.get('fluency_score', 0),
        audio_path
    ))
    
    session_id = cursor.lastrowid
    
    # Insert phoneme scores
    phoneme_scores = score_data.get('phoneme_scores', [])
    for phoneme_data in phoneme_scores:
        cursor.execute('''
            INSERT INTO phoneme_scores (session_id, phoneme, score, error_type)
            VALUES (?, ?, ?, ?)
        ''', (
            session_id,
            phoneme_data['phoneme'],
            phoneme_data['score'],
            None  # error_type can be added later
        ))
    
    # Update weak phonemes
    weak_phonemes = score_data.get('weak_phonemes', [])
    for phoneme in weak_phonemes:
        cursor.execute('''
            INSERT INTO user_weak_phonemes (user_id, phoneme, frequency, last_occurrence)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(user_id, phoneme) 
            DO UPDATE SET 
                frequency = frequency + 1,
                last_occurrence = ?
        ''', (user_id, phoneme, datetime.now(), datetime.now()))
    
    # Update user last_active
    cursor.execute('''
        UPDATE users SET last_active = ? WHERE user_id = ?
    ''', (datetime.now(), user_id))
    
    conn.commit()
    return session_id


def get_user_history(conn, user_id, limit=50):
    """
    Get user's practice session history.
    
    Args:
        conn: Database connection
        user_id: User identifier
        limit: Maximum number of sessions to retrieve
    
    Returns:
        pandas.DataFrame: Session history
    """
    query = '''
        SELECT session_id, timestamp, sentence, transcription, 
               overall_score, fluency_score
        FROM sessions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    '''
    
    df = pd.read_sql_query(query, conn, params=(user_id, limit))
    
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df


def get_phoneme_statistics(conn, user_id):
    """
    Calculate statistics for each phoneme practiced by user.
    
    Args:
        conn: Database connection
        user_id: User identifier
    
    Returns:
        dict: Dictionary with phoneme statistics
    """
    query = '''
        SELECT ps.phoneme, 
               AVG(ps.score) as average_score,
               COUNT(*) as count,
               MIN(ps.score) as min_score,
               MAX(ps.score) as max_score
        FROM phoneme_scores ps
        JOIN sessions s ON ps.session_id = s.session_id
        WHERE s.user_id = ?
        GROUP BY ps.phoneme
        ORDER BY average_score ASC
    '''
    
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    
    stats = {}
    for row in cursor.fetchall():
        phoneme, avg_score, count, min_score, max_score = row
        stats[phoneme] = {
            'average_score': round(avg_score, 1),
            'count': count,
            'min_score': round(min_score, 1),
            'max_score': round(max_score, 1)
        }
    
    return stats


def get_weak_phonemes_history(conn, user_id):
    """
    Get user's weak phonemes history.
    
    Args:
        conn: Database connection
        user_id: User identifier
    
    Returns:
        dict: Dictionary of weak phonemes with frequencies
    """
    query = '''
        SELECT phoneme, frequency, last_occurrence
        FROM user_weak_phonemes
        WHERE user_id = ?
        ORDER BY frequency DESC
    '''
    
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    
    weak_phonemes = {}
    for row in cursor.fetchall():
        phoneme, frequency, last_occurrence = row
        weak_phonemes[phoneme] = {
            'frequency': frequency,
            'last_occurrence': last_occurrence
        }
    
    return weak_phonemes


def get_latest_session(conn, user_id):
    """
    Get user's most recent session.
    
    Args:
        conn: Database connection
        user_id: User identifier
    
    Returns:
        dict: Latest session data or None
    """
    query = '''
        SELECT session_id, timestamp, sentence, transcription, 
               overall_score, fluency_score
        FROM sessions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
    '''
    
    cursor = conn.cursor()
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    
    if row:
        return {
            'session_id': row[0],
            'timestamp': row[1],
            'sentence': row[2],
            'transcription': row[3],
            'overall_score': row[4],
            'fluency_score': row[5]
        }
    
    return None


def delete_user_data(conn, user_id):
    """
    Delete all data for a specific user (GDPR compliance).
    
    Args:
        conn: Database connection
        user_id: User identifier
    
    Returns:
        bool: Success status
    """
    cursor = conn.cursor()
    
    try:
        # Delete phoneme scores for user's sessions
        cursor.execute('''
            DELETE FROM phoneme_scores 
            WHERE session_id IN (SELECT session_id FROM sessions WHERE user_id = ?)
        ''', (user_id,))
        
        # Delete sessions
        cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
        
        # Delete weak phonemes
        cursor.execute('DELETE FROM user_weak_phonemes WHERE user_id = ?', (user_id,))
        
        # Delete user
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        
        conn.commit()
        return True
    
    except Exception as e:
        conn.rollback()
        print(f"Error deleting user data: {e}")
        return False


def get_user_statistics(conn, user_id):
    """
    Get comprehensive user statistics.
    
    Args:
        conn: Database connection
        user_id: User identifier
    
    Returns:
        dict: User statistics
    """
    cursor = conn.cursor()
    
    # Total sessions
    cursor.execute('SELECT COUNT(*) FROM sessions WHERE user_id = ?', (user_id,))
    total_sessions = cursor.fetchone()[0]
    
    # Average score
    cursor.execute('''
        SELECT AVG(overall_score), AVG(fluency_score) 
        FROM sessions WHERE user_id = ?
    ''', (user_id,))
    avg_scores = cursor.fetchone()
    avg_overall = avg_scores[0] if avg_scores[0] else 0
    avg_fluency = avg_scores[1] if avg_scores[1] else 0
    
    # Best score
    cursor.execute('''
        SELECT MAX(overall_score) FROM sessions WHERE user_id = ?
    ''', (user_id,))
    best_score = cursor.fetchone()[0] or 0
    
    # Total practice time (estimate: 30 seconds per session)
    total_practice_minutes = total_sessions * 0.5
    
    return {
        'total_sessions': total_sessions,
        'average_overall_score': round(avg_overall, 1),
        'average_fluency_score': round(avg_fluency, 1),
        'best_score': round(best_score, 1),
        'total_practice_time': f"{total_practice_minutes:.1f} minutes"
    }
