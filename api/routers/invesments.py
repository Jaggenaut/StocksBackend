from fastapi import APIRouter,HTTPException, Depends
from api.supabase_client import supabase
from utils import get_current_user

router = APIRouter()

@router.get('/investment')
def investments(user_id: str = Depends(get_current_user)):
    try:
        response = supabase.from_("investments").select("*").eq("user_id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching investments.")
