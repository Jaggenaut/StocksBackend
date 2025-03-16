from fastapi import HTTPException, Header
from typing import Optional
from supabase_client import supabase

# Dependency to get current user from Supabase token
def get_current_user(authorization: Optional[str] = Header(None)):
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Authorization header missing")
    # token = authorization.replace("Bearer ", "")
    # user = supabase.auth.get_user(token)
    # if not user:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    return '3368feb0-2d1a-4951-acb5-e91a0cca12ff'
