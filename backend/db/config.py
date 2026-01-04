"""
Database configuration and utilities
"""

import os
from typing import Optional
from supabase import create_client, Client


class Database:
    """Database connection manager for Supabase"""
    
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client singleton"""
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError(
                    "SUPABASE_URL and SUPABASE_KEY environment variables must be set"
                )
            
            cls._instance = create_client(url, key)
        
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the client (useful for testing)"""
        cls._instance = None
