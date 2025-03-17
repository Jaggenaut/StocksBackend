from fastapi import APIRouter, HTTPException, Depends
from api.supabase_client import supabase
from api.schemas.auth import User

router = APIRouter()

@router.post("/register")
def register(user: User):
    try:
        result = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        if result.user:
            return {"status": "success", "data": {"message": "User registered successfully"}}
        else:
            raise HTTPException(status_code=400, detail="Registration failed")

    except HTTPException as http_err:
        raise http_err  # Forward known HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(e)})


@router.post("/login")
def login(user: User):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if result.user and result.session:
            return {
                "status": "success",
                "data": {
                    "message": "Login successful",
                    "access_token": result.session.access_token
                }
            }
        else:
            raise HTTPException(status_code=401, detail={"status": "error", "message": "Invalid email or password"})
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(e)})
