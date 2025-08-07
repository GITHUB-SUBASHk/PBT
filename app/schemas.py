# app/schemas.py

from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import date

# ------------- REGISTER ------------- #
class RegisterRequest(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=20)
    first_name: str
    last_name: str
    dob: date
    country: str
    state: str
    town: str


class RegisterResponse(BaseModel):
    message: str


# ------------- SET PASSWORD AFTER EMAIL LINK ------------- #
class SetPasswordRequest(BaseModel):
    token: str
    password: constr(min_length=8)


class SetPasswordResponse(BaseModel):
    message: str


# ------------- LOGIN ------------- #
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str


# ------------- PASSWORD RESET - REQUEST OTP ------------- #
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetRequestResponse(BaseModel):
    message: str


# ------------- PASSWORD RESET - VERIFY OTP ------------- #
class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class OTPVerifyResponse(BaseModel):
    message: str


# ------------- PASSWORD RESET - SET NEW PASSWORD ------------- #
class PasswordResetConfirmRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class PasswordResetConfirmResponse(BaseModel):
    message: str
