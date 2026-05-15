"""
Manim animation: DDPM vs DDIM Reverse Dynamics on a 2-mode Gaussian Mixture
ICML 2026 — "Why DDIM Hallucinates More than DDPM"

Usage:
    manim -pql scripts/manim_animation.py DDPMvsDDIMScene
    (replace -ql with -qh for production quality)

Output: side-by-side animation of ODE (DDIM) and SDE (DDPM) trajectories.
"""

from manim import *
import numpy as np
from scipy.interpolate import make_interp_spline

# ── Palette (matches the website / matplotlib figures) ────────────────────────
BG_COLOR   = "#F8F7F4"
SLATE      = "#1E293B"
SLATE_M    = "#475569"
SLATE_L    = "#94A3B8"
INDIGO_C   = "#4F46E5"
ROSE_C     = "#F43F5E"
TEAL_C     = "#0D9488"
AMBER_C    = "#D97706"

config.background_color = BG_COLOR
config.pixel_height = 1080
config.pixel_width  = 1920
config.frame_rate   = 30


# ─────────────────────────────────────────────────────────────────────────────
# Helper: 1D Gaussian mixture density & score
# ─────────────────────────────────────────────────────────────────────────────
MU_LEFT  = -1.6
MU_RIGHT =  1.6
SIGMA    =  0.45

def gmm_pdf(x):
    c = 1 / (SIGMA * np.sqrt(2 * np.pi))
    return 0.5 * c * (np.exp(-0.5*((x-MU_LEFT)/SIGMA)**2) +
                      np.exp(-0.5*((x-MU_RIGHT)/SIGMA)**2))

def score(x):
    wL = np.exp(-0.5*((x-MU_LEFT)/SIGMA)**2)
    wR = np.exp(-0.5*((x-MU_RIGHT)/SIGMA)**2)
    Z  = wL + wR
    return (wL*(MU_LEFT-x) + wR*(MU_RIGHT-x)) / (SIGMA**2 * Z)

# ── DDIM ODE step (deterministic) ──────────────────────────────────────────
def ddim_step(x, dt=0.04, sigma_t=0.6):
    return x + dt * sigma_t * score(x)

# ── DDPM SDE step (stochastic) ─────────────────────────────────────────────
def ddpm_step(x, dt=0.04, sigma_t=0.6, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    return x + dt * sigma_t * score(x) + np.sqrt(2 * dt * sigma_t) * rng.normal()


# ─────────────────────────────────────────────────────────────────────────────
# Main scene
# ─────────────────────────────────────────────────────────────────────────────
class DDPMvsDDIMScene(Scene):
    def construct(self):
        # ── Layout ──────────────────────────────────────────────────────────
        self.camera.background_color = BG_COLOR

        # Dividing line
        divider = Line(UP * 3.6, DOWN * 3.6, color=SLATE_L, stroke_width=1.2)
        self.add(divider)

        # Panel labels
        ddim_label = (
            Text("DDIM  (Deterministic ODE)", font_size=26, color=ROSE_C, weight=BOLD)
            .move_to(LEFT * 3.5 + UP * 3.2)
        )
        ddpm_label = (
            Text("DDPM  (Stochastic SDE)", font_size=26, color=TEAL_C, weight=BOLD)
            .move_to(RIGHT * 3.5 + UP * 3.2)
        )
        self.add(ddim_label, ddpm_label)

        # ── Axis setup (shared y-range, mirrored on each side) ──────────────
        x_range = [-2.8, 2.8]
        x_scale = 2.0  # world-units per data-unit

        def data_to_screen(x_data, panel="left"):
            x_px = x_data * x_scale
            offset = -3.5 if panel == "left" else 3.5
            return np.array([offset + x_px, 0.0, 0.0])

        # ── Density curves ──────────────────────────────────────────────────
        xs = np.linspace(-2.8, 2.8, 400)
        ys = gmm_pdf(xs)
        y_max = ys.max()
        y_scale = 1.6 / y_max   # map density peak to 1.6 units height

        def make_density_curve(panel, color):
            points = []
            for xv, yv in zip(xs, ys):
                base = data_to_screen(xv, panel)
                points.append(base + np.array([0, -1.8 + yv * y_scale, 0]))
            curve = VMobject(color=color, stroke_width=2.5, fill_opacity=0.15,
                             fill_color=color)
            # close the path for fill
            fill_pts = (
                [data_to_screen(xs[0], panel) + np.array([0, -1.8, 0])]
                + points
                + [data_to_screen(xs[-1], panel) + np.array([0, -1.8, 0])]
            )
            curve.set_points_smoothly(fill_pts)
            return curve

        for panel, color in [("left", ROSE_C), ("right", TEAL_C)]:
            self.add(make_density_curve(panel, color))

        # Baseline
        for panel in ("left", "right"):
            base = Line(
                data_to_screen(x_range[0], panel) + DOWN * 1.8,
                data_to_screen(x_range[1], panel) + DOWN * 1.8,
                color=SLATE_L, stroke_width=0.8
            )
            self.add(base)

        # Mode markers
        for panel in ("left", "right"):
            for mu in [MU_LEFT, MU_RIGHT]:
                pos = data_to_screen(mu, panel) + DOWN * 1.8
                dot = Dot(pos, radius=0.07, color=SLATE, fill_opacity=0.8)
                lbl = MathTex(r"\mu", font_size=18, color=SLATE_M).next_to(dot, DOWN, buff=0.12)
                self.add(dot, lbl)

        # Midpoint marker
        for panel in ("left", "right"):
            mpos = data_to_screen(0.0, panel) + DOWN * 1.8
            mid_dot = Dot(mpos, radius=0.07, color=AMBER_C)
            mid_lbl = MathTex(r"y_0", font_size=18, color=AMBER_C).next_to(mid_dot, DOWN*0.9, buff=0.12)
            self.add(mid_dot, mid_lbl)

        # ── Intro text ───────────────────────────────────────────────────────
        intro = (
            Text(
                "Both samplers start at x₀ = 0 (the midpoint between two modes)",
                font_size=21, color=SLATE_M
            )
            .move_to(DOWN * 3.2)
        )
        self.play(FadeIn(intro, run_time=0.8))
        self.wait(1.0)
        self.play(FadeOut(intro))

        # ── Simulate trajectories ────────────────────────────────────────────
        N_STEPS    = 80
        N_TRAJ     = 10
        rng        = np.random.default_rng(seed=7)
        x0_vals    = rng.normal(0, 0.05, N_TRAJ)   # start near midpoint

        ddim_trajs = []
        ddpm_trajs = []
        for x0 in x0_vals:
            # DDIM
            traj = [x0]
            for _ in range(N_STEPS):
                traj.append(np.clip(ddim_step(traj[-1]), *x_range))
            ddim_trajs.append(traj)
            # DDPM
            traj = [x0]
            for _ in range(N_STEPS):
                traj.append(np.clip(ddpm_step(traj[-1], rng=rng), *x_range))
            ddpm_trajs.append(traj)

        # ── Draw starting dots ───────────────────────────────────────────────
        ddim_dots, ddpm_dots = [], []
        for x0, traj_d, traj_p in zip(x0_vals, ddim_trajs, ddpm_trajs):
            y_base = -1.8 + gmm_pdf(x0) * y_scale * 0.3  # lift slightly off baseline
            for panel, color, store, traj in [
                ("left",  ROSE_C, ddim_dots, traj_d),
                ("right", TEAL_C, ddpm_dots, traj_p),
            ]:
                d = Dot(
                    data_to_screen(x0, panel) + np.array([0, y_base + 1.8, 0]),
                    radius=0.055,
                    color=color,
                    fill_opacity=0.8,
                )
                store.append(d)

        self.play(*[FadeIn(d, scale=0.4) for d in ddim_dots + ddpm_dots], run_time=0.6)
        self.wait(0.5)

        # ── Animate step by step (batch into groups for speed) ──────────────
        KEYFRAMES = list(range(0, N_STEPS, 2))  # every 2nd step

        def dot_pos(x_data, panel):
            y_up = -1.8 + gmm_pdf(np.clip(x_data, *x_range)) * y_scale * 0.18
            return data_to_screen(x_data, panel) + np.array([0, y_up + 1.8, 0])

        for step in KEYFRAMES:
            anims = []
            for i, (traj_d, traj_p, dd, dp) in enumerate(
                zip(ddim_trajs, ddpm_trajs, ddim_dots, ddpm_dots)
            ):
                next_d = traj_d[min(step+2, N_STEPS)]
                next_p = traj_p[min(step+2, N_STEPS)]
                anims.append(dd.animate.move_to(dot_pos(next_d, "left")))
                anims.append(dp.animate.move_to(dot_pos(next_p, "right")))
            self.play(*anims, run_time=0.07, rate_func=linear)

        self.wait(0.8)

        # ── Final state annotation ────────────────────────────────────────────
        final_ddim_x = np.mean([t[-1] for t in ddim_trajs])
        final_ddpm_x = np.mean([t[-1] for t in ddpm_trajs])

        ddim_result_lbl = (
            Text("Trapped near y₀\n(hallucination)", font_size=20, color=ROSE_C, weight=BOLD)
            .move_to(data_to_screen(final_ddim_x, "left") + UP * 0.8)
        )
        ddpm_result_lbl = (
            Text("Escaped to true mode", font_size=20, color=TEAL_C, weight=BOLD)
            .move_to(data_to_screen(final_ddpm_x, "right") + UP * 0.8)
        )
        self.play(
            FadeIn(ddim_result_lbl, shift=UP * 0.2),
            FadeIn(ddpm_result_lbl, shift=UP * 0.2),
            run_time=0.7,
        )
        self.wait(1.5)

        # ── Conclusion text ───────────────────────────────────────────────────
        conclusion = (
            Text(
                "DDPM's stochastic noise is the key to escaping the midpoint trap.",
                font_size=22, color=SLATE,
            )
            .move_to(DOWN * 3.2)
        )
        self.play(FadeIn(conclusion, shift=UP * 0.15), run_time=0.8)
        self.wait(2.5)
        self.play(FadeOut(conclusion))


# ─────────────────────────────────────────────────────────────────────────────
# Scene 2: Score field with animated particle
# ─────────────────────────────────────────────────────────────────────────────
class ScoreFieldScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text(
            "Score Field  ∇ log p(x)  of a Two-Mode Gaussian Mixture",
            font_size=28, color=SLATE, weight=BOLD,
        ).to_edge(UP, buff=0.4)
        self.add(title)

        xs = np.linspace(-3.0, 3.0, 500)
        ys_pdf   = np.array([gmm_pdf(x) for x in xs])
        ys_score = np.array([score(x) for x in xs])

        # Axes
        ax_pdf = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, ys_pdf.max() * 1.15, 0.1],
            x_length=11,
            y_length=2.6,
            axis_config={"color": SLATE_L, "stroke_width": 1.2,
                         "include_tip": False, "include_numbers": False},
        ).move_to(UP * 1.2)

        ax_score = Axes(
            x_range=[-3, 3, 1],
            y_range=[-5, 5, 1],
            x_length=11,
            y_length=2.6,
            axis_config={"color": SLATE_L, "stroke_width": 1.2,
                         "include_tip": False, "include_numbers": True},
        ).move_to(DOWN * 2.0)

        # PDF curve
        pdf_curve = ax_pdf.plot(
            lambda x: gmm_pdf(x), x_range=[-3, 3],
            color=INDIGO_C, stroke_width=2.8,
        )
        pdf_fill = ax_pdf.get_area(pdf_curve, x_range=[-3, 3], color=INDIGO_C, opacity=0.12)

        # Score curve
        score_curve = ax_score.plot(
            lambda x: score(x), x_range=[-2.99, 2.99],
            color=ROSE_C, stroke_width=2.8,
        )
        zero_line = DashedLine(
            ax_score.c2p(-3, 0), ax_score.c2p(3, 0),
            color=SLATE_L, stroke_width=0.8,
        )

        # Labels
        pdf_lbl   = MathTex(r"p(x)", font_size=26, color=INDIGO_C).next_to(ax_pdf, LEFT, buff=0.1)
        score_lbl = MathTex(r"\nabla\!\log p(x)", font_size=26, color=ROSE_C).next_to(ax_score, LEFT, buff=0.1)

        # Mode lines
        mode_lines = VGroup()
        for mu in [MU_LEFT, MU_RIGHT]:
            for ax_obj in [ax_pdf, ax_score]:
                mode_lines.add(
                    DashedLine(ax_obj.c2p(mu, ax_obj.y_range[0]),
                               ax_obj.c2p(mu, ax_obj.y_range[1]),
                               color=SLATE_L, stroke_width=1.0).set_opacity(0.6)
                )

        # Midpoint highlight
        mid_region_score = ax_score.get_area(
            ax_score.plot(lambda x: score(x), x_range=[-0.55, 0.55]),
            x_range=[-0.55, 0.55], color=AMBER_C, opacity=0.18,
        )
        mid_dot_pdf = Dot(ax_pdf.c2p(0, gmm_pdf(0)), color=AMBER_C, radius=0.08)
        mid_dot_score = Dot(ax_score.c2p(0, score(0)), color=AMBER_C, radius=0.08)
        mid_lbl = (
            Text("Unstable\nequilibrium y₀", font_size=16, color=AMBER_C)
            .next_to(ax_score.c2p(0, score(0.02)), RIGHT * 0.1 + UP * 0.4)
        )

        # Build up
        self.play(
            Create(ax_pdf), Create(ax_score), run_time=0.8,
        )
        self.play(
            Create(pdf_curve), FadeIn(pdf_fill), FadeIn(pdf_lbl),
            run_time=0.9,
        )
        self.play(
            Create(score_curve), FadeIn(zero_line), FadeIn(score_lbl),
            FadeIn(mode_lines),
            run_time=0.9,
        )
        self.play(
            FadeIn(mid_region_score), FadeIn(mid_dot_pdf), FadeIn(mid_dot_score),
            FadeIn(mid_lbl),
            run_time=0.7,
        )
        self.wait(0.5)

        # Animate a DDIM particle (stays near 0)
        ddim_particle = Dot(ax_score.c2p(0.18, 0), color=ROSE_C, radius=0.11)
        ddim_path_pts = [0.18]
        x_cur = 0.18
        for _ in range(60):
            x_cur = x_cur + 0.02 * score(x_cur)
            ddim_path_pts.append(np.clip(x_cur, -2.9, 2.9))

        self.add(ddim_particle)
        ddim_trace = TracedPath(ddim_particle.get_center, stroke_color=ROSE_C,
                                stroke_width=1.6, stroke_opacity=0.5)
        self.add(ddim_trace)

        for x_next in ddim_path_pts[1:]:
            self.play(
                ddim_particle.animate.move_to(ax_score.c2p(x_next, score(x_next))),
                run_time=0.04, rate_func=linear,
            )

        ddim_stuck = Text("DDIM stuck", font_size=17, color=ROSE_C).next_to(ddim_particle, UP * 0.6)
        self.play(FadeIn(ddim_stuck), run_time=0.4)
        self.wait(0.6)

        # Animate a DDPM particle (escapes)
        ddpm_particle = Dot(ax_score.c2p(0.18, 0), color=TEAL_C, radius=0.11)
        rng = np.random.default_rng(seed=3)
        ddpm_path = [0.18]
        x_cur = 0.18
        for _ in range(60):
            x_cur = x_cur + 0.02 * score(x_cur) + 0.18 * rng.normal()
            ddpm_path.append(np.clip(x_cur, -2.9, 2.9))

        self.add(ddpm_particle)
        ddpm_trace = TracedPath(ddpm_particle.get_center, stroke_color=TEAL_C,
                                stroke_width=1.6, stroke_opacity=0.5)
        self.add(ddpm_trace)

        for x_next in ddpm_path[1:]:
            self.play(
                ddpm_particle.animate.move_to(ax_score.c2p(x_next, score(x_next))),
                run_time=0.04, rate_func=linear,
            )

        ddpm_escaped = Text("DDPM escaped!", font_size=17, color=TEAL_C).next_to(ddpm_particle, UP * 0.6)
        self.play(FadeIn(ddpm_escaped), run_time=0.4)
        self.wait(2.5)
