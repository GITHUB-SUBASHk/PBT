# app/otp_utils.py

import random
from datetime import datetime, timedelta

def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP."""
    return ''.join(random.choices("0123456789", k=length))

def otp_expiry(minutes: int = 5) -> datetime:
    """Return an expiry timestamp for the OTP."""
    return datetime.utcnow() + timedelta(minutes=minutes)

def is_otp_valid(stored_otp: str, input_otp: str, expiry_time: datetime) -> bool:
    """Check if OTP is correct and not expired."""
    if stored_otp != input_otp:
        return False
    if datetime.utcnow() > expiry_time:
        return False
    return True
