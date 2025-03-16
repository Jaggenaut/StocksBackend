from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, invesments, overlap, sector_allocation

# Initialize the app
app = FastAPI()

# ✅ Allow CORS (Update in Production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(invesments.router)
app.include_router(overlap.router)
app.include_router(sector_allocation.router)

@app.get('/')
def root():
    return {'message':"This is root"}