from fastapi import APIRouter, HTTPException, Depends
from api.supabase_client import supabase
from api.utils import get_current_user

router = APIRouter()

@router.get('/investment')
def investments(user_id: str = Depends(get_current_user)):
    try:
        response = (
            supabase.from_("investments")
            .select("*, mutual_funds(name)")
            .eq("user_id", user_id)
            .execute()
        )

        if response.data:
            return {"status": "success", "data": response.data}
        else:
            return {"status": "success", "data": [], "message": "No investments found"}
    except HTTPException as http_err:
        raise http_err  # Forward known HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": "An unexpected error occurred while fetching investments."})
