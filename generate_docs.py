"""Generate Project Proposal PDF and Project Insight PDF using ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import datetime

# ── Color palette ──────────────────────────────────────────────────────────────
ACCENT     = colors.HexColor("#7C3AED")
ACCENT2    = colors.HexColor("#06B6D4")
TEXT_LIGHT = colors.HexColor("#F8FAFC")
TEXT_GRAY  = colors.HexColor("#94A3B8")
TABLE_HDR  = colors.HexColor("#1E293B")
TABLE_ROW1 = colors.HexColor("#F1F5F9")
TABLE_ROW2 = colors.HexColor("#FFFFFF")
WARN_RED   = colors.HexColor("#DC2626")
WARN_YLW   = colors.HexColor("#D97706")
GREEN      = colors.HexColor("#16A34A")
BORDER     = colors.HexColor("#334155")
BODY_TEXT  = colors.HexColor("#1E293B")
PHASE_BG   = colors.HexColor("#EDE9FE")


def make_styles():
    styles = getSampleStyleSheet()
    add = styles.add

    add(ParagraphStyle("DocTitle",   parent=styles["Title"],
        fontSize=26, textColor=ACCENT, spaceAfter=6,
        fontName="Helvetica-Bold", alignment=TA_CENTER))
    add(ParagraphStyle("DocSub",
        fontSize=13, textColor=TEXT_GRAY, spaceAfter=20,
        fontName="Helvetica", alignment=TA_CENTER))
    add(ParagraphStyle("Cap",
        fontSize=9, textColor=TEXT_GRAY, spaceAfter=4,
        fontName="Helvetica-Oblique", alignment=TA_CENTER))
    add(ParagraphStyle("H1",
        fontSize=17, textColor=ACCENT, spaceBefore=16, spaceAfter=8,
        fontName="Helvetica-Bold"))
    add(ParagraphStyle("H2",
        fontSize=12, textColor=ACCENT2, spaceBefore=10, spaceAfter=5,
        fontName="Helvetica-Bold"))
    add(ParagraphStyle("H3",
        fontSize=10, textColor=colors.HexColor("#1E40AF"), spaceBefore=7, spaceAfter=3,
        fontName="Helvetica-Bold"))
    add(ParagraphStyle("Body",
        fontSize=9.5, textColor=BODY_TEXT, spaceAfter=5,
        fontName="Helvetica", leading=14, alignment=TA_JUSTIFY))
    add(ParagraphStyle("Bul",
        fontSize=9.5, textColor=BODY_TEXT, spaceAfter=3,
        fontName="Helvetica", leftIndent=14, leading=13))
    add(ParagraphStyle("Warn",
        fontSize=9.5, textColor=WARN_RED, spaceAfter=5,
        fontName="Helvetica-Bold", leftIndent=6))
    # cell styles — smaller, for inside table cells
    add(ParagraphStyle("Cell",
        fontSize=8.5, textColor=BODY_TEXT,
        fontName="Helvetica", leading=12, spaceAfter=0))
    add(ParagraphStyle("CellBold",
        fontSize=8.5, textColor=TEXT_LIGHT,
        fontName="Helvetica-Bold", leading=12, spaceAfter=0))
    add(ParagraphStyle("CellHdr",
        fontSize=9, textColor=TEXT_LIGHT,
        fontName="Helvetica-Bold", leading=13, spaceAfter=0))
    add(ParagraphStyle("CellGreen",
        fontSize=8.5, textColor=GREEN,
        fontName="Helvetica-Bold", leading=12, spaceAfter=0))
    add(ParagraphStyle("CellRed",
        fontSize=8.5, textColor=WARN_RED,
        fontName="Helvetica-Bold", leading=12, spaceAfter=0))
    add(ParagraphStyle("CellOrange",
        fontSize=8.5, textColor=WARN_YLW,
        fontName="Helvetica-Bold", leading=12, spaceAfter=0))
    return styles


def hr(color=ACCENT):
    return HRFlowable(width="100%", thickness=1, color=color, spaceAfter=8, spaceBefore=3)


def p(text, style):
    """Convenience: wrap text in Paragraph for table cells."""
    return Paragraph(text, style)


def base_table_style():
    return TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  TABLE_HDR),
        ("ROWBACKGROUNDS",(0,1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID",         (0, 0), (-1, -1), 0.35, BORDER),
        ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",   (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
        ("LEFTPADDING",  (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ])


# ══════════════════════════════════════════════════════════════════════════════
# PDF 1 — PROJECT PROPOSAL
# ══════════════════════════════════════════════════════════════════════════════

def build_proposal(path, S):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="D-Vision-3D-Reconstructure — Project Proposal",
        author="Dana Khaing",
    )
    story = []

    # Cover
    story += [
        Spacer(1, 1.5*cm),
        Paragraph("D-Vision-3D-Reconstructure", S["DocTitle"]),
        Paragraph("Memoir3D · Project Proposal & Build Roadmap", S["DocSub"]),
        Paragraph(f"Prepared by Dana Khaing · {datetime.date.today().strftime('%B %d, %Y')}", S["Cap"]),
        Spacer(1, 0.4*cm), hr(ACCENT),
    ]

    # Overview
    story += [
        Paragraph("Project Overview", S["H1"]),
        Paragraph(
            "D-Vision-3D-Reconstructure (product name: <b>Memoir3D</b>) transforms crowd-sourced "
            "event photos — taken by multiple attendees with different phones, angles, lighting, "
            "and timestamps — into a single navigable 3D scene with a timeline scrubber. "
            "The user can fly around the venue in a browser and scrub through time to relive "
            "any moment of the party.", S["Body"]),
        Paragraph(
            "<b>Market gap:</b> No existing tool (Luma AI, Polycam, Scaniverse) handles "
            "crowd-sourced multi-attendee photos with a temporal layer. The research foundation "
            "(WildGaussians NeurIPS 2024, CSS arXiv 2409.08562) is mature enough to build on.", S["Body"]),
        Spacer(1, 0.2*cm),
    ]

    # Tech Stack — Backend
    story += [Paragraph("Definitive Tech Stack", S["H1"]), hr()]
    story.append(Paragraph("Backend (Python)", S["H2"]))
    be = [
        [p("Package", S["CellHdr"]),     p("Version", S["CellHdr"]),  p("Role", S["CellHdr"])],
        [p("FastAPI", S["Cell"]),         p("0.115+", S["Cell"]),  p("REST API + WebSocket server", S["Cell"])],
        [p("ARQ", S["Cell"]),             p("0.26+", S["Cell"]),   p("Async Redis job queue — avoids MPS GPU context fork issues", S["Cell"])],
        [p("SQLModel", S["Cell"]),        p("0.0.21+", S["Cell"]), p("ORM — single model for SQLite (local) + PostgreSQL (cloud)", S["Cell"])],
        [p("Alembic", S["Cell"]),         p("1.13+", S["Cell"]),   p("Database migrations", S["Cell"])],
        [p("redis[asyncio]", S["Cell"]),  p("5.0+", S["Cell"]),    p("Job queue + PubSub for live pipeline progress events", S["Cell"])],
        [p("Pillow + piexif", S["Cell"]), p("10+", S["Cell"]),     p("Thumbnails, EXIF timestamp + focal length extraction", S["Cell"])],
    ]
    t = Table(be, colWidths=[3.5*cm, 2.2*cm, 10.3*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.25*cm)]

    # ML Stack
    story.append(Paragraph("ML Pipeline — Apple Silicon (Metal / MPS)", S["H2"]))
    ml = [
        [p("Tool", S["CellHdr"]),                      p("Role", S["CellHdr"]),                              p("Apple Silicon", S["CellHdr"])],
        [p("COLMAP / pycolmap", S["Cell"]),             p("Camera pose estimation (SfM)", S["Cell"]),         p("Metal-native via brew install", S["CellGreen"])],
        [p("hloc SuperPoint+SuperGlue", S["Cell"]),     p("Feature matching for dark/party photos", S["Cell"]),p("MPS supported", S["CellGreen"])],
        [p("SAM2 (Meta)", S["Cell"]),                   p("Person masking per photo", S["Cell"]),             p("MPS with PYTORCH_ENABLE_MPS_FALLBACK=1", S["CellGreen"])],
        [p("YOLOv8n (ultralytics)", S["Cell"]),         p("Person bounding boxes to prompt SAM2", S["Cell"]), p("MPS supported", S["CellGreen"])],
        [p("Depth Anything v2 Small", S["Cell"]),       p("Depth hints — Apache 2.0 license", S["Cell"]),     p("MPS + Core ML", S["CellGreen"])],
        [p("OpenSplat", S["Cell"]),                     p("3D Gaussian Splatting training", S["Cell"]),       p("Metal-native build required", S["CellGreen"])],
    ]
    t = Table(ml, colWidths=[4.5*cm, 5.5*cm, 6*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.25*cm)]

    # Frontend
    story.append(Paragraph("Frontend (React / TypeScript)", S["H2"]))
    fe = [
        [p("Package", S["CellHdr"]),                            p("Role", S["CellHdr"])],
        [p("React 18 + Vite 5", S["Cell"]),                     p("SPA — not Next.js (no SSR needed, simpler build)", S["Cell"])],
        [p("Three.js 0.169+", S["Cell"]),                       p("3D renderer core", S["Cell"])],
        [p("@mkkellogg/gaussian-splats-3d", S["Cell"]),         p("Best maintained WebGL Gaussian Splatting renderer for Three.js", S["Cell"])],
        [p("Zustand 4.5+", S["Cell"]),                          p("Minimal state management (viewer state, job state, camera)", S["Cell"])],
        [p("Tailwind CSS 4 + shadcn/ui", S["Cell"]),            p("Utility styling + accessible Radix-based components", S["Cell"])],
        [p("axios + react-dropzone", S["Cell"]),                p("File upload with progress events + drag-drop support", S["Cell"])],
    ]
    t = Table(fe, colWidths=[5.5*cm, 10.5*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.3*cm), PageBreak()]

    # ML Pipeline Flow
    story += [Paragraph("ML Pipeline — Full Data Flow", S["H1"]), hr()]
    story.append(Paragraph(
        "All stages run sequentially. Each stage writes a checkpoint file so failed or "
        "cancelled jobs resume from the last completed stage automatically.", S["Body"]))
    story.append(Spacer(1, 0.15*cm))

    pipe = [
        [p("Step", S["CellHdr"]),               p("Script", S["CellHdr"]),         p("Time (300 photos)", S["CellHdr"]), p("Output", S["CellHdr"])],
        [p("1 — Ingest & Validate", S["Cell"]),  p("01_ingest.py", S["Cell"]),      p("~5 sec", S["Cell"]),  p("processed_images/, metadata.json", S["Cell"])],
        [p("2 — Temporal Bucketing", S["Cell"]), p("02_bucket.py", S["Cell"]),      p("<1 sec", S["Cell"]),  p("buckets.json (15-min sliding windows)", S["Cell"])],
        [p("3 — COLMAP Full Event", S["Cell"]),  p("03_colmap_full.py", S["Cell"]), p("20–90 min", S["Cell"]),p("sparse/0/ — camera poses for all photos", S["Cell"])],
        [p("4 — SAM2 Masking", S["Cell"]),       p("04_mask.py", S["Cell"]),        p("5–15 min", S["Cell"]), p("masks/*.png (255 = exclude people)", S["Cell"])],
        [p("5 — Window Sub-Recon", S["Cell"]),   p("05_window_recon.py", S["Cell"]),p("<1 min", S["Cell"]),   p("windows/{id}/sparse/0/ with anchor photos", S["Cell"])],
        [p("6 — OpenSplat Training", S["Cell"]), p("06_train_windows.py", S["Cell"]),p("~17 min/window", S["Cell"]),p("{bucket_id}.ply per time window", S["Cell"])],
        [p("7 — Post-Processing", S["Cell"]),    p("07_postprocess.py", S["Cell"]), p("~2 min", S["Cell"]),   p("scene.json + LOD preview.ply (<5 MB)", S["Cell"])],
    ]
    t = Table(pipe, colWidths=[3.5*cm, 3.8*cm, 3*cm, 5.7*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.25*cm)]

    # Key settings
    story += [
        Paragraph("Key COLMAP Settings for Party Photos", S["H3"]),
        Paragraph("• <b>domain_size_pooling=True</b> — biggest win for dark/low-texture scenes", S["Bul"]),
        Paragraph("• <b>max_num_features=16384</b> — double default to survive noise and blur", S["Bul"]),
        Paragraph("• <b>camera_mode=PER_IMAGE</b> — critical for mixed phones from different manufacturers", S["Bul"]),
        Paragraph("• <b>hloc SuperPoint+SuperGlue</b> — replace SIFT matching for 2–3× more matched pairs", S["Bul"]),
        Spacer(1, 0.15*cm),
        Paragraph("Key OpenSplat Parameters", S["H3"]),
        Paragraph("• <b>max_gaussians=1,000,000</b> — hard cap to stay within 24 GB unified memory", S["Bul"]),
        Paragraph("• <b>sh_degree=3</b> — full spherical harmonics; reduce to 1 if OOM on first attempt", S["Bul"]),
        Paragraph("• <b>iterations=30,000</b> — approximately 17 minutes on M-series with Metal GPU", S["Bul"]),
        Paragraph("• <b>masks directory enabled</b> — pass SAM2 mask folder to exclude people from training", S["Bul"]),
        Spacer(1, 0.3*cm), PageBreak(),
    ]

    # Phases
    story += [Paragraph("Phase-by-Phase Build Plan", S["H1"]), hr()]
    phases = [
        ("Phase 0 — Proof of Concept", "Weeks 1–3",
         ["Install pycolmap, OpenSplat, SAM2. Run COLMAP on ETH3D dataset. Benchmark every stage.",
          "Take 50–100 photos of your own room. Run full COLMAP → OpenSplat pipeline.",
          "View resulting .ply in Supersplat. Document real processing times on your Mac mini.",
          "⚠ This phase CANNOT be skipped. All product decisions depend on these real numbers."]),
        ("Phase 1 — Single-Event Pipeline", "Weeks 4–8",
         ["Build pipeline.py: COLMAP → SAM2 → OpenSplat as subprocess chain with per-stage logging.",
          "FastAPI skeleton: upload endpoint, job trigger, ARQ background worker.",
          "Redis PubSub progress events. Job status polling via GET /jobs/{id}.",
          "Run pipeline 5× with varied photo sets. Fix every crash. Add timeout handling."]),
        ("Phase 2 — Browser 3D Viewer", "Weeks 9–13",
         ["React + Vite + Three.js scaffold. gaussian-splats-3d renderer. Load static .ply.",
          "OrbitControls, keyboard shortcuts, HTTP range request streaming.",
          "Safari / iOS compatibility. M3 milestone: navigable scene in 3 browsers."]),
        ("Phase 3 — Timeline Layer  ⚠ Highest Risk", "Weeks 14–20 + 4-week buffer",
         ["Week 14: Research sprint ONLY — read CSS paper (arXiv 2409.08562) + WildGaussians. No code.",
          "EXIF extraction, clock drift detection, 15-minute time-window bucketing.",
          "SAM2 batch inference on real event photos. Benchmark mask quality.",
          "Per-window sub-reconstructions anchored to full-event COLMAP coordinate frame.",
          "Timeline scrubber React component. 0.4s cross-fade between window transitions."]),
        ("Phase 4 — Photo Collection UX", "Weeks 21–26",
         ["Event creation UI + shareable URL + QR code generation.",
          "Mobile-optimized upload page: iOS HEIC→JPEG conversion, EXIF orientation fix.",
          "Resumable uploads, perceptual hash deduplication, coverage heatmap.",
          "Test: 3 real non-developers successfully upload without asking for help."]),
        ("Phase 5 — MVP Polish & Real Event Test", "Weeks 27–32",
         ["WebSocket live progress UI showing all 6 pipeline stages. Email notifications.",
          "Error handling audit: every failure produces a user-facing message + action.",
          "500-photo stress test. Profile and fix pipeline bottlenecks.",
          "Week 31: USE AT A REAL EVENT. Document every breakage. Fix top issues."]),
        ("Phase 6 — Production Quality", "Weeks 33–40",
         ["SQLite → PostgreSQL migration (Alembic). Docker container.",
          "Cloud deploy on Railway or Fly.io. Cloudflare R2 for .ply storage.",
          "Sentry error monitoring. Uptime alerts. UI redesign from real user feedback."]),
    ]
    for title, timeline, bullets in phases:
        hdr_row = [[p(f"<b>{title}</b>", S["H3"]), p(timeline, S["Body"])]]
        bullet_rows = [[p(f"• {b}", S["Bul"]), p("", S["Cell"])] for b in bullets]
        t = Table(hdr_row + bullet_rows, colWidths=[13.5*cm, 2.5*cm])
        ts = TableStyle([
            ("BACKGROUND",   (0, 0), (-1, 0),  PHASE_BG),
            ("GRID",         (0, 0), (-1, -1), 0.3, BORDER),
            ("SPAN",         (0, 1), (-1, -1)),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 4),
            ("LEFTPADDING",  (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ])
        t.setStyle(ts)
        story += [t, Spacer(1, 0.15*cm)]
    story.append(Spacer(1, 0.2*cm))

    # Milestones
    story.append(Paragraph("Milestones Summary", S["H2"]))
    ms = [
        [p("#", S["CellHdr"]),  p("Milestone", S["CellHdr"]),         p("Target Week", S["CellHdr"]), p("Key Success Criteria", S["CellHdr"])],
        [p("M0", S["Cell"]),    p("Environment working", S["Cell"]),   p("3", S["Cell"]),    p("All tools install; real benchmark times documented on your Mac mini", S["Cell"])],
        [p("M1", S["Cell"]),    p("First reconstruction", S["Cell"]),  p("2–3", S["Cell"]),  p("Your room photos → viewable .ply file in Supersplat", S["Cell"])],
        [p("M2", S["Cell"]),    p("Pipeline API complete", S["Cell"]), p("8", S["Cell"]),    p("curl upload → .ply via API; pipeline handles errors without crashing", S["Cell"])],
        [p("M3", S["Cell"]),    p("Browser viewer", S["Cell"]),        p("13", S["Cell"]),   p("3DGS scene navigable in Chrome + Safari + Android Chrome", S["Cell"])],
        [p("M4", S["Cell"]),    p("Timeline scrubber", S["Cell"]),     p("20 ±4", S["Cell"]),p("Scrubbing the timeline causes visible changes in the 3D scene", S["Cell"])],
        [p("M5", S["Cell"]),    p("Multi-contributor UX", S["Cell"]),  p("26", S["Cell"]),   p("3 non-developers successfully upload photos without your help", S["Cell"])],
        [p("M6", S["Cell"]),    p("MVP at real event", S["Cell"]),     p("32", S["Cell"]),   p("Real guests open result; no manual intervention required", S["Cell"])],
        [p("M7", S["Cell"]),    p("Production quality", S["Cell"]),    p("40", S["Cell"]),   p("Cloud deployed; strangers can use it without your assistance", S["Cell"])],
    ]
    t = Table(ms, colWidths=[1*cm, 4*cm, 2.5*cm, 8.5*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.3*cm), PageBreak()]

    # Risks
    story += [Paragraph("Critical Risks & Mitigations", S["H1"]), hr()]
    risks = [
        [p("Risk", S["CellHdr"]),                                       p("P", S["CellHdr"]), p("I", S["CellHdr"]),    p("Mitigation & Contingency", S["CellHdr"])],
        [p("COLMAP fails on dark/blurry party photos", S["Cell"]),      p("High", S["CellRed"]),    p("Critical", S["CellRed"]),  p("Blur rejection gate (Laplacian < 50), hloc SuperGlue matcher, domain_size_pooling=True. Contingency: show coverage heatmap, prompt for more photos.", S["Cell"])],
        [p("OpenSplat exceeds 24 GB unified memory", S["Cell"]),        p("High", S["CellRed"]),    p("Critical", S["CellRed"]),  p("Hard cap max_gaussians=1M, memory monitor wrapper (alert at 18 GB, kill at 22 GB), auto-retry with sh_degree=1.", S["Cell"])],
        [p("OpenSplat Metal kernel not working on your Mac", S["Cell"]),p("High", S["CellRed"]),    p("Critical", S["CellRed"]),  p("Validate in Week 1 before Phase 1. Expected: >2 iter/sec with Metal. Fallback: gsplat MPS community fork.", S["Cell"])],
        [p("Phone clock drift makes timeline nonsensical", S["Cell"]),  p("High", S["CellRed"]),    p("Critical", S["CellRed"]),  p("Visual anchor alignment across devices. Manual per-device offset slider. Contingency: disable timeline, static scene.", S["Cell"])],
        [p("Concurrent jobs OOM each other (no queue)", S["Cell"]),     p("High", S["CellRed"]),    p("Critical", S["CellRed"]),  p("ARQ single-job queue enforced in Phase 1. Never allow parallel GPU-heavy pipeline stages.", S["Cell"])],
        [p("People ghost despite SAM2 masking", S["Cell"]),             p("High", S["CellOrange"]), p("Major", S["CellOrange"]),  p("20px mask dilation, YOLO-prompted SAM2 (not auto-mode), float-Gaussian pruning pass after training.", S["Cell"])],
        [p("WhatsApp strips EXIF timestamps", S["Cell"]),               p("Med", S["CellOrange"]),  p("Major", S["CellOrange"]),  p("Warn user on upload; offer manual time-range picker. Prompt 'upload originals, not re-shares'.", S["Cell"])],
        [p(".ply file too large for mobile browser", S["Cell"]),        p("Med", S["CellOrange"]),  p("Major", S["CellOrange"]),  p("LOD preview.ply (<5 MB loads in <2s). Mobile devices get 100K-Gaussian scene by default.", S["Cell"])],
        [p("Silent PyTorch MPS→CPU fallback", S["Cell"]),               p("High", S["CellOrange"]), p("Major", S["CellOrange"]),  p("Test with PYTORCH_ENABLE_MPS_FALLBACK=0 in CI — makes fallbacks throw exceptions instead of silently degrading.", S["Cell"])],
    ]
    t = Table(risks, colWidths=[4*cm, 1.1*cm, 1.5*cm, 9.4*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.3*cm)]

    # Validation gates
    story += [
        Paragraph("Validation Gates", S["H2"]),
        Paragraph("<b>Before COLMAP:</b> ≥30 images after blur filtering · ≤50% rejected for blur · ≥60% have DateTimeOriginal EXIF", S["Bul"]),
        Paragraph("<b>Before OpenSplat:</b> ≥70% images registered · ≥25 registered images · ≥5,000 sparse 3D points · reprojection error ≤2px", S["Bul"]),
        Paragraph("<b>After OpenSplat:</b> Validation PSNR ≥22 dB · SSIM ≥0.75 · Gaussian count ≤2,000,000 · .ply file <300 MB", S["Bul"]),
        Spacer(1, 0.3*cm), PageBreak(),
    ]

    # Privacy
    story += [
        Paragraph("Privacy & Legal Requirements", S["H1"]), hr(),
        Paragraph(
            "3D Gaussian splats rendering recognizable faces constitute biometric data under "
            "GDPR Article 9. These requirements must be implemented BEFORE any public launch.", S["Warn"]),
        Spacer(1, 0.15*cm),
    ]
    priv = [
        [p("Requirement", S["CellHdr"]),       p("Implementation", S["CellHdr"])],
        [p("Face blurring", S["Cell"]),         p("InsightFace (MIT) detection + 25px Gaussian blur on texture layer. Auto-applied to all public scenes.", S["Cell"])],
        [p("Data retention", S["Cell"]),        p("Raw photos deleted 24h after reconstruction. COLMAP model: 30 days. Final .ply: 90 days (default).", S["Cell"])],
        [p("EXIF GPS stripping", S["Cell"]),    p("Strip GPS from all uploads on ingest. Retain only DateTimeOriginal and FocalLength for pipeline.", S["Cell"])],
        [p("Right to erasure", S["Cell"]),      p("'Report myself in this scene' button visible to viewers. Take-down within 72 hours of report.", S["Cell"])],
        [p("Consent gate", S["Cell"]),          p("Host confirms all attendees were informed before triggering 3D reconstruction.", S["Cell"])],
        [p("GDPR / CCPA", S["Cell"]),           p("Privacy policy + data subject access request mechanism required before accepting EU/California users.", S["Cell"])],
    ]
    t = Table(priv, colWidths=[3.5*cm, 12.5*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.25*cm)]

    # License table
    story.append(Paragraph("Library License Safety", S["H2"]))
    lic = [
        [p("Library", S["CellHdr"]),                    p("License", S["CellHdr"]),    p("Commercial Use?", S["CellHdr"])],
        [p("COLMAP / pycolmap", S["Cell"]),              p("BSD-3-Clause", S["Cell"]),  p("Yes", S["CellGreen"])],
        [p("SAM2 (Meta)", S["Cell"]),                    p("Apache 2.0", S["Cell"]),    p("Yes", S["CellGreen"])],
        [p("Depth Anything v2 Small", S["Cell"]),        p("Apache 2.0", S["Cell"]),    p("Yes — Small variant only", S["CellGreen"])],
        [p("OpenSplat", S["Cell"]),                      p("AGPLv3", S["Cell"]),        p("Yes — with AGPL network-service awareness", S["CellGreen"])],
        [p("WildGaussians (reference code)", S["Cell"]), p("MIT", S["Cell"]),           p("Yes", S["CellGreen"])],
        [p("InstantSplat (NVLabs)", S["Cell"]),          p("NVIDIA NC License", S["Cell"]), p("NO — do not use", S["CellRed"])],
        [p("DUSt3R / MASt3R", S["Cell"]),                p("CC-BY-NC-SA 4.0", S["Cell"]),  p("NO — do not use", S["CellRed"])],
        [p("Depth Anything v2 Base / Large", S["Cell"]), p("CC-BY-NC-4.0", S["Cell"]),     p("NO — Small variant only", S["CellRed"])],
    ]
    t = Table(lic, colWidths=[5*cm, 4*cm, 7*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.3*cm)]

    # Key papers
    story += [Paragraph("Key Papers to Read", S["H1"]), hr()]
    papers = [
        [p("#", S["CellHdr"]),  p("Paper & Authors", S["CellHdr"]),                                                       p("Why Essential", S["CellHdr"])],
        [p("1", S["Cell"]),     p("<b>3D Gaussian Splatting</b> — Kerbl et al., SIGGRAPH 2023. arxiv.org/abs/2308.04079", S["Cell"]),   p("Foundation — everything builds on this", S["Cell"])],
        [p("2", S["Cell"]),     p("<b>NeRF in the Wild</b> — Martin-Brualla et al., CVPR 2021. arxiv.org/abs/2008.02268", S["Cell"]),   p("Appearance embeddings for variable lighting — the core technique", S["Cell"])],
        [p("3", S["Cell"]),     p("<b>CSS: Crowd-Sourced Gaussian Splatting</b> — Chen et al., 2024. arxiv.org/abs/2409.08562", S["Cell"]), p("YOUR EXACT PROBLEM — read before writing any code", S["CellRed"])],
        [p("4", S["Cell"]),     p("<b>WildGaussians</b> — Kulhanek et al., NeurIPS 2024. arxiv.org/abs/2407.08447", S["Cell"]),        p("MIT license — borrow the appearance embedding implementation", S["Cell"])],
        [p("5", S["Cell"]),     p("<b>DUSt3R: Geometric 3D Vision Made Easy</b> — Wang et al., CVPR 2024. arxiv.org/abs/2312.14132", S["Cell"]), p("Pose-free pipeline (NC license but required reading)", S["Cell"])],
        [p("6", S["Cell"]),     p("<b>Gaussian in the Dark</b> — 2024. arxiv.org/abs/2408.09130", S["Cell"]),              p("Dark venue and nightclub reconstruction", S["Cell"])],
    ]
    t = Table(papers, colWidths=[0.6*cm, 9.4*cm, 6*cm])
    t.setStyle(base_table_style())
    story.append(t)

    doc.build(story)
    print(f"✓  Project Proposal PDF → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# PDF 2 — PROJECT INSIGHT
# ══════════════════════════════════════════════════════════════════════════════

def build_insight(path, S):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="D-Vision-3D-Reconstructure — Project Insight",
        author="Dana Khaing",
    )
    story = []

    # Cover
    story += [
        Spacer(1, 1.5*cm),
        Paragraph("D-Vision-3D-Reconstructure", S["DocTitle"]),
        Paragraph("Memoir3D · Project Insight & Market Research", S["DocSub"]),
        Paragraph(f"Prepared by Dana Khaing · {datetime.date.today().strftime('%B %d, %Y')}", S["Cap"]),
        Spacer(1, 0.4*cm), hr(ACCENT),
    ]

    # The Idea
    story += [
        Paragraph("The Core Idea", S["H1"]),
        Paragraph(
            "Every party generates hundreds of photos scattered across everyone's camera rolls. "
            "No single person saw the whole party. The solution: aggregate all photos from all "
            "attendees and use AI to reconstruct the event as a 3D navigable space with a "
            "timeline scrubber.", S["Body"]),
        Paragraph(
            "The key innovation is the <b>temporal layer</b>. Photos have EXIF timestamps. "
            "By grouping photos into 15-minute windows and training a separate 3D Gaussian Splat "
            "for each window — all anchored to the same coordinate frame from a single full-event "
            "COLMAP reconstruction — the user can scrub through time and watch the venue "
            "transform from an empty room to a packed dance floor.", S["Body"]),
        Spacer(1, 0.2*cm),
    ]

    # Competitors
    story += [Paragraph("Market Research: Competitor Landscape", S["H1"]), hr()]
    comp = [
        [p("Product", S["CellHdr"]),            p("What It Does", S["CellHdr"]),                                           p("The Gap vs. Memoir3D", S["CellHdr"])],
        [p("Luma AI", S["Cell"]),               p("Photo/video to Gaussian Splat. Cloud-based. Best visual quality.", S["Cell"]), p("Single-person capture only. No timeline, no multi-attendee workflow. Pivoted away from GS in late 2025.", S["Cell"])],
        [p("Polycam", S["Cell"]),               p("LiDAR + photo scan. 4.7★ / 540K iOS ratings. UE5 export.", S["Cell"]),  p("Requires a deliberate scan session. No crowd-sourcing, no temporal dimension.", S["Cell"])],
        [p("Scaniverse (Niantic)", S["Cell"]),  p("On-device GS processing. Free.", S["Cell"]),                             p("Single device only. No temporal dimension. No multi-contributor workflow.", S["Cell"])],
        [p("KIRI Engine", S["Cell"]),           p("Photogrammetry-first, freemium.", S["Cell"]),                            p("No timeline, no crowd aggregation. Professional scanning tool.", S["Cell"])],
        [p("RealityScan (Epic)", S["Cell"]),    p("High-quality mesh from photos.", S["Cell"]),                             p("Professional tool. No event or social use case.", S["Cell"])],
    ]
    t = Table(comp, colWidths=[3*cm, 5.5*cm, 7.5*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.2*cm)]
    story.append(Paragraph(
        "<b>Conclusion:</b> The timeline-scrubber over a crowd-sourced party scene is novel "
        "and commercially unoccupied. The main competitive risk is Polycam or Luma AI adding "
        "multi-user + temporal features — neither has announced this as of mid-2026.", S["Body"]))
    story.append(Spacer(1, 0.2*cm))

    # Academic landscape
    story += [Paragraph("Academic Research Landscape", S["H1"]), hr()]
    story.append(Paragraph(
        "The research foundation exists — the product implementation does not. "
        "This is the gap to fill.", S["Body"]))
    story.append(Spacer(1, 0.15*cm))
    acad = [
        [p("Research / Tool", S["CellHdr"]),                p("Relevance", S["CellHdr"]),                                                                       p("Status", S["CellHdr"])],
        [p("WildGaussians (NeurIPS 2024)", S["Cell"]),       p("Handles in-the-wild uncontrolled photos with variable lighting. MIT license.", S["Cell"]),        p("Research code only — no product", S["Cell"])],
        [p("CSS: Crowd-Sourced GS (arXiv 2409.08562)", S["Cell"]), p("Directly addresses pose-free reconstruction from crowd-sourced imagery with inconsistent lighting.", S["Cell"]), p("Research only — no code released", S["Cell"])],
        [p("InstantSplat (NVLabs)", S["Cell"]),              p("Pose-free GS in seconds. Architecturally ideal for this use case.", S["Cell"]),                   p("CUDA only + non-commercial license — cannot use", S["CellRed"])],
        [p("Splatt3R", S["Cell"]),                           p("Zero-shot GS from uncalibrated image pairs.", S["Cell"]),                                          p("Non-commercial license — cannot use", S["CellRed"])],
        [p("OpenSplat", S["Cell"]),                          p("Metal-native GS training. AGPLv3 license. Active community.", S["Cell"]),                          p("USE THIS — runs on Apple Silicon", S["CellGreen"])],
        [p("COLMAP", S["Cell"]),                             p("Gold-standard SfM. Metal-accelerated on macOS via Homebrew.", S["Cell"]),                          p("USE THIS — production ready", S["CellGreen"])],
        [p("SAM2 (Meta)", S["Cell"]),                        p("Segment Anything v2. Apache 2.0. MPS support confirmed.", S["Cell"]),                              p("USE THIS — for person masking", S["CellGreen"])],
    ]
    t = Table(acad, colWidths=[4*cm, 7.5*cm, 4.5*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.3*cm), PageBreak()]

    # Apple Silicon
    story += [Paragraph("Apple Silicon Reality Check", S["H1"]), hr()]
    story.append(Paragraph(
        "Your Mac mini M-series (24 GB unified memory, Metal GPU) is capable but requires "
        "careful tool selection. Most research implementations assume NVIDIA CUDA and are "
        "blocked on your hardware.", S["Body"]))
    story.append(Spacer(1, 0.15*cm))
    mps = [
        [p("Library", S["CellHdr"]),                    p("MPS / Metal Support", S["CellHdr"]),                                      p("Verdict", S["CellHdr"])],
        [p("WildGaussians", S["Cell"]),                  p("No — CUDA 11.8 explicitly required", S["Cell"]),                          p("Blocked", S["CellRed"])],
        [p("InstantSplat (NVLabs)", S["Cell"]),          p("No — CUDA 12.1 explicitly required", S["Cell"]),                          p("Blocked", S["CellRed"])],
        [p("gsplat (official)", S["Cell"]),              p("No — issue #163 open since April 2024, unresolved", S["Cell"]),           p("Blocked", S["CellRed"])],
        [p("Splatfacto-W / nerfstudio GS", S["Cell"]),  p("Broken — confirmed in issue #3290", S["Cell"]),                           p("Blocked", S["CellRed"])],
        [p("COLMAP / pycolmap", S["Cell"]),              p("Yes — native Metal, brew install colmap, arm64 pip wheel", S["Cell"]),    p("Full support", S["CellGreen"])],
        [p("OpenSplat", S["Cell"]),                      p("Yes — Metal-native build (build from source with libtorch)", S["Cell"]), p("Use this for GS", S["CellGreen"])],
        [p("SAM2", S["Cell"]),                           p("Yes — MPS with PYTORCH_ENABLE_MPS_FALLBACK=1", S["Cell"]),               p("Supported", S["CellGreen"])],
        [p("Depth Anything v2 Small", S["Cell"]),        p("Yes — MPS + Core ML Neural Engine option", S["Cell"]),                   p("Supported", S["CellGreen"])],
        [p("hloc (SuperPoint+SuperGlue)", S["Cell"]),    p("Yes — MPS (slower than CUDA, retrieval pairing mitigates)", S["Cell"]),  p("Supported", S["CellGreen"])],
    ]
    t = Table(mps, colWidths=[4.5*cm, 7.5*cm, 4*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.25*cm)]

    # Benchmarks
    story.append(Paragraph("Performance Benchmarks — M-series Mac mini Estimates", S["H2"]))
    bench = [
        [p("Stage", S["CellHdr"]),                   p("100 photos", S["CellHdr"]), p("300 photos", S["CellHdr"]), p("Notes", S["CellHdr"])],
        [p("COLMAP SIFT extraction", S["Cell"]),      p("~45 sec", S["Cell"]),  p("~2.5 min", S["Cell"]),  p("Scales linearly, CPU-bound on Apple Silicon", S["Cell"])],
        [p("COLMAP exhaustive matching", S["Cell"]),  p("~2 min", S["Cell"]),   p("~20 min", S["Cell"]),   p("O(n²) bottleneck — switch to vocab tree matching above 200 photos", S["Cell"])],
        [p("hloc SuperGlue matching", S["Cell"]),     p("~8 min", S["Cell"]),   p("~60+ min", S["Cell"]),  p("Higher quality; use retrieval-based pairing to cap pair count", S["Cell"])],
        [p("COLMAP incremental mapping", S["Cell"]),  p("~5 min", S["Cell"]),   p("~25 min", S["Cell"]),   p("CPU-bound, bundle adjustment included in time", S["Cell"])],
        [p("SAM2 masking (ViT-B+, MPS)", S["Cell"]), p("~5 min", S["Cell"]),   p("~15 min", S["Cell"]),   p("Approximately 3 seconds per image on MPS device", S["Cell"])],
        [p("OpenSplat 30K iterations", S["Cell"]),    p("~17 min", S["Cell"]),  p("~17 min", S["Cell"]),   p("Training time is roughly constant vs photo count (GPU-bound)", S["Cell"])],
        [p("Total pipeline (per window)", S["Cell"]), p("~35 min", S["Cell"]),  p("~80 min", S["Cell"]),   p("Sequential; 4 time windows = 4× training time", S["Cell"])],
    ]
    t = Table(bench, colWidths=[4.2*cm, 2.3*cm, 2.3*cm, 7.2*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.2*cm)]
    story.append(Paragraph(
        "24 GB unified memory is a meaningful advantage over dedicated VRAM. "
        "OpenSplat uses ~13–19 GB for a 300-photo indoor scene, which fits comfortably. "
        "The hard limit is ~2 million Gaussians — beyond that, OOM risk is high.", S["Body"]))
    story.append(Spacer(1, 0.3*cm))

    # Product design
    story += [Paragraph("Product Design Highlights", S["H1"]), hr()]
    story.append(Paragraph("Core User Journeys", S["H2"]))
    journeys = [
        ("Host", "Creates event → shares QR code → guests upload → triggers reconstruction → reviews result → shares link. System warns about sparse coverage gaps before triggering GPU compute."),
        ("Viewer", "Receives link → 8-second cinematic intro flythrough → free exploration → scrubs timeline to watch party evolve in 3D. No account required to view."),
        ("Contributor", "Scans QR at venue or taps link in group chat → mobile browser, no app install → selects photos from camera roll → chunked upload → 'Your 27 photos are in the mix!'"),
    ]
    for name, desc in journeys:
        story.append(Paragraph(f"<b>{name}:</b> {desc}", S["Bul"]))
    story.append(Spacer(1, 0.2*cm))

    story += [
        Paragraph("3D Viewer UX Design Principles", S["H2"]),
        Paragraph("Core principle: feel like <b>Google Maps 3D</b>, not Blender. Non-technical users already know pinch-to-zoom and drag-to-pan from maps.", S["Body"]),
        Paragraph("• Mouse: left-drag = orbit · scroll = zoom · right-drag = pan · double-click = recenter orbit point", S["Bul"]),
        Paragraph("• Touch: one-finger drag = orbit · pinch = zoom · two-finger drag = pan", S["Bul"]),
        Paragraph("• Timeline: full-width bar, 30-min buckets, density histogram, 0.4s cross-fade between time windows", S["Bul"]),
        Paragraph("• Play button: auto-advance one window per 4 seconds — creates a time-lapse of the entire party", S["Bul"]),
        Spacer(1, 0.2*cm),
        Paragraph("Progressive Loading — Never Show a Blank Screen", S["H2"]),
        Paragraph("• 0–1s: Fetch scene.json → render timeline scrubber with loading skeletons per window", S["Bul"]),
        Paragraph("• 1–5s: Stream foundation_preview.ply (10% density, <5 MB) → user can already orbit gray point cloud", S["Bul"]),
        Paragraph("• 5–20s: Stream full foundation.ply in 2 MB HTTP range chunks → surfaces solidify progressively", S["Bul"]),
        Paragraph("• On demand: time windows loaded on scrubber interaction; ±1 window prefetched silently", S["Bul"]),
        Spacer(1, 0.3*cm), PageBreak(),
    ]

    # Monetization
    story += [Paragraph("Monetization Strategy", S["H1"]), hr()]
    story.append(Paragraph("Per-Event Pricing (Consumer)", S["H2"]))
    pricing = [
        [p("Tier", S["CellHdr"]),      p("Price", S["CellHdr"]),         p("Limits", S["CellHdr"]),              p("Key Features", S["CellHdr"])],
        [p("Free", S["Cell"]),          p("$0", S["Cell"]),               p("1 event, 50 photos", S["Cell"]),     p("Memoir3D watermark on all exports", S["Cell"])],
        [p("Starter", S["Cell"]),       p("$9 one-time", S["Cell"]),      p("500 photos", S["Cell"]),             p("No watermark, 720p flythrough video export", S["Cell"])],
        [p("Pro", S["Cell"]),           p("$29 one-time", S["Cell"]),     p("5 events, 2K photos/event", S["Cell"]), p("Face blur toggle, 1080p export, password protection", S["Cell"])],
        [p("Wedding / Event", S["Cell"]),p("$79 one-time", S["Cell"]),   p("Unlimited photos", S["Cell"]),       p("4K export, embed code, priority processing queue", S["Cell"])],
    ]
    t = Table(pricing, colWidths=[2.5*cm, 2.5*cm, 4*cm, 7*cm])
    t.setStyle(base_table_style())
    story += [t, Spacer(1, 0.2*cm)]
    story += [
        Paragraph("B2B Subscription — $99/month", S["H2"]),
        Paragraph(
            "Target: wedding photographers, event management companies, corporate comms teams. "
            "Includes: unlimited events, white-label viewer (remove branding, add their logo), "
            "client delivery portal, API access, 5 team seats. High LTV, low churn — "
            "repeat buyers making 20–50 events per year.", S["Body"]),
        Spacer(1, 0.15*cm),
        Paragraph("À La Carte Add-Ons (highest-margin upsells shown at sharing moment)", S["H2"]),
        Paragraph("• Face blur pack: $5/event · AI highlight reel 60s: $8/event · Extended storage 5yr: $12/yr", S["Bul"]),
        Paragraph("• Rush processing (2-hour guarantee): $15/event · Custom vanity URL: $8 one-time", S["Bul"]),
        Spacer(1, 0.3*cm),
    ]

    # Timeline
    story += [Paragraph("Realistic Timeline Summary", S["H1"]), hr()]
    tl = [
        [p("Scenario", S["CellHdr"]),            p("MVP (M6)", S["CellHdr"]),      p("Production (M7)", S["CellHdr"]), p("Notes", S["CellHdr"])],
        [p("Optimistic", S["Cell"]),              p("Week 26 (~6.5 mo)", S["Cell"]),p("Week 34 (~8.5 mo)", S["Cell"]), p("Everything works first try, no major blockers", S["Cell"])],
        [p("Realistic ← use this", S["CellBold"]),p("Week 32 (~8 mo)", S["CellBold"]),p("Week 40 (~10 mo)", S["CellBold"]),p("Normal debugging, a few direction changes, life happens", S["CellBold"])],
        [p("Pessimistic", S["Cell"]),             p("Week 42 (~10.5 mo)", S["Cell"]),p("Week 52 (~13 mo)", S["Cell"]), p("Timeline feature requires a research pivot; COLMAP needs workarounds", S["Cell"])],
    ]
    t = Table(tl, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 5.5*cm])
    ts = base_table_style()
    ts.add("BACKGROUND", (0, 2), (-1, 2), PHASE_BG)
    t.setStyle(ts)
    story += [t, Spacer(1, 0.2*cm)]
    story.append(Paragraph(
        "The difference between optimistic and pessimistic is driven by two things: "
        "(1) how long the photo-to-Gaussian temporal association problem takes to solve, and "
        "(2) whether COLMAP performance on Apple Silicon is acceptable. "
        "Both can be validated in Phase 0 (Weeks 1–3).", S["Body"]))
    story.append(Spacer(1, 0.3*cm))

    # The Rule
    story += [
        Paragraph("The One Rule", S["H1"]), hr(),
        Paragraph(
            "Before writing a single line of app code, take 100 photos of your room and run "
            "the full COLMAP → OpenSplat pipeline on your Mac mini. "
            "The numbers you get — training time, quality, memory usage — will inform every "
            "product decision for the next 10 months. No planning document replaces this.", S["Body"]),
        Spacer(1, 0.2*cm),
        Paragraph(
            "The most important test: does the .ply file render as a recognizable room in "
            "Supersplat? If yes, the foundation is proven and you can build with confidence. "
            "If no, you have discovered the core blocker before investing months of work.", S["Body"]),
    ]

    doc.build(story)
    print(f"✓  Project Insight PDF → {path}")


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    out = "/Users/dana_khaing/PROJECTS/D-Vision-3D-reconstructure/docs"
    os.makedirs(out, exist_ok=True)
    S = make_styles()
    build_proposal(f"{out}/D-Vision-3D-Project-Proposal.pdf", S)
    build_insight(f"{out}/D-Vision-3D-Project-Insight.pdf", S)
    print("Done.")
