"""Generate Project Plan PDF and Project Insight PDF using ReportLab."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import datetime

# ── Color palette ─────────────────────────────────────────────────────────────
DARK_BG    = colors.HexColor("#0F172A")
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

W, H = A4

def make_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        "DocTitle",
        parent=styles["Title"],
        fontSize=28, textColor=ACCENT, spaceAfter=6,
        fontName="Helvetica-Bold", alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "DocSubtitle",
        fontSize=14, textColor=TEXT_GRAY, spaceAfter=20,
        fontName="Helvetica", alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        "H1",
        fontSize=18, textColor=ACCENT, spaceBefore=18, spaceAfter=8,
        fontName="Helvetica-Bold", borderPad=4,
    ))
    styles.add(ParagraphStyle(
        "H2",
        fontSize=13, textColor=ACCENT2, spaceBefore=12, spaceAfter=6,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "H3",
        fontSize=11, textColor=colors.HexColor("#1E40AF"), spaceBefore=8, spaceAfter=4,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        "Body",
        fontSize=10, textColor=colors.HexColor("#1E293B"), spaceAfter=6,
        fontName="Helvetica", leading=15, alignment=TA_JUSTIFY,
    ))
    styles.add(ParagraphStyle(
        "BulletItem",
        fontSize=10, textColor=colors.HexColor("#1E293B"), spaceAfter=3,
        fontName="Helvetica", leftIndent=16, leading=14,
        bulletText="•", bulletIndent=6,
    ))
    styles.add(ParagraphStyle(
        "CodeBlock",
        fontSize=8, textColor=colors.HexColor("#1E293B"), spaceAfter=4,
        fontName="Courier", backColor=colors.HexColor("#F1F5F9"),
        leftIndent=12, rightIndent=12, borderPad=6, leading=12,
    ))
    styles.add(ParagraphStyle(
        "WarningText",
        fontSize=10, textColor=WARN_RED, spaceAfter=6,
        fontName="Helvetica-Bold", leftIndent=8,
    ))
    styles.add(ParagraphStyle(
        "CaptionText",
        fontSize=9, textColor=TEXT_GRAY, spaceAfter=4,
        fontName="Helvetica-Oblique", alignment=TA_CENTER,
    ))
    return styles

def table_style(has_header=True):
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("WORDWRAP", (0, 0), (-1, -1), True),
    ]
    return TableStyle(cmds)

def hr(color=ACCENT):
    return HRFlowable(width="100%", thickness=1, color=color, spaceAfter=8, spaceBefore=4)

# ══════════════════════════════════════════════════════════════════════════════
# PDF 1 — PROJECT PLAN
# ══════════════════════════════════════════════════════════════════════════════

def build_project_plan(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="D-Vision-3D-Reconstructure — Project Plan",
        author="Dana Khaing",
    )
    S = make_styles()
    story = []

    # ── Cover ────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 1.5*cm),
        Paragraph("D-Vision-3D-Reconstructure", S["DocTitle"]),
        Paragraph("Memoir3D · Project Plan & Build Roadmap", S["DocSubtitle"]),
        Paragraph(f"Generated: {datetime.date.today().strftime('%B %d, %Y')}", S["CaptionText"]),
        Spacer(1, 0.5*cm),
        hr(ACCENT),
    ]

    # ── Overview ─────────────────────────────────────────────────────────────
    story += [
        Paragraph("Project Overview", S["H1"]),
        Paragraph(
            "D-Vision-3D-Reconstructure (product name: Memoir3D) transforms crowd-sourced event "
            "photos — taken by multiple attendees with different phones, angles, lighting, and "
            "timestamps — into a single navigable 3D scene with a timeline scrubber. The user "
            "can fly around the venue in a browser and scrub through time to relive any moment "
            "of the party.", S["Body"]),
        Paragraph(
            "<b>Market gap:</b> No existing tool (Luma AI, Polycam, Scaniverse) handles "
            "crowd-sourced multi-attendee photos with a temporal layer. The product gap is real "
            "and the research foundation (WildGaussians NeurIPS 2024, CSS arXiv 2409.08562) "
            "is mature enough to build on.", S["Body"]),
        Spacer(1, 0.3*cm),
    ]

    # ── Tech Stack ───────────────────────────────────────────────────────────
    story += [
        Paragraph("Definitive Tech Stack", S["H1"]),
        hr(),
        Paragraph("Backend (Python)", S["H2"]),
    ]
    backend_data = [
        ["Package", "Version", "Role"],
        ["FastAPI", "0.115+", "REST API + WebSocket server"],
        ["ARQ", "0.26+", "Async Redis job queue (avoids MPS GPU context fork issues)"],
        ["SQLModel", "0.0.21+", "ORM — single model for SQLite (local) + PostgreSQL (cloud)"],
        ["Alembic", "1.13+", "Database migrations"],
        ["redis[asyncio]", "5.0+", "Job queue + PubSub for live progress"],
        ["Pillow + piexif", "10+", "Thumbnails, EXIF extraction"],
    ]
    t = Table(backend_data, colWidths=[3.5*cm, 2.5*cm, 10*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story.append(Paragraph("ML Pipeline (Apple Silicon Metal/MPS)", S["H2"]))
    ml_data = [
        ["Tool", "Role", "Apple Silicon"],
        ["COLMAP / pycolmap", "Camera pose estimation (SfM)", "✓ Metal-native (brew install)"],
        ["hloc SuperPoint+SuperGlue", "Feature matching for dark photos", "✓ MPS supported"],
        ["SAM2 (Meta)", "Person masking per photo", "✓ MPS with fallback env var"],
        ["YOLOv8n (ultralytics)", "Person bounding boxes for SAM2", "✓ MPS supported"],
        ["Depth Anything v2 Small", "Depth hints (Apache 2.0)", "✓ MPS + Core ML"],
        ["OpenSplat", "3D Gaussian Splatting training", "✓ Metal-native build"],
    ]
    t = Table(ml_data, colWidths=[4.5*cm, 5*cm, 6.5*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story.append(Paragraph("Frontend (React / TypeScript)", S["H2"]))
    fe_data = [
        ["Package", "Role"],
        ["React 18 + Vite 5", "SPA — not Next.js (no SSR needed, simpler)"],
        ["Three.js 0.169+", "3D renderer"],
        ["@mkkellogg/gaussian-splats-3d", "Best maintained WebGL Gaussian Splatting renderer"],
        ["Zustand 4.5+", "Minimal state management"],
        ["Tailwind CSS 4 + shadcn/ui", "Styling + accessible components"],
        ["axios + react-dropzone", "File upload with progress events"],
    ]
    t = Table(fe_data, colWidths=[6*cm, 10*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.5*cm), PageBreak()]

    # ── Pipeline ─────────────────────────────────────────────────────────────
    story += [
        Paragraph("ML Pipeline — Full Data Flow", S["H1"]),
        hr(),
        Paragraph(
            "All stages are chained sequentially. Each stage writes a checkpoint file. "
            "On failure or retry, completed stages are skipped automatically.", S["Body"]),
        Spacer(1, 0.2*cm),
    ]
    pipeline_data = [
        ["Step", "Script", "Time (300 photos)", "Output"],
        ["1 — Ingest & Validate", "01_ingest.py", "~5 sec", "processed_images/, metadata.json"],
        ["2 — Temporal Bucketing", "02_bucket.py", "<1 sec", "buckets.json (15-min windows)"],
        ["3 — COLMAP Full Event", "03_colmap_full.py", "20–90 min", "sparse/0/ (camera poses)"],
        ["4 — SAM2 Masking", "04_mask.py", "5–15 min", "masks/*.png (255=exclude people)"],
        ["5 — Window Sub-Recon", "05_window_recon.py", "<1 min", "windows/{id}/sparse/0/"],
        ["6 — OpenSplat Training", "06_train_windows.py", "~17 min/window", "{bucket_id}.ply"],
        ["7 — Post-Processing", "07_postprocess.py", "~2 min", "scene.json + LOD preview.ply"],
    ]
    t = Table(pipeline_data, colWidths=[3.5*cm, 3.5*cm, 3*cm, 6*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("Key COLMAP Settings for Party Photos", S["H3"]),
        Paragraph("• <b>domain_size_pooling=True</b> — biggest win for dark/low-texture scenes", S["BulletItem"]),
        Paragraph("• <b>max_num_features=16384</b> — double default to survive noise", S["BulletItem"]),
        Paragraph("• <b>camera_mode=PER_IMAGE</b> — critical for mixed phones", S["BulletItem"]),
        Paragraph("• <b>hloc SuperPoint+SuperGlue</b> — replace SIFT for 2–3× more matched pairs", S["BulletItem"]),
        Spacer(1, 0.3*cm),
        Paragraph("OpenSplat Key Parameters", S["H3"]),
        Paragraph("• <b>max_gaussians=1,000,000</b> — hard cap to stay within 24 GB unified memory", S["BulletItem"]),
        Paragraph("• <b>sh_degree=3</b> — full spherical harmonics; reduce to 1 if OOM", S["BulletItem"]),
        Paragraph("• <b>iterations=30,000</b> — ~17 min on M-series Metal GPU", S["BulletItem"]),
        Paragraph("• <b>masks enabled</b> — pass SAM2 mask directory to exclude people from training", S["BulletItem"]),
        Spacer(1, 0.5*cm), PageBreak(),
    ]

    # ── Phase Plan ───────────────────────────────────────────────────────────
    story += [
        Paragraph("Phase-by-Phase Build Plan", S["H1"]),
        hr(),
    ]
    phases = [
        ("Phase 0 — Proof of Concept", "Weeks 1–3",
         "Prove the pipeline runs on your Mac mini BEFORE building anything.\n"
         "Install pycolmap + OpenSplat + SAM2. Run on ETH3D dataset.\n"
         "Take 50–100 photos of your room → full pipeline → view .ply in Supersplat.\n"
         "Document real processing times. This phase cannot be skipped."),
        ("Phase 1 — Single-Event Pipeline", "Weeks 4–8",
         "Python pipeline orchestrator: COLMAP→SAM2→OpenSplat as subprocess chain.\n"
         "FastAPI skeleton: upload endpoint, job trigger, status polling.\n"
         "ARQ background worker with Redis PubSub progress events.\n"
         "Run pipeline 5× with varied photo sets. Fix every crash."),
        ("Phase 2 — Browser 3D Viewer", "Weeks 9–13",
         "React + Vite + Three.js scaffold. gaussian-splats-3d renderer.\n"
         "Orbit/pan/zoom controls. Progressive .ply loading via HTTP range requests.\n"
         "Safari/iOS compatibility testing. M3 milestone: navigable in 3 browsers."),
        ("Phase 3 — Timeline Layer ⚠️", "Weeks 14–20 (+4 buffer)",
         "RESEARCH WEEK 14: Read CSS paper + WildGaussians before coding.\n"
         "EXIF extraction, clock drift detection, 15-min time bucketing.\n"
         "SAM2 batch inference. Per-window sub-reconstructions from shared COLMAP poses.\n"
         "Timeline scrubber React component. Cross-fade between windows.\n"
         "NOTE: Highest uncertainty phase. Budget 3–4 extra weeks."),
        ("Phase 4 — Photo Collection UX", "Weeks 21–26",
         "Event creation UI + shareable URL + QR code generation.\n"
         "Mobile-optimized upload page (iOS HEIC conversion, EXIF orientation fix).\n"
         "Resumable uploads, deduplication, coverage heatmap.\n"
         "Test: 3 real non-developers upload without help."),
        ("Phase 5 — MVP Polish & Real Event", "Weeks 27–32",
         "WebSocket live progress UI (6-stage pipeline). Email notifications.\n"
         "Error handling audit. 500-photo stress test.\n"
         "USE AT A REAL EVENT (Week 31). Fix from feedback.\n"
         "M6: 5 guests open result, 1 says it's cool, no manual intervention."),
        ("Phase 6 — Production Quality", "Weeks 33–40",
         "SQLite → PostgreSQL migration (Alembic). Docker container.\n"
         "Cloud deploy (Railway/Fly.io). Cloudflare R2 storage. Sentry monitoring.\n"
         "UI redesign from real user feedback. Landing page copy.\n"
         "M7: strangers can use it without your help."),
    ]
    for title, timeline, desc in phases:
        phase_data = [[title, timeline]] + [[Paragraph(line, S["Body"]), ""] for line in desc.split("\n")]
        t = Table(
            [[Paragraph(f"<b>{title}</b>", S["H3"]), Paragraph(f"<i>{timeline}</i>", S["Body"])]] +
            [[Paragraph(line, S["BulletItem"]), ""] for line in desc.split("\n")],
            colWidths=[14*cm, 2*cm]
        )
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EDE9FE")),
            ("GRID", (0, 0), (-1, -1), 0.3, BORDER),
            ("SPAN", (0, 1), (-1, -1)),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story += [t, Spacer(1, 0.2*cm)]

    story.append(Spacer(1, 0.3*cm))

    # Milestones table
    story += [
        Paragraph("Milestones Summary", S["H2"]),
    ]
    ms_data = [
        ["#", "Milestone", "Target Week", "Key Success Criteria"],
        ["M0", "Environment working", "3", "All tools install; real benchmarks documented"],
        ["M1", "First reconstruction", "2–3", "Your room photos → viewable .ply"],
        ["M2", "Pipeline API", "8", "curl upload → .ply via API, handles errors"],
        ["M3", "Browser viewer", "13", "3DGS navigable in Chrome + Safari + Android"],
        ["M4", "Timeline scrubber", "20 ±4", "Scrubbing changes the 3D scene"],
        ["M5", "Multi-contributor UX", "26", "3 non-devs upload without help"],
        ["M6", "MVP real event", "32", "Real guests, no manual intervention"],
        ["M7", "Production quality", "40", "Cloud deployed, strangers use it"],
    ]
    t = Table(ms_data, colWidths=[1*cm, 4.5*cm, 3*cm, 7.5*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.5*cm), PageBreak()]

    # ── Risks ────────────────────────────────────────────────────────────────
    story += [
        Paragraph("Critical Risks & Mitigations", S["H1"]),
        hr(),
    ]
    risk_data = [
        ["Risk", "P", "I", "Mitigation"],
        ["COLMAP fails on dark/blurry photos", "High", "Critical",
         "Blur rejection gate (Laplacian < 50), hloc SuperGlue matcher, domain_size_pooling"],
        ["OpenSplat OOM (>24 GB)", "High", "Critical",
         "max_gaussians=1M hard cap, memory monitor wrapper, auto-retry with sh_degree=1"],
        ["OpenSplat Metal kernel missing", "High", "Critical",
         "Validate on your Mac mini in Week 1 before Phase 1. Fallback: gsplat MPS fork"],
        ["Phone clock drift ruins timeline", "High", "Critical",
         "Visual anchor alignment, manual per-device offset slider in UI"],
        ["No job queue → concurrent OOM", "High", "Critical",
         "ARQ single-job queue in Phase 1. Never allow parallel GPU stages."],
        ["People ghost despite SAM2", "High", "Major",
         "20px mask dilation, YOLO-prompted SAM2, float-Gaussian pruning post-train"],
        ["WhatsApp strips EXIF", "Med", "Major",
         "Warn user, manual time-range picker fallback"],
        [".ply too large for mobile", "Med", "Major",
         "LOD preview.ply (<5 MB), chunked HTTP range streaming, mobile gets 100K Gaussians"],
        ["Silent MPS CPU fallback", "High", "Major",
         "Test with PYTORCH_ENABLE_MPS_FALLBACK=0 in CI to make fallbacks throw exceptions"],
    ]
    t = Table(risk_data, colWidths=[4.5*cm, 1.2*cm, 1.8*cm, 8.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TEXTCOLOR", (1, 1), (1, 5), WARN_RED),
        ("TEXTCOLOR", (1, 6), (1, -1), WARN_YLW),
        ("FONTNAME", (1, 1), (2, -1), "Helvetica-Bold"),
    ]))
    story += [t, Spacer(1, 0.5*cm)]

    # ── Validation Gates ─────────────────────────────────────────────────────
    story += [
        Paragraph("Validation Gates", S["H2"]),
        Paragraph("<b>Before COLMAP:</b>", S["H3"]),
        Paragraph("≥ 30 images after blur filtering · ≤ 50% rejected for blur · ≥ 60% have DateTimeOriginal EXIF", S["BulletItem"]),
        Paragraph("<b>Before OpenSplat:</b>", S["H3"]),
        Paragraph("≥ 70% images registered · ≥ 25 registered images · ≥ 5,000 sparse 3D points · reprojection error ≤ 2px", S["BulletItem"]),
        Paragraph("<b>After OpenSplat:</b>", S["H3"]),
        Paragraph("Validation PSNR ≥ 22 dB · SSIM ≥ 0.75 · Gaussian count ≤ 2,000,000 · .ply < 300 MB", S["BulletItem"]),
        Spacer(1, 0.3*cm), PageBreak(),
    ]

    # ── Privacy ──────────────────────────────────────────────────────────────
    story += [
        Paragraph("Privacy & Legal Requirements", S["H1"]),
        hr(),
        Paragraph(
            "3D Gaussian splats rendering recognizable faces constitute biometric data under "
            "GDPR Article 9. These requirements must be implemented BEFORE any public launch.", S["WarningText"]),
        Spacer(1, 0.2*cm),
    ]
    privacy_items = [
        ("Face blurring", "InsightFace (MIT) detection + 25px Gaussian blur on texture layer. Auto-applied to all public scenes."),
        ("Data retention", "Raw photos deleted 24h after reconstruction. COLMAP model: 30 days. Final .ply: 90 days default."),
        ("EXIF GPS stripping", "Strip GPS from all uploads on ingest. Keep only DateTimeOriginal and FocalLength."),
        ("Right to erasure", "'Report myself in this scene' button. Take-down within 72 hours."),
        ("Consent gate", "Host confirms all attendees were informed before triggering reconstruction."),
        ("GDPR/CCPA", "Privacy policy + data subject access request mechanism required before EU/CA users."),
    ]
    priv_data = [["Requirement", "Implementation"]] + [[k, v] for k, v in privacy_items]
    t = Table(priv_data, colWidths=[4*cm, 12*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("Library License Safety", S["H2"]),
    ]
    lic_data = [
        ["Library", "License", "Commercial?"],
        ["COLMAP / pycolmap", "BSD-3-Clause", "✓ Yes"],
        ["SAM2 (Meta)", "Apache 2.0", "✓ Yes"],
        ["Depth Anything v2 Small", "Apache 2.0", "✓ Yes"],
        ["OpenSplat", "AGPLv3", "✓ Yes (AGPL-aware)"],
        ["WildGaussians (reference)", "MIT", "✓ Yes"],
        ["InstantSplat (NVLabs)", "NVIDIA NC License", "✗ NO — do not use"],
        ["DUSt3R / MASt3R", "CC-BY-NC-SA 4.0", "✗ NO — do not use"],
        ["Depth Anything v2 Base/Large", "CC-BY-NC-4.0", "✗ NO — Small variant only"],
    ]
    t = Table(lic_data, colWidths=[5*cm, 4*cm, 7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TEXTCOLOR", (2, 6), (2, 8), WARN_RED),
        ("TEXTCOLOR", (2, 1), (2, 5), GREEN),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
    ]))
    story += [t, Spacer(1, 0.3*cm)]

    # ── Key Papers ────────────────────────────────────────────────────────────
    story += [
        Paragraph("Key Papers to Read", S["H1"]),
        hr(),
    ]
    papers = [
        ("1", "3D Gaussian Splatting for Real-Time Radiance Field Rendering",
         "Kerbl et al., SIGGRAPH 2023", "arxiv.org/abs/2308.04079", "Foundation — everything builds on this"),
        ("2", "NeRF in the Wild: Neural Radiance Fields for Unconstrained Photo Collections",
         "Martin-Brualla et al., CVPR 2021", "arxiv.org/abs/2008.02268", "Appearance embeddings for variable lighting — the core technique"),
        ("3", "CSS: Overcoming Pose and Scene Challenges in Crowd-Sourced 3D Gaussian Splatting",
         "Chen et al., Sept 2024", "arxiv.org/abs/2409.08562", "YOUR EXACT PROBLEM — read before writing any code"),
        ("4", "WildGaussians: 3D Gaussian Splatting in the Wild",
         "Kulhanek et al., NeurIPS 2024", "arxiv.org/abs/2407.08447", "MIT license — borrow appearance embedding approach"),
        ("5", "DUSt3R: Geometric 3D Vision Made Easy",
         "Wang et al., CVPR 2024", "arxiv.org/abs/2312.14132", "Pose-free pipeline (NC license but essential reading)"),
        ("6", "Gaussian in the Dark",
         "2024", "arxiv.org/abs/2408.09130", "Dark venue / nightclub reconstruction"),
    ]
    papers_data = [["#", "Paper", "Venue", "Link", "Why"]] + \
                  [[n, Paragraph(t, S["Body"]), a, Paragraph(f"<i>{l}</i>", S["CodeBlock"]),
                    Paragraph(w, S["Body"])] for n, t, a, l, w in papers]
    t = Table(papers_data, colWidths=[0.5*cm, 4.5*cm, 2.5*cm, 4*cm, 4.5*cm])
    t.setStyle(table_style())
    story += [t]

    doc.build(story)
    print(f"✓ Project Plan PDF → {path}")


# ══════════════════════════════════════════════════════════════════════════════
# PDF 2 — PROJECT INSIGHT
# ══════════════════════════════════════════════════════════════════════════════

def build_project_insight(path):
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm, topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="D-Vision-3D-Reconstructure — Project Insight",
        author="Dana Khaing",
    )
    S = make_styles()
    story = []

    # ── Cover ────────────────────────────────────────────────────────────────
    story += [
        Spacer(1, 1.5*cm),
        Paragraph("D-Vision-3D-Reconstructure", S["DocTitle"]),
        Paragraph("Memoir3D · Project Insight & Market Research", S["DocSubtitle"]),
        Paragraph(f"Generated: {datetime.date.today().strftime('%B %d, %Y')}", S["CaptionText"]),
        Spacer(1, 0.5*cm),
        hr(ACCENT),
    ]

    # ── The Idea ─────────────────────────────────────────────────────────────
    story += [
        Paragraph("The Core Idea", S["H1"]),
        Paragraph(
            "Every party generates hundreds of photos — scattered across everyone's camera rolls. "
            "The problem: no single person saw the whole party. The solution: aggregate all photos "
            "from all attendees and use AI to reconstruct the event as a 3D navigable space with "
            "a timeline.", S["Body"]),
        Paragraph(
            "The key innovation is the <b>temporal layer</b>: photos have EXIF timestamps. "
            "By grouping photos into 15-minute windows and training a separate 3D Gaussian Splat "
            "for each window — all anchored to the same coordinate frame from a single full-event "
            "COLMAP reconstruction — the user can scrub through time and watch the venue "
            "transform.", S["Body"]),
        Spacer(1, 0.3*cm),
    ]

    # ── Market Gap ───────────────────────────────────────────────────────────
    story += [
        Paragraph("Market Research: Competitor Landscape", S["H1"]),
        hr(),
    ]
    comp_data = [
        ["Product", "What It Does", "The Gap vs. Memoir3D"],
        ["Luma AI", "Photo/video → Gaussian Splat. Cloud. Best visual quality.",
         "Single-person capture only. No timeline, no multi-attendee workflow. Pivoted to video gen."],
        ["Polycam", "LiDAR + photo scan. 4.7★ / 540K iOS ratings. UE5 export.",
         "Requires deliberate scan session. No crowd-sourcing, no temporal dimension."],
        ["Scaniverse (Niantic)", "On-device GS processing. Completely free.",
         "Single device. No temporal dimension. No multi-contributor workflow."],
        ["KIRI Engine", "Photogrammetry-first, freemium.",
         "No timeline, no crowd aggregation. Professional tool."],
        ["RealityScan (Epic)", "High-quality mesh from photos.",
         "Professional tool only. No event/social use case."],
    ]
    t = Table(comp_data, colWidths=[2.5*cm, 5*cm, 8.5*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph(
            "Conclusion: The timeline-scrubber over a crowd-sourced party scene is novel and "
            "commercially unoccupied. The main competitive risk is Polycam or Luma AI adding "
            "multi-user + temporal features — neither has announced this as of mid-2026.", S["Body"]),
        Spacer(1, 0.3*cm),
    ]

    # ── Academic Landscape ───────────────────────────────────────────────────
    story += [
        Paragraph("Academic Research Landscape", S["H1"]),
        hr(),
        Paragraph(
            "The research foundation exists — the product implementation does not. "
            "This is the gap to fill.", S["Body"]),
        Spacer(1, 0.2*cm),
    ]
    research_data = [
        ["Research / Tool", "Relevance", "Status"],
        ["WildGaussians (NeurIPS 2024)", "Handles in-the-wild uncontrolled photos with variable lighting. MIT license.", "Research code, no product"],
        ["CSS: Crowd-Sourced GS (arXiv 2409.08562)", "Directly addresses pose-free reconstruction from crowd-sourced imagery.", "Research only, no code released"],
        ["InstantSplat (NVLabs)", "Pose-free GS in seconds. Architecturally ideal.", "CUDA only + non-commercial license"],
        ["Splatt3R", "Zero-shot GS from uncalibrated image pairs.", "Non-commercial license"],
        ["OpenSplat", "Metal-native GS training. AGPLv3 license.", "✓ USE THIS — runs on Apple Silicon"],
        ["COLMAP", "Gold-standard SfM. Metal-accelerated on macOS.", "✓ USE THIS — production ready"],
        ["SAM2 (Meta)", "Segment Anything v2. Apache 2.0. MPS support.", "✓ USE THIS — for person masking"],
    ]
    t = Table(research_data, colWidths=[4.5*cm, 8*cm, 3.5*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.5*cm), PageBreak()]

    # ── Apple Silicon Reality ─────────────────────────────────────────────────
    story += [
        Paragraph("Apple Silicon Reality Check", S["H1"]),
        hr(),
        Paragraph(
            "Your Mac mini M-series (24 GB unified memory, Metal GPU) is capable but requires "
            "careful tool selection. Most research implementations assume NVIDIA CUDA and are "
            "blocked on your hardware.", S["Body"]),
        Spacer(1, 0.2*cm),
    ]
    mps_data = [
        ["Library", "MPS/Metal Support", "Verdict"],
        ["WildGaussians", "No (CUDA 11.8 required)", "❌ Blocked"],
        ["InstantSplat", "No (CUDA 12.1 required)", "❌ Blocked"],
        ["gsplat (official)", "No (issue #163 open since Apr 2024)", "❌ Blocked"],
        ["Splatfacto-W / nerfstudio GS", "Broken (issue #3290)", "❌ Blocked"],
        ["COLMAP / pycolmap", "Yes — native Metal, brew install", "✅ Full support"],
        ["OpenSplat", "Yes — Metal-native build", "✅ Use this for GS"],
        ["SAM2", "Yes — MPS with PYTORCH_ENABLE_MPS_FALLBACK=1", "✅ Supported"],
        ["Depth Anything v2 Small", "Yes — MPS + Core ML option", "✅ Supported"],
        ["hloc (SuperPoint+SuperGlue)", "Yes — MPS (slower than CUDA)", "✅ Supported"],
    ]
    t = Table(mps_data, colWidths=[5*cm, 6*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TEXTCOLOR", (2, 1), (2, 4), WARN_RED),
        ("TEXTCOLOR", (2, 5), (2, -1), GREEN),
        ("FONTNAME", (2, 1), (2, -1), "Helvetica-Bold"),
    ]))
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("Performance Benchmarks (M-series estimates)", S["H2"]),
    ]
    bench_data = [
        ["Stage", "100 photos", "300 photos", "Notes"],
        ["COLMAP SIFT extraction", "~45 sec", "~2.5 min", "Scales linearly, CPU-bound"],
        ["COLMAP exhaustive matching", "~2 min", "~20 min", "O(n²) bottleneck — use vocab tree >200 photos"],
        ["hloc SuperGlue matching", "~8 min", "~60+ min", "Higher quality, retrieval pairing recommended"],
        ["COLMAP incremental mapping", "~5 min", "~25 min", "CPU-bound, bundle adjustment included"],
        ["SAM2 masking (ViT-B+, MPS)", "~5 min", "~15 min", "~3 sec/image on MPS"],
        ["OpenSplat 30K iters", "~17 min", "~17 min", "Training time ≈ constant vs photo count"],
        ["Total pipeline", "~35 min", "~80 min", "Per time window, sequential"],
    ]
    t = Table(bench_data, colWidths=[4.5*cm, 2.5*cm, 2.5*cm, 6.5*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph(
            "24 GB unified memory is a meaningful advantage over CUDA GPUs with separate VRAM. "
            "OpenSplat uses ~13–19 GB for a 300-photo indoor scene, which fits comfortably. "
            "The hard limit is ~2M Gaussians — beyond that, OOM risk is high.", S["Body"]),
        Spacer(1, 0.5*cm), PageBreak(),
    ]

    # ── Product Design ────────────────────────────────────────────────────────
    story += [
        Paragraph("Product Design Highlights", S["H1"]),
        hr(),
        Paragraph("Core User Journeys", S["H2"]),
    ]
    journeys = [
        ("The Host",
         "Creates event → shares QR code → collects photos from guests → triggers reconstruction "
         "→ reviews result → shares final link. System warns about sparse coverage before "
         "triggering GPU compute."),
        ("The Viewer",
         "Receives link → 8-second cinematic intro flythrough → free exploration → scrubs "
         "timeline → sees party evolve in 3D. No account required to view."),
        ("The Contributor",
         "Scans QR at venue (or taps link in group chat) → mobile browser, no app install → "
         "select photos from camera roll → chunked upload → 'Your 27 photos are in the mix!'"),
    ]
    for name, desc in journeys:
        story += [
            Paragraph(f"<b>{name}:</b> {desc}", S["BulletItem"]),
        ]
    story.append(Spacer(1, 0.3*cm))

    story += [
        Paragraph("3D Viewer UX Design Principles", S["H2"]),
        Paragraph(
            "Core principle: feel like <b>Google Maps 3D</b>, not Blender. "
            "Non-technical users already know pinch-to-zoom and drag-to-pan.", S["Body"]),
        Paragraph("Mouse: left-drag = orbit · scroll = zoom · right-drag = pan · double-click = recenter", S["BulletItem"]),
        Paragraph("Touch: one-finger drag = orbit · pinch = zoom · two-finger drag = pan", S["BulletItem"]),
        Paragraph("Timeline: full-width bar, 30-min buckets, density histogram, 0.4s cross-fade between windows", S["BulletItem"]),
        Paragraph("Play mode: auto-advance one window per 4 seconds — time-lapse of the entire party", S["BulletItem"]),
        Spacer(1, 0.3*cm),
        Paragraph("Progressive Loading (never show a blank screen)", S["H2"]),
        Paragraph("0–1s: Fetch scene.json → render timeline with loading skeletons", S["BulletItem"]),
        Paragraph("1–5s: Stream foundation_preview.ply (10% density, <5 MB) → user can already orbit", S["BulletItem"]),
        Paragraph("5–20s: Stream full foundation.ply in 2 MB chunks → surfaces solidify", S["BulletItem"]),
        Paragraph("On demand: time windows loaded on scrubber interaction, ±1 window prefetched", S["BulletItem"]),
        Spacer(1, 0.3*cm),
    ]

    # ── Monetization ─────────────────────────────────────────────────────────
    story += [
        Paragraph("Monetization Strategy", S["H1"]),
        hr(),
        Paragraph("Per-Event Pricing (Consumer)", S["H2"]),
    ]
    pricing_data = [
        ["Tier", "Price", "Limits", "Key Features"],
        ["Free", "$0", "1 event, 50 photos", "Memoir3D watermark on exports"],
        ["Starter", "$9 one-time", "500 photos", "No watermark, 720p flythrough export"],
        ["Pro", "$29 one-time", "5 events, 2K photos/event", "Face blur, 1080p export, password protection"],
        ["Wedding", "$79 one-time", "Unlimited photos", "4K export, embed code, priority processing"],
    ]
    t = Table(pricing_data, colWidths=[2*cm, 2.5*cm, 4.5*cm, 7*cm])
    t.setStyle(table_style())
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph("B2B Subscription — $99/month", S["H2"]),
        Paragraph(
            "Target: wedding photographers, event management companies, corporate comms teams. "
            "Includes: unlimited events, white-label viewer, client delivery portal, API access, "
            "5 team seats. High LTV, low churn — repeat buyers making 20–50 events/year.", S["Body"]),
        Spacer(1, 0.2*cm),
        Paragraph("À La Carte Add-Ons", S["H2"]),
        Paragraph("Face blur ($5) · AI highlight reel 60s ($8) · Extended storage 5yr ($12/yr) · Rush processing ($15) · Vanity URL ($8)", S["BulletItem"]),
        Spacer(1, 0.5*cm), PageBreak(),
    ]

    # ── Timeline ─────────────────────────────────────────────────────────────
    story += [
        Paragraph("Realistic Timeline Summary", S["H1"]),
        hr(),
    ]
    tl_data = [
        ["Scenario", "MVP (M6)", "Production (M7)", "Notes"],
        ["Optimistic", "Week 26 (~6.5 mo)", "Week 34 (~8.5 mo)", "Everything works first try"],
        ["Realistic ← use this", "Week 32 (~8 mo)", "Week 40 (~10 mo)", "Normal debugging, a few restarts"],
        ["Pessimistic", "Week 42 (~10.5 mo)", "Week 52 (~13 mo)", "Timeline feature requires research pivot"],
    ]
    t = Table(tl_data, colWidths=[4*cm, 4*cm, 3.5*cm, 4.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HDR),
        ("TEXTCOLOR", (0, 0), (-1, 0), TEXT_LIGHT),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID", (0, 0), (-1, -1), 0.4, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#EDE9FE")),
        ("FONTNAME", (0, 2), (-1, 2), "Helvetica-Bold"),
    ]))
    story += [t, Spacer(1, 0.3*cm)]

    story += [
        Paragraph(
            "The difference between optimistic and pessimistic is almost entirely driven by "
            "two things: (1) how long the timeline/photo-Gaussian association problem takes to "
            "solve, and (2) whether COLMAP performance on Apple Silicon is acceptable or requires "
            "architectural workarounds. Both can be validated in Phase 0 (Weeks 1–3).", S["Body"]),
        Spacer(1, 0.3*cm),
    ]

    # ── The Rule ─────────────────────────────────────────────────────────────
    story += [
        Paragraph("The One Rule", S["H1"]),
        hr(),
        Paragraph(
            "Before writing a single line of app code, take 100 photos of your room and run "
            "the full COLMAP → OpenSplat pipeline on your Mac mini. The numbers you get — "
            "training time, quality, memory usage — will inform every product decision for the "
            "next 10 months. No planning document replaces this experiment.", S["Body"]),
        Spacer(1, 0.5*cm),
        Paragraph(
            "The most important test: does the .ply file render as a recognizable room in "
            "Supersplat? If yes, the foundation is proven and you can build with confidence. "
            "If no, you have discovered the core blocker before investing months of work.", S["Body"]),
    ]

    doc.build(story)
    print(f"✓ Project Insight PDF → {path}")


if __name__ == "__main__":
    import os
    out = "/Users/dana_khaing/PROJECTS/D-Vision-3D-reconstructure/docs"
    os.makedirs(out, exist_ok=True)
    build_project_plan(f"{out}/D-Vision-3D-Project-Plan.pdf")
    build_project_insight(f"{out}/D-Vision-3D-Project-Insight.pdf")
    print("Done.")
