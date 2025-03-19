from supabase import create_client
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)


supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase = create_client(supabase_url, supabase_key)