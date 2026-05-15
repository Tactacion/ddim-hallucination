"""
Extract the actual figures from the paper PDF pages (rendered at 300 DPI = 2550x3300 px).
All coordinates determined by visual inspection. Adds 12px white padding on all sides.
"""

from PIL import Image, ImageOps
import os

OUT  = "/Users/revanshphull/ddpm-site/public/assets"
BASE = "/tmp/paper_hires"

def load(page):
    return Image.open(f"{BASE}-0{page}.png").convert("RGB")

def crop_and_save(img, box, name, pad=22):
    """
    box = (left, upper, right, lower) in 300-dpi pixel coords.
    Adds white padding, saves as PNG.
    """
    cropped = img.crop(box)
    padded  = ImageOps.expand(cropped, border=pad, fill=(248, 247, 244))  # site bg colour
    out_path = os.path.join(OUT, name)
    padded.save(out_path, "PNG", optimize=True)
    w, h = padded.size
    print(f"  {name}  {w}×{h} px")

print("Extracting paper figures…\n")

# ── Page 3 ────────────────────────────────────────────────────────────────────
# Figure 2 — three-panel DDPM vs DDIM sample comparison (25-mode GMM)
# Runs full width, top portion of page; includes caption
p3 = load(3)
crop_and_save(p3,
    (62, 148, 2488, 1060),   # L, T, R, B
    "paper_fig2_samples.png")

# ── Page 4 ────────────────────────────────────────────────────────────────────
# Figure 2 (continued) — geometric diagram with modes, bisector, ε-ball
# Right column only
p4 = load(4)
crop_and_save(p4,
    (1278, 62, 2488, 930),
    "paper_fig2_geometry.png")

# ── Page 7 ────────────────────────────────────────────────────────────────────
# Figure 3 — Hallucination rate vs DDIM timesteps (right column, detected bounds)
p7 = load(7)
crop_and_save(p7,
    (1300, 200, 2260, 900),
    "paper_fig3_halluc.png")

# ── Page 8 ────────────────────────────────────────────────────────────────────
p8 = load(8)

# Figure 4 — Convergence plots, both panels, full width (detected bounds)
crop_and_save(p8,
    (62, 199, 2488, 1050),
    "paper_fig4_convergence.png")

# Figure 5 — Hallucination rate vs radius, right column (detected bounds)
crop_and_save(p8,
    (1301, 960, 2256, 1750),
    "paper_fig5_radius.png")

print("\n✓ All paper figures extracted to", OUT)
