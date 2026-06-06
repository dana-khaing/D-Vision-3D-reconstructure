# D-Vision-3D-Reconstructure

**Memoir3D** — Upload everyone's party photos. Get a navigable 3D memory you can explore from any angle, at any moment of the night.

## What It Does

Takes crowd-sourced photos from a party or event (different phones, angles, lighting, timestamps) and reconstructs a navigable 3D Gaussian Splatting scene with a timeline scrubber — so you can fly around the venue in a browser and scrub through time.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI + uvicorn |
| Job Queue | ARQ (async Redis queue) |
| Database | SQLite (dev) → PostgreSQL (cloud) |
| SfM | COLMAP / pycolmap (Metal-native on Apple Silicon) |
| Person Masking | SAM2 + YOLOv8n (MPS) |
| 3D Reconstruction | OpenSplat (Metal-native) |
| Frontend | React 18 + Vite 5 + Three.js |
| 3D Viewer | @mkkellogg/gaussian-splats-3d |

## Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/dana-khaing/D-Vision-3D-reconstructure
cd D-Vision-3D-reconstructure

# 2. Copy env
cp .env.example .env
# Edit .env with your paths

# 3. Install Python deps
pip install -e ".[dev]"

# 4. Install frontend deps
cd frontend && npm install && cd ..

# 5. Start Redis
brew services start redis

# 6. Run all services
pip install honcho && honcho start
```

API → http://localhost:8000 · Frontend → http://localhost:5173 · Docs → http://localhost:8000/docs

## Project Structure

```
D-Vision-3D-reconstructure/
├── app/              # FastAPI application
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/       # SQLModel DB models
│   ├── routers/      # API route handlers
│   └── services/     # Business logic
├── worker/           # ARQ background worker
│   ├── settings.py
│   ├── pipeline.py   # Main ML orchestrator
│   └── stages/       # COLMAP, SAM2, OpenSplat, export
├── pipeline/         # Phase 0 standalone test scripts
├── frontend/         # React + Vite + Three.js
├── tests/
├── docs/             # Project proposal and insight PDFs
└── alembic/          # DB migrations
```

## Phase 0 — Validate Your Hardware First

Before building any product code, prove the ML pipeline works on your Mac mini:

```bash
cd pipeline
python 00_env_check.py        # verify all tools installed + MPS working
python 01_colmap_test.py      # run COLMAP on ETH3D test dataset
python 02_opensplat_test.py   # train a Gaussian Splat from COLMAP output
python 03_sam2_test.py        # test SAM2 person masking on sample images
```

See `docs/D-Vision-3D-Project-Proposal.pdf` for the full 40-week build roadmap.
