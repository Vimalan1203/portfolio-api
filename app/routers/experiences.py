import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from sqlalchemy import desc
from app.models.portfolio_models import Experience
from app.schemas.schemas import ExperienceCreate, ExperienceOut
from app.core.security import verify_token

router = APIRouter()


def _serialize(e: Experience) -> ExperienceOut:
    return ExperienceOut(
        id=e.id,
        role=e.role,
        company=e.company,
        location=e.location,
        start_date=e.start_date,
        end_date=e.end_date,
        current=e.current,
        bullets=json.loads(e.bullets or "[]"),
    )


@router.get("/", response_model=List[ExperienceOut])
def get_experiences(db: Session = Depends(get_db)):
    experiences = (
        db.query(Experience)
        .order_by(
            desc(Experience.current),
            desc(Experience.start_date),
            desc(Experience.end_date),
        )
        .all()
    )
    return [_serialize(e) for e in experiences]


@router.post("/", response_model=ExperienceOut, status_code=status.HTTP_201_CREATED)
def create_experience(
    body: ExperienceCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    e = Experience(
        role=body.role,
        company=body.company,
        location=body.location,
        start_date=body.start_date,
        end_date=body.end_date,
        current=body.current,
        bullets=json.dumps(body.bullets or []),
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return _serialize(e)


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    e = db.query(Experience).filter(Experience.id == experience_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(e)
    db.commit()
