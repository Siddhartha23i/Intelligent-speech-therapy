"""
Supabase Client Configuration

This module handles Supabase connection and provides a singleton client instance.
Supports both local .env files and Streamlit Secrets for deployment.
"""

import os
import streamlit as st
from supabase import create_client, Client

# Single client instance
_supabase_client = None


def get_supabase_credentials():
    """
    Get Supabase credentials from Streamlit Secrets or environment variables.
    
    Returns:
        tuple: (SUPABASE_URL, SUPABASE_KEY)
    """
    # Try Streamlit Secrets first (for Streamlit Share deployment)
    try:
        url = st.secrets.get("SUPABASE_URL")
        key = st.secrets.get("SUPABASE_KEY")
        if url and key:
            return url, key
    except Exception:
        pass
    
    # Fall back to environment variables (for local development)
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    return url, key


def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance.
    
    Returns:
        Client: Supabase client
        
    Raises:
        ValueError: If credentials are not configured
    """
    global _supabase_client
    
    if _supabase_client is None:
        url, key = get_supabase_credentials()
        
        if not url or not key:
            raise ValueError(
                "Supabase credentials not found. "
                "For local development: Create a .env file with SUPABASE_URL and SUPABASE_KEY. "
                "For Streamlit Share: Add secrets in the app settings."
            )
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


def test_connection():
    """
    Test Supabase connection.
    
    Returns:
        bool: True if connection successful
    """
    try:
        client = get_supabase_client()
        # Try a simple query
        result = client.table('user_profiles').select("id").limit(1).execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    test_connection()
