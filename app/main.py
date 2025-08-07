# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import database
import auth

# FastAPI app instance
app = FastAPI()

# CORS: Allow your React frontend to talk to backend
origins = [
    "http://localhost:3000"  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth routes from auth.py (to be created next)
app.include_router(auth.router)

# This is just a simple health check endpoint
@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
    
# Create DB tables on startup
@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)
