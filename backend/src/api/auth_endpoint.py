"""
Mock authentication endpoints for MVP.
Phase III-C: Authentication disabled - these are placeholder endpoints.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime, timedelta

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    user: dict
    session_token: str
    expires_at: str


@router.post("/v1/auth/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    Mock login endpoint - returns dummy session for MVP.
    TODO: Implement real authentication in production.
    """
    # For MVP, accept any credentials
    user_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()

    return AuthResponse(
        user={
            "user_id": user_id,
            "email": request.email,
        },
        session_token=session_token,
        expires_at=expires_at,
    )


@router.post("/v1/auth/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """
    Mock signup endpoint - returns dummy session for MVP.
    TODO: Implement real user registration in production.
    """
    # For MVP, accept any credentials
    user_id = str(uuid.uuid4())
    session_token = str(uuid.uuid4())
    expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()

    return AuthResponse(
        user={
            "user_id": user_id,
            "email": request.email,
        },
        session_token=session_token,
        expires_at=expires_at,
    )


@router.post("/v1/auth/logout")
async def logout():
    """
    Mock logout endpoint - does nothing for MVP.
    TODO: Implement session invalidation in production.
    """
    return {"status": "success", "message": "Logged out successfully"}
