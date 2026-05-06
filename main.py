from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, projects, skills, experiences, contact
from app.db.database import init_db

app = FastAPI(
    title="Vimalan Portfolio API",
    description="FastAPI backend for Vimalan's Angular portfolio",
    version="1.0.0",
)

# ── CORS (allow Angular dev server) ────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",   # Angular dev server
        "http://localhost:4000",
        "*",                       # Remove in production; use your domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Startup ─────────────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup_event():
    init_db()

# ── Routers ─────────────────────────────────────────────────────────────────
app.include_router(auth.router,        prefix="/api/auth",        tags=["Auth"])
app.include_router(projects.router,    prefix="/api/projects",    tags=["Projects"])
app.include_router(skills.router,      prefix="/api/skills",      tags=["Skills"])
app.include_router(experiences.router, prefix="/api/experiences", tags=["Experiences"])
app.include_router(contact.router,     prefix="/api/contact",     tags=["Contact"])

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Vimalan Portfolio API is running 🚀"}
