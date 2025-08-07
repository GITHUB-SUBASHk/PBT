# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    town = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # None until user sets password
    is_verified = Column(Boolean, default=False)     # Changes to True after email verification
    created_at = Column(DateTime, default=datetime.utcnow)


class VerifyToken(Base):
    __tablename__ = "verify_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class ResetOTP(Base):
    __tablename__ = "reset_otps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
