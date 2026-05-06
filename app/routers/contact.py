from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.portfolio_models import ContactMessage
from app.schemas.schemas import ContactMessageIn, ContactMessageOut
from app.core.security import verify_token

router = APIRouter()


@router.post("/", response_model=ContactMessageOut, status_code=status.HTTP_201_CREATED)
def send_message(body: ContactMessageIn, db: Session = Depends(get_db)):
    """
    Public endpoint — Angular ContactComponent submits here.
    Messages are saved to the DB so admin can view them.
    """
    msg = ContactMessage(
        name=body.name,
        email=body.email,
        subject=body.subject,
        message=body.message,
        created_at=datetime.utcnow().isoformat(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@router.get("/", response_model=List[ContactMessageOut])
def get_messages(
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    """Admin-only — list all received contact messages."""
    return db.query(ContactMessage).order_by(ContactMessage.id.desc()).all()
