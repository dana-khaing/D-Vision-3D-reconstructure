from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config import settings
from app.database import init_db
from app.routers import events, photos, jobs, viewer, ws


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.ensure_dirs()
    await init_db()
    yield


app = FastAPI(
    title="Memoir3D API",
    description="Event photo → 3D Gaussian Splatting scene with timeline scrubber",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(events.router, prefix="/api/v1")
app.include_router(photos.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(viewer.router)
app.include_router(ws.router)


@app.get("/health")
async def health():
    return {"status": "ok", "env": settings.app_env}


# Serve frontend build in production
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
