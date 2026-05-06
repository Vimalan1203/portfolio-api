from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import LoginRequest, TokenResponse
from app.core.security import create_token, verify_password
from app.db.database import get_db
from app.models.portfolio_models import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user from database and return a JWT token.
    """
    user = db.query(User).filter(User.username == body.username).first()

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled",
        )

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    token = create_token(user.username)
    return TokenResponse(username=user.username, token=token)


@router.post("/logout")
def logout():
    """Angular handles logout client-side; this endpoint is a no-op placeholder."""
    return {"message": "Logged out successfully"}

