from fastapi import APIRouter, HTTPException
from supabase_client import supabase
from schemas.auth import User

router = APIRouter()

@router.post("/register")
def register(user: User):
    try:
        result = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        if result.user:
            return {"message": "User registered successfully"}
        else:
            raise HTTPException(status_code=400, detail="Registration failed")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/login")
def login(user:User):
    try:
        result = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if result.user and result.session:
            return {
                "message": "Login successful",
                "access_token": result.session.access_token
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

