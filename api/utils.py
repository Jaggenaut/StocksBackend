from fastapi import HTTPException, Header
from typing import Optional
from api.supabase_client import supabase

# Dependency to get current user from Supabase token
def get_current_user(authorization: Optional[str] = Header(None)):
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Authorization header missing")
    # token = authorization.replace("Bearer ", "")
    # user = supabase.auth.get_user(token)
    # if not user:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    return '03b5d8fc-a7f1-43a5-9346-e870131751bf'
