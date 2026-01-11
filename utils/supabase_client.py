"""
Supabase Client Configuration

This module handles Supabase connection and provides a singleton client instance.
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Single client instance
_supabase_client = None


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
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "Supabase credentials not found. Please create a .env file with "
                "SUPABASE_URL and SUPABASE_KEY."
            )
        
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
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
        result = client.table('users').select("*").limit(1).execute()
        print("✅ Supabase connection successful!")
        return True
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    test_connection()
