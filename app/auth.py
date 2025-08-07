# app/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uuid

import models, schemas, database, email_utils, otp_utils

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.RegisterResponse)
def register_user(request: schemas.RegisterRequest, db: Session = Depends(get_db)):
    # Check for existing email or username
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(models.User).filter(models.User.username == request.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create user without password (they will set it later)
    new_user = models.User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        dob=request.dob,
        country=request.country,
        state=request.state,
        town=request.town,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create verification token
    token_entry = models.VerifyToken(user_id=new_user.id)
    db.add(token_entry)
    db.commit()

    # Send verification email
    email_utils.send_verification_email(new_user.email, token_entry.token)

    return {"message": "Verification email sent"}

@router.post("/verify-account", response_model=schemas.SetPasswordResponse)
def verify_account(request: schemas.SetPasswordRequest, db: Session = Depends(get_db)):
    token_entry = db.query(models.VerifyToken).filter(models.VerifyToken.token == request.token).first()

    if not token_entry:
        raise HTTPException(status_code=404, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == token_entry.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Set password and verify user
    hashed_password = pwd_context.hash(request.password)
    user.hashed_password = hashed_password
    user.is_verified = True
    db.delete(token_entry)  # remove token after use
    db.commit()

    return {"message": "Account verified and password set"}

@router.post("/login", response_model=schemas.LoginResponse)
def login_user(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    if not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")

    return {"message": "Login successful"}

@router.post("/password-reset-request", response_model=schemas.PasswordResetRequestResponse)
def reset_password_request(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Generate OTP
    otp = otp_utils.generate_otp()
    otp_entry = models.ResetOTP(user_id=user.id, otp=otp)
    db.add(otp_entry)
    db.commit()

    # Send OTP to user's email
    email_utils.send_otp_email(user.email, otp)

    return {"message": "OTP sent to your email"}

@router.post("/password-reset-verify", response_model=schemas.OTPVerifyResponse)
def verify_otp(request: schemas.OTPVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_record = db.query(models.ResetOTP).filter(
        models.ResetOTP.user_id == user.id,
        models.ResetOTP.otp == request.otp
    ).order_by(models.ResetOTP.created_at.desc()).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Check expiration (5 minutes)
    if datetime.utcnow() - otp_record.created_at > timedelta(minutes=5):
        raise HTTPException(status_code=400, detail="OTP expired")

    return {"message": "OTP verified"}

@router.post("/password-reset-confirm", response_model=schemas.PasswordResetConfirmResponse)
def reset_password_confirm(request: schemas.PasswordResetConfirmRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Set new password
    user.hashed_password = pwd_context.hash(request.password)
    db.commit()

    return {"message": "Password reset successful"}
