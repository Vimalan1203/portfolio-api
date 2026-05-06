from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


# ── Project ──────────────────────────────────────────────────────────────────
class ProjectBase(BaseModel):
    title:       str
    description: str
    tech_stack:  List[str]
    duration:    Optional[str] = None
    highlights:  Optional[List[str]] = []
    category:    str  # government | enterprise | personal
    live_url:    Optional[str] = None
    github_url:  Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectOut(ProjectBase):
    id: int

    class Config:
        from_attributes = True


# ── Skill ────────────────────────────────────────────────────────────────────
class SkillBase(BaseModel):
    category:    str
    name:        str
    proficiency: int = Field(..., ge=0, le=100)
    icon:        str


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    pass


class SkillOut(SkillBase):
    id: int

    class Config:
        from_attributes = True


# ── Experience ───────────────────────────────────────────────────────────────
class ExperienceBase(BaseModel):
    role:       str
    company:    str
    location:   Optional[str] = None
    start_date: Optional[str] = None
    end_date:   Optional[str] = None
    current:    bool = False
    bullets:    Optional[List[str]] = []


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceOut(ExperienceBase):
    id: int

    class Config:
        from_attributes = True


# ── Contact ──────────────────────────────────────────────────────────────────
class ContactMessageIn(BaseModel):
    name:    str = Field(..., min_length=2)
    email:   EmailStr
    subject: str = Field(..., min_length=1)
    message: str = Field(..., min_length=10)


class ContactMessageOut(ContactMessageIn):
    id:         int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Auth ─────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    username: str
    token:    str
    token_type: str = "bearer"
