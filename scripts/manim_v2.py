"""
Manim v2 — Production animations for
"Why DDIM Hallucinates More than DDPM: A Theoretical Analysis of Reverse Dynamics"
ICML 2026

Scenes
------
GMMLandscape3D   →  hero video  (3D probability surface, rotating camera)
DDPMvsDDIMFinal  →  figures section  (crisp 2D comparison, dark bg)
"""

from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
PAGE_BG  = "#F8F7F4"
DARK_BG  = "#0D1117"          # near-black for 3D / dark scenes
SLATE    = "#1E293B"
SLATE_M  = "#64748B"
SLATE_L  = "#CBD5E1"
INDIGO   = "#6366F1"
ROSE     = "#F43F5E"
TEAL     = "#14B8A6"
AMBER    = "#F59E0B"
EMERALD  = "#10B981"
WHITE_OP = "#E2E8F0"

# ── GMM helpers ───────────────────────────────────────────────────────────────
MU_L, MU_R, SIG_1D = -1.8, 1.8, 0.48

def gmm1d(x):
    c = 1.0 / (SIG_1D * np.sqrt(2 * np.pi))
    return 0.5 * c * (
        np.exp(-0.5 * ((x - MU_L) / SIG_1D) ** 2) +
        np.exp(-0.5 * ((x - MU_R) / SIG_1D) ** 2)
    )

def score1d(x):
    wL = np.exp(-0.5 * ((x - MU_L) / SIG_1D) ** 2)
    wR = np.exp(-0.5 * ((x - MU_R) / SIG_1D) ** 2)
    Z  = wL + wR + 1e-12
    return (wL * (MU_L - x) + wR * (MU_R - x)) / (SIG_1D ** 2 * Z)

def ddim_step(x, dt=0.06, sig_t=0.7):
    return x + dt * sig_t * score1d(x)

def ddpm_step(x, dt=0.06, sig_t=0.7, rng=None):
    rng = rng or np.random.default_rng()
    return x + dt * sig_t * score1d(x) + np.sqrt(2 * dt * sig_t) * rng.normal()

# ── 2D GMM for 3D surface ─────────────────────────────────────────────────────
MU1_2D = np.array([-1.6,  0.0])
MU2_2D = np.array([ 1.6,  0.0])
SIG_2D = 0.55

def gmm2d(u, v):
    p1 = np.exp(-0.5 * ((u - MU1_2D[0])**2 + (v - MU1_2D[1])**2) / SIG_2D**2)
    p2 = np.exp(-0.5 * ((u - MU2_2D[0])**2 + (v - MU2_2D[1])**2) / SIG_2D**2)
    return (p1 + p2) / (2 * 2 * np.pi * SIG_2D**2)

Z_SCALE  = 7.0          # amplify height for visual clarity
Z_OFFSET = 0.0


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 1 — 3D GMM Probability Landscape (hero video)
# ══════════════════════════════════════════════════════════════════════════════
class GMMLandscape3D(ThreeDScene):
    """
    Rotating 3D probability landscape.
    - Two tall peaks = true modes
    - Low saddle between them = midpoint / hallucination zone
    - DDIM trajectory (rose) slides to saddle and stops
    - DDPM trajectory (teal) jolts sideways and climbs to a peak
    """

    def construct(self):
        config.background_color = DARK_BG

        # ── Axes ──────────────────────────────────────────────────────────
        axes = ThreeDAxes(
            x_range=[-3.2, 3.2, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[ 0.0, 0.55, 0.1],
            x_length=9,
            y_length=6,
            z_length=5,
            axis_config={
                "color"        : SLATE_M,
                "stroke_width" : 1.0,
                "include_tip"  : True,
                "tip_length"   : 0.15,
            },
        )
        axes.set_opacity(0.45)

        # Axis labels (fixed in frame so they stay readable during rotation)
        lbl_x = MathTex("x_1", font_size=28, color=WHITE_OP).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        lbl_y = MathTex("x_2", font_size=28, color=WHITE_OP).next_to(axes.y_axis.get_end(), UP,    buff=0.2)
        lbl_z = MathTex("p(x)", font_size=28, color=WHITE_OP).next_to(axes.z_axis.get_end(), UP,   buff=0.2)
        for lbl in (lbl_x, lbl_y, lbl_z):
            lbl.rotate(PI/2, axis=RIGHT)

        # ── Surface ───────────────────────────────────────────────────────
        RES = 36
        surface = Surface(
            lambda u, v: axes.c2p(u, v, gmm2d(u, v) * Z_SCALE + Z_OFFSET),
            u_range=[-3.2, 3.2],
            v_range=[-2.4, 2.4],
            resolution=(RES, RES),
        )
        # Color by z-value: deep indigo valley → teal slope → gold peak
        surface.set_color_by_gradient(
            ManimColor("#312E81"),   # deep indigo   (low, saddle)
            ManimColor("#4F46E5"),   # indigo
            ManimColor("#0D9488"),   # teal          (mid slope)
            ManimColor("#F59E0B"),   # amber         (peak)
        )
        surface.set_style(fill_opacity=0.88, stroke_width=0.25,
                          stroke_color=WHITE, stroke_opacity=0.15)

        # ── Mode markers ──────────────────────────────────────────────────
        z_peak1 = gmm2d(*MU1_2D) * Z_SCALE
        z_peak2 = gmm2d(*MU2_2D) * Z_SCALE
        z_saddle = gmm2d(0, 0) * Z_SCALE

        peak1  = Dot3D(axes.c2p(*MU1_2D, z_peak1),  radius=0.12, color=AMBER)
        peak2  = Dot3D(axes.c2p(*MU2_2D, z_peak2),  radius=0.12, color=AMBER)
        saddle = Dot3D(axes.c2p(0, 0, z_saddle), radius=0.10, color=ManimColor("#FCD34D"))

        # ── Build 3D trajectories ─────────────────────────────────────────
        rng = np.random.default_rng(seed=42)

        def on_surface(x, y):
            return axes.c2p(x, y, gmm2d(x, y) * Z_SCALE + 0.04)

        # DDIM: deterministic, drifts toward saddle along x-axis
        ddim_path_pts = []
        x_cur = 0.35
        for _ in range(55):
            x_cur = np.clip(ddim_step(x_cur, dt=0.05, sig_t=0.65), -3, 3)
            ddim_path_pts.append(on_surface(x_cur, 0.0))

        # DDPM: stochastic, escapes toward MU1
        ddpm_path_pts = []
        x_cur, y_cur = 0.35, 0.0
        for _ in range(55):
            nx = np.clip(ddpm_step(x_cur, dt=0.05, sig_t=0.65, rng=rng), -3, 3)
            ny = np.clip(y_cur + 0.04 * rng.normal(), -2.3, 2.3)
            x_cur, y_cur = nx, ny
            ddpm_path_pts.append(on_surface(x_cur, y_cur))

        ddim_line = VMobject(color=ROSE, stroke_width=4.5, stroke_opacity=0.95)
        ddim_line.set_points_smoothly([ddim_path_pts[0]])

        ddpm_line = VMobject(color=TEAL, stroke_width=4.5, stroke_opacity=0.95)
        ddpm_line.set_points_smoothly([ddpm_path_pts[0]])

        start_dot = Dot3D(on_surface(0.35, 0.0), radius=0.10, color=WHITE_OP)

        # ── Scene assembly ─────────────────────────────────────────────────
        self.set_camera_orientation(phi=62 * DEGREES, theta=-68 * DEGREES, zoom=0.72)
        self.add(axes, lbl_x, lbl_y, lbl_z)

        # Title (fixed in frame)
        title = Text("Probability Landscape of a Gaussian Mixture",
                     font_size=30, color=WHITE_OP, weight=BOLD)
        title.to_edge(UP, buff=0.25)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, run_time=0.7))

        # Surface rises in
        self.play(
            Create(surface, run_time=2.0, rate_func=smooth),
            FadeIn(peak1, peak2, saddle, run_time=1.5),
        )

        # Saddle label
        saddle_lbl = Text("Midpoint  y₀", font_size=20, color=AMBER)
        saddle_lbl.next_to(saddle, UP * 0.6 + RIGHT * 0.2)
        saddle_lbl.rotate(PI/2, axis=RIGHT)
        self.play(FadeIn(saddle_lbl), run_time=0.5)

        # Start ambient rotation
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(1.0)

        # ── DDIM animation ─────────────────────────────────────────────────
        ddim_title = Text("DDIM  (Deterministic ODE) →  trapped at y₀",
                          font_size=22, color=ROSE, weight=BOLD)
        ddim_title.to_corner(UL, buff=0.35)
        self.add_fixed_in_frame_mobjects(ddim_title)
        self.play(FadeIn(ddim_title, run_time=0.5), FadeIn(start_dot, run_time=0.4))
        self.add(ddim_line)

        ddim_dot = Dot3D(ddim_path_pts[0], radius=0.12, color=ROSE)
        self.add(ddim_dot)

        for idx, pt in enumerate(ddim_path_pts[1:], start=1):
            new_line = ddim_line.copy()
            new_line.set_points_smoothly(ddim_path_pts[:idx+1])
            self.play(
                Transform(ddim_line, new_line),
                ddim_dot.animate.move_to(pt),
                run_time=0.06,
                rate_func=linear,
            )

        # "Stuck" indicator
        stuck = Text("✕  HALLUCINATION", font_size=22, color=ROSE, weight=BOLD)
        stuck.next_to(ddim_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(stuck)
        self.play(FadeIn(stuck, run_time=0.5))
        self.wait(0.6)

        # ── DDPM animation ─────────────────────────────────────────────────
        ddpm_title = Text("DDPM  (Stochastic SDE) →  escapes to true mode",
                          font_size=22, color=TEAL, weight=BOLD)
        ddpm_title.to_corner(UR, buff=0.35)
        self.add_fixed_in_frame_mobjects(ddpm_title)
        self.play(FadeIn(ddpm_title, run_time=0.5))
        self.add(ddpm_line)

        ddpm_dot = Dot3D(ddpm_path_pts[0], radius=0.12, color=TEAL)
        self.add(ddpm_dot)

        for idx, pt in enumerate(ddpm_path_pts[1:], start=1):
            new_line = ddpm_line.copy()
            new_line.set_points_smoothly(ddpm_path_pts[:idx+1])
            self.play(
                Transform(ddpm_line, new_line),
                ddpm_dot.animate.move_to(pt),
                run_time=0.06,
                rate_func=linear,
            )

        escaped = Text("✓  TRUE SAMPLE", font_size=22, color=TEAL, weight=BOLD)
        escaped.next_to(ddpm_title, DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(escaped)
        self.play(FadeIn(escaped, run_time=0.5))

        self.wait(3.5)
        self.stop_ambient_camera_rotation()


# ══════════════════════════════════════════════════════════════════════════════
#  SCENE 2 — Clean 2D Side-by-Side (dark bg, crisp, bold)
# ══════════════════════════════════════════════════════════════════════════════
class DDPMvsDDIMFinal(Scene):
    """
    Dark-background 2D scene. Shows DDIM and DDPM trajectories side by side
    on an explicit GMM density, with large particles and traced paths.
    """

    def construct(self):
        self.camera.background_color = DARK_BG

        X_RANGE  = [-3.2, 3.2]
        AX_W, AX_H = 8.2, 3.2
        LEFT_CX  = -4.8
        RIGHT_CX =  4.8

        # ── Axes ──────────────────────────────────────────────────────────
        ax_cfg = dict(
            x_range=[X_RANGE[0], X_RANGE[1], 1],
            y_range=[0, 0.60, 0.1],
            x_length=AX_W,
            y_length=AX_H,
            axis_config={
                "color": SLATE_M, "stroke_width": 1.4,
                "include_tip": True, "tip_length": 0.15,
                "include_numbers": False,
            },
        )
        ddim_ax = Axes(**ax_cfg).move_to([LEFT_CX,  -0.6, 0])
        ddpm_ax = Axes(**ax_cfg).move_to([RIGHT_CX, -0.6, 0])

        # ── Density curves ────────────────────────────────────────────────
        ddim_curve = ddim_ax.plot(gmm1d, x_range=X_RANGE, color=ROSE,   stroke_width=3.5)
        ddpm_curve = ddpm_ax.plot(gmm1d, x_range=X_RANGE, color=TEAL,   stroke_width=3.5)
        ddim_fill  = ddim_ax.get_area(ddim_curve, x_range=X_RANGE, color=ROSE, opacity=0.14)
        ddpm_fill  = ddpm_ax.get_area(ddpm_curve, x_range=X_RANGE, color=TEAL, opacity=0.14)

        # Axis labels
        for ax, xcolor in [(ddim_ax, ROSE), (ddpm_ax, TEAL)]:
            ax.get_x_axis().set_color(xcolor).set_opacity(0.5)
            ax.get_y_axis().set_color(xcolor).set_opacity(0.5)

        # ── Static markers ────────────────────────────────────────────────
        def add_markers(ax):
            mobs = VGroup()
            for mu, c in [(MU_L, WHITE_OP), (MU_R, WHITE_OP)]:
                d = Dot(ax.c2p(mu, gmm1d(mu)), radius=0.10, color=c, fill_opacity=0.9)
                l = MathTex(r"\mu", font_size=20, color=c).next_to(d, UP, buff=0.12)
                mobs.add(d, l)
            mid = Dot(ax.c2p(0, gmm1d(0)), radius=0.10, color=AMBER, fill_opacity=1)
            ml  = MathTex("y_0", font_size=20, color=AMBER).next_to(mid, DOWN, buff=0.12)
            mobs.add(mid, ml)
            return mobs

        ddim_markers = add_markers(ddim_ax)
        ddpm_markers = add_markers(ddpm_ax)

        # ── Panel titles ──────────────────────────────────────────────────
        ddim_title = VGroup(
            Text("DDIM", font_size=34, color=ROSE, weight=BOLD),
            Text("Deterministic Reverse ODE", font_size=18, color=SLATE_M),
        ).arrange(DOWN, buff=0.08).move_to([LEFT_CX, 3.2, 0])

        ddpm_title = VGroup(
            Text("DDPM", font_size=34, color=TEAL, weight=BOLD),
            Text("Stochastic Reverse SDE", font_size=18, color=SLATE_M),
        ).arrange(DOWN, buff=0.08).move_to([RIGHT_CX, 3.2, 0])

        divider = Line([0, 4.0, 0], [0, -3.8, 0], color=SLATE_M,
                       stroke_width=1.0, stroke_opacity=0.35)

        # ── Build scene ───────────────────────────────────────────────────
        self.add(divider)
        self.play(
            FadeIn(ddim_ax, ddpm_ax, run_time=0.6),
            FadeIn(ddim_title, ddpm_title, run_time=0.6),
        )
        self.play(
            Create(ddim_curve), Create(ddpm_curve),
            FadeIn(ddim_fill),  FadeIn(ddpm_fill),
            run_time=0.9,
        )
        self.play(FadeIn(ddim_markers, ddpm_markers), run_time=0.5)
        self.wait(0.4)

        # ── Simulate trajectories ─────────────────────────────────────────
        N_TRAJ   = 8
        N_STEPS  = 70
        rng      = np.random.default_rng(seed=99)
        x0_vals  = rng.uniform(-0.15, 0.15, N_TRAJ)

        ddim_trajs, ddpm_trajs = [], []
        for x0 in x0_vals:
            d_traj = [x0]
            for _ in range(N_STEPS):
                d_traj.append(np.clip(ddim_step(d_traj[-1]), *X_RANGE))
            ddim_trajs.append(d_traj)

            p_traj = [x0]
            for _ in range(N_STEPS):
                p_traj.append(np.clip(ddpm_step(p_traj[-1], rng=rng), *X_RANGE))
            ddpm_trajs.append(p_traj)

        # Gradient colors for individual trajectories
        ddim_colors = color_gradient([ROSE, "#FF6B6B", "#FCA5A5", ROSE,
                                      "#E11D48", "#FB7185", ROSE, "#BE123C"], N_TRAJ)
        ddpm_colors = color_gradient([TEAL, "#34D399", "#6EE7B7", TEAL,
                                      "#059669", "#A7F3D0", TEAL, "#065F46"], N_TRAJ)

        # Create traced path lines and dots
        ddim_lines, ddim_dots = [], []
        ddpm_lines, ddpm_dots = [], []

        lift = 0.04  # lift dots slightly off the density curve

        for i, (d_tr, p_tr, dc, pc) in enumerate(
                zip(ddim_trajs, ddpm_trajs, ddim_colors, ddpm_colors)):
            x0 = x0_vals[i]
            y0 = gmm1d(x0) + lift

            dl = VMobject(color=dc, stroke_width=2.8, stroke_opacity=0.9)
            dl.set_points_as_corners([ddim_ax.c2p(x0, y0)] * 2)
            dd = Dot(ddim_ax.c2p(x0, y0), radius=0.11, color=dc, fill_opacity=0.95)
            ddim_lines.append(dl); ddim_dots.append(dd)

            pl = VMobject(color=pc, stroke_width=2.8, stroke_opacity=0.9)
            pl.set_points_as_corners([ddpm_ax.c2p(x0, y0)] * 2)
            pd = Dot(ddpm_ax.c2p(x0, y0), radius=0.11, color=pc, fill_opacity=0.95)
            ddpm_lines.append(pl); ddpm_dots.append(pd)

        self.play(
            *[FadeIn(d, scale=0.5) for d in ddim_dots + ddpm_dots],
            run_time=0.5,
        )
        self.add(*ddim_lines, *ddpm_lines)

        # ── Animate step by step ──────────────────────────────────────────
        STEP_BATCH = 2   # advance this many steps per animation frame
        for step in range(0, N_STEPS, STEP_BATCH):
            anims = []
            for i in range(N_TRAJ):
                # DDIM
                s = min(step + STEP_BATCH, N_STEPS)
                dx = ddim_trajs[i][s]
                dy = gmm1d(dx) + lift
                new_dl = VMobject(color=ddim_colors[i], stroke_width=2.8, stroke_opacity=0.9)
                pts_d  = [ddim_ax.c2p(ddim_trajs[i][k], gmm1d(ddim_trajs[i][k]) + lift)
                          for k in range(0, s+1, max(1, s//20))]
                new_dl.set_points_smoothly(pts_d if len(pts_d) >= 2 else pts_d * 2)
                anims.append(Transform(ddim_lines[i], new_dl, rate_func=linear))
                anims.append(ddim_dots[i].animate.move_to(ddim_ax.c2p(dx, dy)))

                # DDPM
                px = ddpm_trajs[i][s]
                py = gmm1d(px) + lift
                new_pl = VMobject(color=ddpm_colors[i], stroke_width=2.8, stroke_opacity=0.9)
                pts_p  = [ddpm_ax.c2p(ddpm_trajs[i][k], gmm1d(ddpm_trajs[i][k]) + lift)
                          for k in range(0, s+1, max(1, s//20))]
                new_pl.set_points_smoothly(pts_p if len(pts_p) >= 2 else pts_p * 2)
                anims.append(Transform(ddpm_lines[i], new_pl, rate_func=linear))
                anims.append(ddpm_dots[i].animate.move_to(ddpm_ax.c2p(px, py)))

            self.play(*anims, run_time=0.07, rate_func=linear)

        self.wait(0.5)

        # ── Final annotations ─────────────────────────────────────────────
        ddim_verdict = VGroup(
            Text("Trapped at  y₀", font_size=22, color=ROSE, weight=BOLD),
            Text("→  hallucination", font_size=17, color=SLATE_M),
        ).arrange(DOWN, buff=0.08).move_to([LEFT_CX, -3.2, 0])

        ddpm_verdict = VGroup(
            Text("Escaped to  μ", font_size=22, color=TEAL, weight=BOLD),
            Text("→  true sample", font_size=17, color=SLATE_M),
        ).arrange(DOWN, buff=0.08).move_to([RIGHT_CX, -3.2, 0])

        self.play(
            FadeIn(ddim_verdict, shift=UP * 0.2),
            FadeIn(ddpm_verdict, shift=UP * 0.2),
            run_time=0.7,
        )
        self.wait(2.5)

        # ── Footer ────────────────────────────────────────────────────────
        footer = Text(
            "Ashiq · Arora · Harish · Kharbanda · Tseng · Chrysos  ·  ICML 2026",
            font_size=15, color=SLATE_M,
        ).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(footer), run_time=0.6)
        self.wait(1.5)
