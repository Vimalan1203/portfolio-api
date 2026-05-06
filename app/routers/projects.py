import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.portfolio_models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate, ProjectOut
from app.core.security import verify_token

router = APIRouter()


def _serialize(p: Project) -> ProjectOut:
    return ProjectOut(
        id=p.id,
        title=p.title,
        description=p.description,
        tech_stack=json.loads(p.tech_stack or "[]"),
        duration=p.duration,
        highlights=json.loads(p.highlights or "[]"),
        category=p.category,
        live_url=p.live_url,
        github_url=p.github_url,
    )


# ── Public ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    """Return all projects (public)."""
    return [_serialize(p) for p in db.query(Project).all()]


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return _serialize(p)


# ── Admin (JWT required) ─────────────────────────────────────────────────────

@router.post("/", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    body: ProjectCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    p = Project(
        title=body.title,
        description=body.description,
        tech_stack=json.dumps(body.tech_stack),
        duration=body.duration,
        highlights=json.dumps(body.highlights or []),
        category=body.category,
        live_url=body.live_url,
        github_url=body.github_url,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return _serialize(p)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    body: ProjectUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    p.title       = body.title
    p.description = body.description
    p.tech_stack  = json.dumps(body.tech_stack)
    p.duration    = body.duration
    p.highlights  = json.dumps(body.highlights or [])
    p.category    = body.category
    p.live_url    = body.live_url
    p.github_url  = body.github_url
    db.commit()
    db.refresh(p)
    return _serialize(p)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(p)
    db.commit()
