from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List
from app.db.database import get_db

router = APIRouter()

Base = declarative_base()


# ── SQLAlchemy Models ──────────────────────────────────────────────────────────

class HeroModel(Base):
    """Stores the main hero section text content."""
    __tablename__ = "hero"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, nullable=False)          # e.g. "Available for opportunities"
    first_name = Column(String, nullable=False)   # e.g. "Vimalan"
    last_name = Column(String, nullable=False)    # e.g. "Senthilkumar"
    description = Column(String, nullable=False)


class RoleModel(Base):
    """Stores the rotating role titles shown in the hero."""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)        # e.g. "Angular Developer"
    order = Column(Integer, nullable=False)       # controls display sequence
    is_active = Column(Boolean, default=True)


class StatModel(Base):
    """Stores the stats shown below the hero description."""
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(String, nullable=False)          # e.g. "3+", "1M+"
    label = Column(String, nullable=False)        # e.g. "Years Experience"
    order = Column(Integer, nullable=False)


# ── Pydantic Schemas ───────────────────────────────────────────────────────────

class HeroSchema(BaseModel):
    tag: str
    first_name: str
    last_name: str
    description: str

    class Config:
        from_attributes = True


class RoleSchema(BaseModel):
    title: str

    class Config:
        from_attributes = True


class StatSchema(BaseModel):
    num: str
    label: str

    class Config:
        from_attributes = True


class HomePageResponse(BaseModel):
    hero: HeroSchema
    roles: List[RoleSchema]
    stats: List[StatSchema]


# ── Route ──────────────────────────────────────────────────────────────────────

@router.get("/", response_model=HomePageResponse)
def get_home_content(db: Session = Depends(get_db)):
    """
    Returns all content needed to render the Angular HomeComponent:
      - hero section (tag, name, description)
      - roles list (for the rotating role text)
      - stats list (the 4 metrics below the description)
    """
    hero = db.query(HeroModel).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero content not found")

    roles = (
        db.query(RoleModel)
        .filter(RoleModel.is_active == True)
        .order_by(RoleModel.order)
        .all()
    )
    if not roles:
        raise HTTPException(status_code=404, detail="No roles found")

    stats = (
        db.query(StatModel)
        .order_by(StatModel.order)
        .all()
    )
    if not stats:
        raise HTTPException(status_code=404, detail="No stats found")

    return HomePageResponse(hero=hero, roles=roles, stats=stats)