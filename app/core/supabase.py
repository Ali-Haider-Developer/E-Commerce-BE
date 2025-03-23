from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    supabase_url = settings.DATABASE_URL
    supabase_key = settings.DATABASE_API_KEY
    
    if not supabase_url or not supabase_key:
        raise ValueError("Supabase URL and API key must be set")
    
    # Ensure the URL is in the correct format
    if not supabase_url.startswith('https://'):
        supabase_url = f'https://{supabase_url}'
    
    return create_client(supabase_url, supabase_key) 