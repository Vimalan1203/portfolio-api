from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(100), unique=True, nullable=False, index=True)
    email           = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin        = Column(Boolean, default=False)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(String(50))


class Project(Base):
    __tablename__ = "projects"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack  = Column(Text, nullable=False)  # JSON list
    duration    = Column(String(100))
    highlights  = Column(Text)                  # JSON list
    category    = Column(String(50), nullable=False)  # government | enterprise | personal
    live_url    = Column(String(300), nullable=True)
    github_url  = Column(String(300), nullable=True)


class Skill(Base):
    __tablename__ = "skills"

    id          = Column(Integer, primary_key=True, index=True)
    category    = Column(String(100), nullable=False)
    name        = Column(String(100), nullable=False)
    proficiency = Column(Integer, nullable=False)   # 0-100
    icon        = Column(String(10), nullable=False)


class Experience(Base):
    __tablename__ = "experiences"

    id         = Column(Integer, primary_key=True, index=True)
    role       = Column(String(150), nullable=False)
    company    = Column(String(150), nullable=False)
    location   = Column(String(150))
    start_date = Column(String(50))
    end_date   = Column(String(50), nullable=True)
    current    = Column(Boolean, default=False)
    bullets    = Column(Text)   # JSON list


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(200), nullable=False)
    subject    = Column(String(200), nullable=False)
    message    = Column(Text, nullable=False)
    created_at = Column(String(50))
