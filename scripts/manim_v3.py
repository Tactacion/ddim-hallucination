"""
Manim v3 — Production animations
"Why DDIM Hallucinates More than DDPM: A Theoretical Analysis of Reverse Dynamics"
ICML 2026

Scenes
------
GMMLandscape3D   → hero video  (3D probability surface, fixed camera + rotation)
DDPMvsDDIMFinal  → figures section (2D scatter: particles converge to y₀ vs escape to modes)
"""

from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
DARK_BG  = "#0D1117"
SLATE_M  = "#64748B"
SLATE_L  = "#94A3B8"
ROSE     = "#F43F5E"
TEAL     = "#14B8A6"
AMBER    = "#F59E0B"
WHITE_OP = "#E2E8F0"

# ══════════════════════════════════════════════════════════════════════════════
#  SHARED — 2-D GMM helpers used by both scenes
# ══════════════════════════════════════════════════════════════════════════════
MU_A = np.array([-1.7,  0.0])
MU_B = np.array([ 1.7,  0.0])
SIG  = 0.60          # controls width of each mode

def gmm2d(u, v):
    """Unnormalised 2-mode GMM density (normalisation cancels everywhere)."""
    p1 = np.exp(-0.5 * ((u - MU_A[0])**2 + (v - MU_A[1])**2) / SIG**2)
    p2 = np.exp(-0.5 * ((u - MU_B[0])**2 + (v - MU_B[1])**2) / SIG**2)
    return (p1 + p2) / (4 * np.pi * SIG**2)

def score2d(pos):
    """Score function ∇ log p(x) for the two-mode GMM."""
    x, y = pos[0], pos[1]
    w1 = np.exp(-0.5 * ((x - MU_A[0])**2 + (y - MU_A[1])**2) / SIG**2)
    w2 = np.exp(-0.5 * ((x - MU_B[0])**2 + (y - MU_B[1])**2) / SIG**2)
    Z  = w1 + w2 + 1e-15
    sx = (w1 * (MU_A[0] - x) + w2 * (MU_B[0] - x)) / (SIG**2 * Z)
    sy = (w1 * (MU_A[1] - y) + w2 * (MU_B[1] - y)) / (SIG**2 * Z)
    return np.array([sx, sy])

DT    = 0.09          # step size
SIG_T = 0.60          # noise level for DDPM

def ddim_step(pos):
    return pos + DT * SIG_T * score2d(pos)

def ddpm_step(pos, rng):
    noise = rng.standard_normal(2)
    return pos + DT * SIG_T * score2d(pos) + np.sqrt(2 * DT * SIG_T) * noise


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 1 — 3D Probability Landscape  (hero video)
# ══════════════════════════════════════════════════════════════════════════════
# Max density value at a mode peak (for calibrating Z_SCALE):
# gmm2d(MU_A) = 1/(4π·SIG²) ≈ 1/(4π·0.36) ≈ 0.221
# We set Z_SCALE so peak height ≈ 0.90 within a z_range of [0, 1.10].
Z_PEAK  = 1.0 / (4 * np.pi * SIG**2)   # ≈ 0.221
Z_SCALE = 0.95 / Z_PEAK                 # maps peak → 0.95

class GMMLandscape3D(ThreeDScene):
    """
    A clean 3D probability surface with:
    • Two amber peaks (true modes)
    • Indigo saddle (midpoint y₀)
    • DDIM trajectory (rose) → slides into saddle and stops
    • DDPM trajectory (teal) → escapes to true mode
    Camera is fixed at a clean angle so both peaks are fully visible.
    """

    def construct(self):
        config.background_color = DARK_BG

        # ── Axes ──────────────────────────────────────────────────────────
        axes = ThreeDAxes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[ 0.0, 1.10, 0.25],   # calibrated to Z_SCALE
            x_length=9,
            y_length=6,
            z_length=5.5,
            axis_config={
                "color"       : SLATE_M,
                "stroke_width": 1.2,
                "include_tip" : True,
                "tip_length"  : 0.14,
            },
        )
        axes.set_opacity(0.4)

        xl = MathTex("x_1",  font_size=26, color=WHITE_OP).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        yl = MathTex("x_2",  font_size=26, color=WHITE_OP).next_to(axes.y_axis.get_end(), UP,    buff=0.2)
        zl = MathTex("p(x)", font_size=26, color=WHITE_OP).next_to(axes.z_axis.get_end(), UP,    buff=0.2)
        for lbl in (xl, yl, zl):
            lbl.rotate(PI / 2, axis=RIGHT)

        # ── Surface ───────────────────────────────────────────────────────
        RES = 40
        surface = Surface(
            lambda u, v: axes.c2p(u, v, gmm2d(u, v) * Z_SCALE),
            u_range=[-3.2,  3.2],
            v_range=[-2.4,  2.4],
            resolution=(RES, RES),
        )
        surface.set_color_by_gradient(
            ManimColor("#1E1B4B"),   # deep indigo   — valley / saddle
            ManimColor("#4338CA"),   # indigo
            ManimColor("#0891B2"),   # sky-teal       — rising slope
            ManimColor("#0D9488"),   # teal
            ManimColor("#D97706"),   # amber          — peak
        )
        surface.set_style(fill_opacity=0.90, stroke_width=0.3,
                          stroke_color=WHITE, stroke_opacity=0.08)

        # ── Mode & saddle markers ──────────────────────────────────────────
        def on_surf(u, v, lift=0.06):
            return axes.c2p(u, v, gmm2d(u, v) * Z_SCALE + lift)

        peak_a  = Dot3D(on_surf(*MU_A), radius=0.12, color=AMBER)
        peak_b  = Dot3D(on_surf(*MU_B), radius=0.12, color=AMBER)
        saddle  = Dot3D(on_surf(0, 0),  radius=0.10, color=ManimColor("#FDE68A"))

        # ── Trajectory simulation ─────────────────────────────────────────
        rng = np.random.default_rng(7)

        # DDIM: starts near midpoint, drifts along x-axis → stays at saddle
        ddim_pts = []
        pos = np.array([0.30, 0.0])
        for _ in range(60):
            pos = ddim_step(pos)
            pos = np.clip(pos, [-3.1, -2.3], [3.1, 2.3])
            ddim_pts.append(on_surf(pos[0], pos[1]))

        # DDPM: starts near midpoint, noise kicks it toward left mode
        ddpm_pts = []
        pos = np.array([0.30, 0.0])
        for _ in range(60):
            pos = ddpm_step(pos, rng)
            pos = np.clip(pos, [-3.1, -2.3], [3.1, 2.3])
            ddpm_pts.append(on_surf(pos[0], pos[1]))

        start_dot = Dot3D(on_surf(0.30, 0.0), radius=0.11, color=WHITE_OP)

        # Pre-build full path VMobjects for smooth Create animation
        ddim_path = VMobject(color=ROSE, stroke_width=5, stroke_opacity=0.95)
        ddim_path.set_points_smoothly([on_surf(0.30, 0.0)] + ddim_pts)

        ddpm_path = VMobject(color=TEAL, stroke_width=5, stroke_opacity=0.95)
        ddpm_path.set_points_smoothly([on_surf(0.30, 0.0)] + ddpm_pts)

        # ── Scene assembly ─────────────────────────────────────────────────
        # Camera: low-enough phi to show both peaks, zoomed to fill frame
        self.set_camera_orientation(phi=48 * DEGREES, theta=-65 * DEGREES, zoom=0.68)
        self.add(axes, xl, yl, zl)

        # Title (fixed — appears once, stays)
        title = Text("Probability Landscape of a Gaussian Mixture",
                     font_size=28, color=WHITE_OP, weight=BOLD)
        title.to_edge(UP, buff=0.28)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, run_time=0.6))

        # Surface rises
        self.play(
            Create(surface, run_time=2.2, rate_func=smooth),
            FadeIn(peak_a, peak_b, saddle, start_dot, run_time=1.8),
        )

        # Saddle label
        y0_lbl = MathTex("y_0", font_size=26, color=ManimColor("#FDE68A"))
        y0_lbl.next_to(saddle, UP * 0.5 + RIGHT * 0.4)
        y0_lbl.rotate(PI / 2, axis=RIGHT)
        self.play(FadeIn(y0_lbl), run_time=0.4)

        # Slow ambient rotation to show depth
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(0.8)

        # ── DDIM path ─────────────────────────────────────────────────────
        ddim_end_dot = Dot3D(ddim_pts[-1], radius=0.12, color=ROSE)
        ddim_lbl = VGroup(
            Text("DDIM", font_size=28, color=ROSE, weight=BOLD),
            Text("Deterministic ODE  →  trapped at  y₀", font_size=16, color=SLATE_L),
        ).arrange(DOWN, buff=0.08)
        ddim_lbl.to_corner(UL, buff=0.38)
        self.add_fixed_in_frame_mobjects(ddim_lbl)
        self.play(FadeIn(ddim_lbl, run_time=0.5))
        self.play(Create(ddim_path, run_time=2.0, rate_func=smooth),
                  FadeIn(ddim_end_dot, run_time=0.5))

        stuck = Text("✕  hallucination", font_size=18, color=ROSE, weight=BOLD)
        stuck.next_to(ddim_lbl, DOWN, buff=0.22)
        self.add_fixed_in_frame_mobjects(stuck)
        self.play(FadeIn(stuck, run_time=0.4))
        self.wait(0.7)

        # ── DDPM path ─────────────────────────────────────────────────────
        ddpm_end_dot = Dot3D(ddpm_pts[-1], radius=0.12, color=TEAL)
        ddpm_lbl = VGroup(
            Text("DDPM", font_size=28, color=TEAL, weight=BOLD),
            Text("Stochastic SDE  →  escapes to true mode", font_size=16, color=SLATE_L),
        ).arrange(DOWN, buff=0.08)
        ddpm_lbl.to_corner(UR, buff=0.38)
        self.add_fixed_in_frame_mobjects(ddpm_lbl)
        self.play(FadeIn(ddpm_lbl, run_time=0.5))
        self.play(Create(ddpm_path, run_time=2.0, rate_func=smooth),
                  FadeIn(ddpm_end_dot, run_time=0.5))

        escaped = Text("✓  true sample", font_size=18, color=TEAL, weight=BOLD)
        escaped.next_to(ddpm_lbl, DOWN, buff=0.22)
        self.add_fixed_in_frame_mobjects(escaped)
        self.play(FadeIn(escaped, run_time=0.4))

        self.wait(4.0)
        self.stop_ambient_camera_rotation()


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 2 — Score Field Visualisation
#
#  Shows WHY DDIM hallucinates: at the midpoint y₀ the score ∇ log p(x) = 0,
#  so the deterministic ODE has no gradient to push the trajectory to a true
#  mode.  DDPM's Brownian noise term breaks the symmetry and allows escape.
#
#  Layout: single wide scene (full-width axes)
#    • Density contour rings at each mode (glowing amber)
#    • Score field arrows on a 11×11 grid — magnitude encoded in length & opacity
#    • y₀ "dead zone" ring + label "∇ log p = 0 here"
#    • DDIM particle (rose): follows flow exactly → freezes at y₀
#    • DDPM particle (teal): follows flow + noise kicks → escapes to true mode
#    • Side-by-side verdict at end
# ══════════════════════════════════════════════════════════════════════════════

class DDPMvsDDIMFinal(Scene):

    def construct(self):
        self.camera.background_color = DARK_BG

        # ── Axes (full-width) ─────────────────────────────────────────────
        AX_HALF = 3.0
        ax = Axes(
            x_range=[-AX_HALF, AX_HALF, 1],
            y_range=[-AX_HALF, AX_HALF, 1],
            x_length=10.0,
            y_length=8.0,
            axis_config={
                "color"          : SLATE_M,
                "stroke_width"   : 1.0,
                "include_tip"    : True,
                "tip_length"     : 0.12,
                "include_numbers": False,
            },
        ).move_to([0, -0.3, 0])

        ax_xl = MathTex("x_1", font_size=22, color=SLATE_M).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        ax_yl = MathTex("x_2", font_size=22, color=SLATE_M).next_to(ax.y_axis.get_end(), UP, buff=0.08)

        # ── Density contours at each mode ─────────────────────────────────
        contours = VGroup()
        for mu in [MU_A, MU_B]:
            for mult, op in [(0.4, 0.55), (0.75, 0.38), (1.15, 0.22), (1.6, 0.12), (2.1, 0.06)]:
                c = Circle(radius=mult * SIG * (10.0 / (2 * AX_HALF)),
                           color=AMBER, stroke_width=1.2, stroke_opacity=op, fill_opacity=0)
                c.move_to(ax.c2p(*mu))
                contours.add(c)

        # Mode dots
        mode_dots = VGroup(
            *[Dot(ax.c2p(*mu), radius=0.14, color=AMBER, fill_opacity=1.0) for mu in [MU_A, MU_B]]
        )
        mu1_lbl = MathTex(r"\mu_1", font_size=22, color=AMBER).next_to(ax.c2p(*MU_A), UL, buff=0.14)
        mu2_lbl = MathTex(r"\mu_2", font_size=22, color=AMBER).next_to(ax.c2p(*MU_B), UR, buff=0.14)

        # ── Score field arrows ────────────────────────────────────────────
        GRID_N  = 11
        xs = np.linspace(-AX_HALF * 0.88, AX_HALF * 0.88, GRID_N)
        ys = np.linspace(-AX_HALF * 0.88, AX_HALF * 0.88, GRID_N)
        MAX_ARROW = 0.38     # maximum arrow length in Manim units

        # Pre-compute scale: map to scene units (axis spans 10 Manim units over 2*AX_HALF data units)
        DATA_TO_SCENE = 10.0 / (2 * AX_HALF)

        arrows = VGroup()
        for xi in xs:
            for yi in ys:
                pos = np.array([xi, yi])
                s   = score2d(pos)
                mag = np.linalg.norm(s)
                if mag < 1e-4:
                    continue
                # Log-scale length so weak fields (near y₀) are still visible
                length = MAX_ARROW * np.tanh(mag * 0.7)
                direction = s / mag
                tip = pos + direction * length / DATA_TO_SCENE

                # Colour encodes magnitude: slate (low) → indigo → amber (high)
                t = min(1.0, mag / 2.5)
                col = interpolate_color(ManimColor("#334155"), ManimColor("#818CF8"), t)

                arr = Arrow(
                    ax.c2p(*pos), ax.c2p(*tip),
                    buff=0, max_tip_length_to_length_ratio=0.35,
                    stroke_width=1.6, color=col,
                )
                arr.set_opacity(0.30 + 0.55 * t)
                arrows.add(arr)

        # ── Midpoint y₀ — "dead zone" ─────────────────────────────────────
        y0_ring = Circle(radius=0.26, color=ManimColor("#FDE68A"),
                         stroke_width=2.2, stroke_opacity=0.9, fill_opacity=0)
        y0_ring.move_to(ax.c2p(0, 0))
        y0_dot = Dot(ax.c2p(0, 0), radius=0.08, color=ManimColor("#FDE68A"), fill_opacity=1.0)

        y0_lbl = MathTex(r"y_0", font_size=22, color=ManimColor("#FDE68A"))
        y0_lbl.next_to(ax.c2p(0, 0), DOWN, buff=0.22)

        zero_score_lbl = VGroup(
            MathTex(r"\nabla \log p(x) = 0", font_size=19, color=ManimColor("#FCD34D")),
            Text("no gradient — DDIM stalls here", font_size=13, color=SLATE_L),
        ).arrange(DOWN, buff=0.1)
        zero_score_lbl.next_to(y0_ring, RIGHT, buff=0.38)
        zero_score_arrow = CurvedArrow(
            zero_score_lbl.get_left() + LEFT * 0.1,
            y0_ring.get_right() + RIGHT * 0.05,
            color=ManimColor("#FCD34D"), stroke_width=1.5, angle=-0.6,
        )

        # ── Pre-compute single trajectories ──────────────────────────────
        T   = 65
        rng = np.random.default_rng(seed=5)
        START = np.array([0.06, 1.8])   # near bisector, above midpoint

        ddim_traj = [START.copy()]
        pos = START.copy()
        for _ in range(T):
            pos = ddim_step(pos)
            pos = np.clip(pos, -AX_HALF + 0.05, AX_HALF - 0.05)
            ddim_traj.append(pos.copy())

        ddpm_traj = [START.copy()]
        pos = START.copy()
        for _ in range(T):
            pos = ddpm_step(pos, rng)
            pos = np.clip(pos, -AX_HALF + 0.05, AX_HALF - 0.05)
            ddpm_traj.append(pos.copy())

        # Build smooth path VMobjects
        def make_path(traj, color, width=4.5):
            pts = [ax.c2p(*p) for p in traj]
            vm  = VMobject(color=color, stroke_width=width, stroke_opacity=0.92)
            vm.set_points_smoothly(pts)
            return vm

        ddim_path = make_path(ddim_traj, ROSE)
        ddpm_path = make_path(ddpm_traj, TEAL)

        ddim_dot  = Dot(ax.c2p(*START), radius=0.14, color=ROSE, fill_opacity=1.0)
        ddpm_dot  = Dot(ax.c2p(*START), radius=0.14, color=TEAL, fill_opacity=1.0)

        # ── Scene header ──────────────────────────────────────────────────
        title = VGroup(
            Text("Score Field  ", font_size=28, color=WHITE_OP, weight=BOLD),
            MathTex(r"\nabla \log p(x)", font_size=28, color=ManimColor("#818CF8")),
            Text("  of a Two-Mode GMM", font_size=28, color=WHITE_OP, weight=BOLD),
        ).arrange(RIGHT, buff=0.05).to_edge(UP, buff=0.30)

        # ── Build scene ───────────────────────────────────────────────────
        self.play(FadeIn(title, run_time=0.7))
        self.play(FadeIn(ax, ax_xl, ax_yl, run_time=0.6))
        self.play(FadeIn(contours, run_time=0.9), FadeIn(mode_dots, mu1_lbl, mu2_lbl, run_time=0.7))
        self.play(FadeIn(arrows, run_time=1.0, lag_ratio=0.008))
        self.wait(0.4)

        # Reveal saddle / dead zone
        self.play(
            Create(y0_ring, run_time=0.6),
            FadeIn(y0_dot, y0_lbl, run_time=0.5),
        )
        self.play(
            FadeIn(zero_score_lbl, run_time=0.6),
            Create(zero_score_arrow, run_time=0.5),
        )
        self.wait(0.8)

        # ── DDIM trajectory ───────────────────────────────────────────────
        ddim_legend = VGroup(
            Text("DDIM", font_size=22, color=ROSE, weight=BOLD),
            Text("deterministic — follows flow exactly", font_size=14, color=SLATE_L),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        ddim_legend.to_corner(UL, buff=0.45)

        self.play(FadeIn(ddim_legend, run_time=0.5), FadeIn(ddim_dot, run_time=0.4))
        self.play(
            Create(ddim_path, run_time=2.4, rate_func=smooth),
            MoveAlongPath(ddim_dot, ddim_path, run_time=2.4, rate_func=smooth),
        )

        stuck_lbl = Text("✕  stalls — zero gradient", font_size=16, color=ROSE, weight=BOLD)
        stuck_lbl.next_to(ddim_legend, DOWN, buff=0.18)
        self.play(FadeIn(stuck_lbl, run_time=0.5))
        self.wait(0.6)

        # ── DDPM trajectory ───────────────────────────────────────────────
        ddpm_legend = VGroup(
            Text("DDPM", font_size=22, color=TEAL, weight=BOLD),
            Text("stochastic — noise breaks symmetry", font_size=14, color=SLATE_L),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        ddpm_legend.to_corner(UR, buff=0.45)

        # Reset DDPM dot to start
        ddpm_dot.move_to(ax.c2p(*START))
        self.play(FadeIn(ddpm_legend, run_time=0.5), FadeIn(ddpm_dot, run_time=0.4))
        self.play(
            Create(ddpm_path, run_time=2.4, rate_func=smooth),
            MoveAlongPath(ddpm_dot, ddpm_path, run_time=2.4, rate_func=smooth),
        )

        escaped_lbl = Text("✓  escapes to true mode", font_size=16, color=TEAL, weight=BOLD)
        escaped_lbl.next_to(ddpm_legend, DOWN, buff=0.18)
        self.play(FadeIn(escaped_lbl, run_time=0.5))

        self.wait(0.5)
        # Footer
        footer = Text(
            "Ashiq · Arora · Harish · Kharbanda · Tseng · Chrysos  ·  ICML 2026",
            font_size=13, color=SLATE_M,
        ).to_edge(DOWN, buff=0.16)
        self.play(FadeIn(footer, run_time=0.5))
        self.wait(2.5)
