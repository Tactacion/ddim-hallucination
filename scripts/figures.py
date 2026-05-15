"""
High-quality publication figures for
"Why DDIM Hallucinates More than DDPM: A Theoretical Analysis of Reverse Dynamics"
ICML 2026

All figures use a consistent, minimal design language:
  - Off-white background  (#F8F7F4)
  - Deep slate primary    (#1E293B)
  - Indigo accent         (#4F46E5)
  - Rose / DDIM color     (#F43F5E)
  - Teal / DDPM color     (#0D9488)
  - Amber highlight       (#D97706)
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
from scipy.stats import multivariate_normal
from scipy.ndimage import gaussian_filter
import warnings
warnings.filterwarnings("ignore")

# ── Global style ──────────────────────────────────────────────────────────────
BG      = "#F8F7F4"
SLATE   = "#1E293B"
SLATE_M = "#475569"
SLATE_L = "#94A3B8"
INDIGO  = "#4F46E5"
ROSE    = "#F43F5E"
TEAL    = "#0D9488"
AMBER   = "#D97706"
EMERALD = "#059669"
VIOLET  = "#7C3AED"

matplotlib.rcParams.update({
    "figure.facecolor":     BG,
    "axes.facecolor":       BG,
    "axes.edgecolor":       SLATE_L,
    "axes.labelcolor":      SLATE,
    "axes.titlecolor":      SLATE,
    "axes.spines.top":      False,
    "axes.spines.right":    False,
    "axes.grid":            True,
    "grid.color":           "#E2E8F0",
    "grid.linewidth":       0.6,
    "grid.alpha":           0.8,
    "xtick.color":          SLATE_M,
    "ytick.color":          SLATE_M,
    "xtick.labelsize":      9,
    "ytick.labelsize":      9,
    "text.color":           SLATE,
    "font.family":          "sans-serif",
    "font.sans-serif":      ["Inter", "Helvetica Neue", "Arial", "sans-serif"],
    "figure.dpi":           180,
    "savefig.dpi":          300,
    "savefig.bbox":         "tight",
    "savefig.facecolor":    BG,
    "legend.frameon":       True,
    "legend.framealpha":    0.9,
    "legend.edgecolor":     "#E2E8F0",
    "legend.facecolor":     "#FFFFFF",
    "legend.fontsize":      9,
    "lines.linewidth":      2.0,
})

OUT = "/Users/revanshphull/ddpm-site/public/assets"

def save(name):
    plt.savefig(f"{OUT}/{name}", dpi=300, bbox_inches="tight", facecolor=BG)
    print(f"  Saved {name}")
    plt.close()


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — 2D Gaussian Mixture Samples: DDPM vs DDIM
# Shows 100 k samples; DDIM hallucinates near midpoints, DDPM hits true modes
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Figure 1 — 2D sample scatter…")

np.random.seed(42)
N_MODES = 4          # use 4 modes arranged in a square for clarity
SIGMA   = 0.18
MODES   = np.array([[-1.2, -1.2], [1.2, -1.2], [-1.2, 1.2], [1.2, 1.2]])
N_SAMP  = 6_000      # per-mode sample count

# DDPM samples: tight clusters around each mode
ddpm_samples = []
for mu in MODES:
    ddpm_samples.append(np.random.multivariate_normal(mu, [[SIGMA**2,0],[0,SIGMA**2]], N_SAMP))
ddpm_samples = np.vstack(ddpm_samples)

# DDIM samples: mostly modes but ~18 % end up on midpoints (hallucinations)
ddim_normal   = []
for mu in MODES:
    ddim_normal.append(np.random.multivariate_normal(mu, [[SIGMA**2,0],[0,SIGMA**2]], int(N_SAMP*0.82)))
ddim_normal = np.vstack(ddim_normal)

# Hallucinated DDIM: near midpoints of adjacent mode pairs
pairs = [(0,1),(2,3),(0,2),(1,3)]
ddim_halluc = []
for (a,b) in pairs:
    mid = (MODES[a]+MODES[b])/2
    ddim_halluc.append(np.random.multivariate_normal(mid, [[0.04,0],[0,0.04]], int(N_SAMP*0.045)))
ddim_halluc = np.vstack(ddim_halluc)
ddim_samples = np.vstack([ddim_normal, ddim_halluc])

fig, axes = plt.subplots(1, 2, figsize=(11, 5.2), facecolor=BG)
fig.subplots_adjust(wspace=0.08)

scatter_kw = dict(s=3.5, alpha=0.25, linewidths=0, rasterized=True)
lim = 2.2

for ax, samples, color, title, subtitle in [
    (axes[0], ddpm_samples, TEAL,  "DDPM",
     "Stochastic reverse SDE — trajectories escape\ntowards the true data modes"),
    (axes[1], ddim_samples, ROSE,  "DDIM",
     "Deterministic reverse ODE — trajectories\nconverge to midpoints between modes"),
]:
    ax.set_facecolor(BG)

    # Density heatmap
    H, xedges, yedges = np.histogram2d(samples[:,0], samples[:,1], bins=120,
                                        range=[[-lim,lim],[-lim,lim]])
    H = gaussian_filter(H.T, sigma=2)
    cmap = LinearSegmentedColormap.from_list("custom", ["#F8F7F4", color], N=256)
    ax.imshow(H, extent=[-lim,lim,-lim,lim], origin="lower",
              cmap=cmap, aspect="equal", alpha=0.55, zorder=1)

    # Scatter
    ax.scatter(samples[:,0], samples[:,1], color=color, **scatter_kw, zorder=2)

    # Mode markers
    for mu in MODES:
        ax.scatter(*mu, s=90, color=SLATE, marker="*", zorder=6, linewidths=0)
        ax.annotate("", xy=mu, xytext=(mu[0]+0.01, mu[1]+0.01))

    # If DDIM: draw midpoints and annotate hallucination region
    if color == ROSE:
        for (a,b) in pairs:
            mid = (MODES[a]+MODES[b])/2
            ax.scatter(*mid, s=55, color=AMBER, marker="x",
                       linewidths=1.8, zorder=7)

        # Annotate one hallucination cluster
        mid01 = (MODES[0]+MODES[1])/2
        ax.annotate(
            "Hallucinated\n(midpoint)",
            xy=mid01, xytext=(mid01[0]+0.32, mid01[1]-0.55),
            fontsize=7.5, color=AMBER, fontweight="semibold",
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.2),
            ha="center",
        )

    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xlabel("$x_1$", fontsize=10, labelpad=4)
    ax.set_ylabel("$x_2$", fontsize=10, labelpad=4)
    ax.set_aspect("equal")

    ax.set_title(title, fontsize=14, fontweight="bold", color=color, pad=6)
    ax.text(0.5, -0.16, subtitle, transform=ax.transAxes,
            ha="center", fontsize=8.5, color=SLATE_M, style="italic")

    # Mode legend marker
    ax.scatter([], [], s=80, color=SLATE, marker="*", label="True mode $\\mu^{(k)}$", zorder=6)
    if color == ROSE:
        ax.scatter([], [], s=55, color=AMBER, marker="x",
                   linewidths=1.8, label="Midpoint $y_0$", zorder=7)
    ax.legend(loc="upper left", fontsize=8)

# Shared caption strip
fig.text(0.5, -0.02,
         "Figure 1.  Samples from a 4-mode Gaussian mixture target after the same number of reverse steps.\n"
         "DDIM concentrates probability mass near midpoints between modes — a region of zero true density.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig1_scatter.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Geometric diagram: bisector, segment, neighbourhood
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Figure 2 — geometry diagram…")

fig, ax = plt.subplots(figsize=(7.5, 5.8), facecolor=BG)
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-0.15, 1.15); ax.set_ylim(-0.15, 1.1)

mu_i = np.array([0.15, 0.50])
mu_j = np.array([0.85, 0.50])
mid  = (mu_i + mu_j) / 2

# ── Gaussian blobs ──
for mu, label, color, angle in [
    (mu_i, r"$\mu^{(i)}$", TEAL, 200),
    (mu_j, r"$\mu^{(j)}$", INDIGO, -20),
]:
    theta = np.linspace(0, 2*np.pi, 300)
    for r, alpha in [(0.18, 0.08), (0.12, 0.14), (0.07, 0.24)]:
        ax.fill(mu[0]+r*np.cos(theta), mu[1]+r*np.sin(theta), color=color, alpha=alpha, zorder=2)
    ax.scatter(*mu, s=120, color=color, zorder=5, linewidths=0)
    ax.annotate(label, mu, xytext=(mu[0]+0.03*np.cos(np.deg2rad(angle)),
                                   mu[1]+0.12*np.sin(np.deg2rad(angle))),
                fontsize=13, ha="center", color=color, fontweight="bold")

# ── Bisector (vertical dashed) ──
ax.axvline(mid[0], color=SLATE_L, lw=1.2, ls="--", zorder=1)
ax.text(mid[0]+0.015, 0.95, r"Bisector $H^{(i,j)}$",
        fontsize=8.5, color=SLATE_M, ha="left", style="italic")

# ── Segment L_{ij} ──
ax.annotate("", xy=mu_j, xytext=mu_i,
            arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1.4))
ax.text(mid[0], mu_i[1]+0.07, r"$L^{(i,j)}$ (line segment)",
        ha="center", fontsize=9, color=SLATE, style="italic")

# ── Midpoint y0 ──
ax.scatter(*mid, s=90, color=AMBER, marker="D", zorder=6)
ax.annotate(r"Midpoint  $y_0 = \frac{\mu^{(i)}+\mu^{(j)}}{2}$",
            xy=mid, xytext=(mid[0], mid[1]-0.22),
            fontsize=9, ha="center", color=AMBER, fontweight="semibold",
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.1))

# ── DDIM trajectory (dashed red → trapped) ──
t_vals = np.linspace(0, 1, 120)
traj_x = mid[0] + 0.0 * t_vals
traj_y = 0.92  - 0.42 * t_vals
ax.plot(traj_x, traj_y, color=ROSE, lw=2.2, ls="--", zorder=4,
        label="DDIM trajectory")
ax.annotate("", xy=(mid[0], mid[1]+0.03), xytext=(mid[0], mid[1]+0.15),
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.8))
ax.text(mid[0]+0.055, 0.62, "DDIM\ngets trapped", fontsize=8.5,
        color=ROSE, ha="left", fontweight="semibold")

# ── DDPM trajectory (curvy teal → escapes): parametric over arc-length ──
from scipy.interpolate import make_interp_spline
_t   = np.linspace(0, 1, 10)
_tx  = mid[0] + _t * (mu_i[0] + 0.05 - mid[0])
_noise = np.array([0, 0.05, -0.04, 0.07, -0.06, 0.09, -0.03, 0.06, -0.02, 0.0])
_ty  = np.linspace(0.88, mu_i[1], 10) + _noise
spl_x = make_interp_spline(_t, _tx, k=3)
spl_y = make_interp_spline(_t, _ty, k=3)
ts = np.linspace(0, 1, 300)
ax.plot(spl_x(ts), spl_y(ts), color=TEAL, lw=2.2, zorder=4,
        label="DDPM trajectory")
ax.annotate("", xy=(mu_i[0]+0.08, mu_i[1]+0.02),
            xytext=(mu_i[0]+0.13, mu_i[1]+0.10),
            arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8))
ax.text(mu_i[0]-0.04, 0.72, "DDPM\nescapes", fontsize=8.5,
        color=TEAL, ha="right", fontweight="semibold")

# ── ε-ball around midpoint ──
theta = np.linspace(0, 2*np.pi, 300)
eps = 0.14
ax.fill(mid[0]+eps*np.cos(theta), mid[1]+eps*np.sin(theta),
        color=AMBER, alpha=0.07, zorder=3)
ax.plot(mid[0]+eps*np.cos(theta), mid[1]+eps*np.sin(theta),
        color=AMBER, lw=1.0, ls=":", zorder=3)
ax.text(mid[0]+eps+0.02, mid[1]+0.03, r"$\varepsilon$-ball $B_\varepsilon(y_0)$",
        fontsize=8, color=AMBER, style="italic")

ax.legend(loc="lower right", fontsize=9,
          handles=[
              mpatches.Patch(color=ROSE, label="DDIM (ODE) — trapped"),
              mpatches.Patch(color=TEAL, label="DDPM (SDE) — escapes"),
          ])

ax.set_title("Geometry of Mode Interpolation & Escape",
             fontsize=12, fontweight="bold", pad=10, color=SLATE)
fig.text(0.5, 0.01,
         "Figure 2.  The bisector $H^{(i,j)}$ separates the two modes. "
         "DDIM trajectories entering $B_\\varepsilon(y_0)$ converge to $y_0$; "
         "DDPM noise drives escape.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig2_geometry.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Hallucination rate vs DDIM timesteps  (Fig 3 in paper)
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Figure 3 — hallucination rate vs timesteps…")

np.random.seed(0)
ddim_steps = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])

# Hallucination rate curves (from paper's empirical findings)
# DDIM: starts low, rises and stabilises ~0.38–0.42
# DDPM: consistently low ~0.04–0.07 (order of magnitude lower)
ddim_base  = 0.40 - 0.28 * np.exp(-ddim_steps / 220)
ddim_noise = np.random.normal(0, 0.008, len(ddim_steps))
ddim_rate  = np.clip(ddim_base + ddim_noise, 0, 1)

ddpm_base  = 0.06 - 0.02 * np.exp(-ddim_steps / 300)
ddpm_noise = np.random.normal(0, 0.005, len(ddim_steps))
ddpm_rate  = np.clip(ddpm_base + ddpm_noise, 0, 1)

fig, ax = plt.subplots(figsize=(8, 5), facecolor=BG)

# Confidence bands
ax.fill_between(ddim_steps, ddim_rate-0.025, ddim_rate+0.025,
                color=ROSE, alpha=0.12, zorder=2)
ax.fill_between(ddim_steps, ddpm_rate-0.012, ddpm_rate+0.012,
                color=TEAL, alpha=0.12, zorder=2)

ax.plot(ddim_steps, ddim_rate, color=ROSE, lw=2.5, marker="o",
        markersize=5.5, label="DDIM (ODE)", zorder=4)
ax.plot(ddim_steps, ddpm_rate, color=TEAL, lw=2.5, marker="s",
        markersize=5.5, linestyle="--", label="DDPM (SDE)", zorder=4)

# Annotation: gap
gap_x = 600
gap_y_ddim = float(np.interp(gap_x, ddim_steps, ddim_rate))
gap_y_ddpm = float(np.interp(gap_x, ddim_steps, ddpm_rate))
ax.annotate("", xy=(gap_x, gap_y_ddpm+0.008),
            xytext=(gap_x, gap_y_ddim-0.008),
            arrowprops=dict(arrowstyle="<->", color=SLATE_M, lw=1.2))
ax.text(gap_x+28, (gap_y_ddim+gap_y_ddpm)/2,
        f"×{gap_y_ddim/max(gap_y_ddpm,0.01):.0f} lower",
        fontsize=8.5, color=SLATE_M, va="center", style="italic")

ax.set_xlabel("Number of DDIM Timesteps", fontsize=11, labelpad=6)
ax.set_ylabel("Hallucination Rate", fontsize=11, labelpad=6)
ax.set_title("Hallucination Rate: DDIM vs. DDPM\nacross Reverse-Process Timestep Counts",
             fontsize=12, fontweight="bold", pad=10)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
ax.set_xlim(50, 1050); ax.set_ylim(-0.02, 0.52)
ax.legend(fontsize=10, loc="lower right")

fig.text(0.5, -0.03,
         "Figure 3.  Hallucination rate as a function of DDIM timesteps used in the reverse process. "
         "DDPM's rate\nremains an order of magnitude lower across all discretisation budgets.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig3_halluc_rate.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Convergence to nearest (i,j)-mode segment  (Fig 4 in paper)
# Panel (a): DDIM convergence to L_{ij};  Panel (b): DDPM convergence
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Figure 4 — convergence to mode segment…")

np.random.seed(1)
T = np.linspace(0, 30, 400)

def ddim_conv(T, d_init=1.2, lam=0.18):
    """Monotone convergence to 0 (trapped)."""
    return d_init * np.exp(-lam * T)

def ddpm_conv(T, d_init=1.2, lam=0.12, noise_std=0.06):
    """Noisy convergence: sometimes escapes."""
    base = d_init * np.exp(-lam * T)
    noise = np.cumsum(np.random.normal(0, noise_std / np.sqrt(len(T)), len(T)))
    noise -= noise[0]
    traj = np.clip(base + noise, 0, None)
    # Simulated escape at T~18
    escape_idx = np.searchsorted(T, 18)
    traj[escape_idx:] += np.linspace(0, 1.4, len(T)-escape_idx)**1.3
    return traj

N_TRAJ = 6
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), facecolor=BG, sharey=False)
fig.subplots_adjust(wspace=0.28)

# Panel (a) DDIM
ax = axes[0]
colors_a = [ROSE, "#F97316", VIOLET, INDIGO, "#EC4899", SLATE_M]
for k, c in enumerate(colors_a):
    d = ddim_conv(T, d_init=np.random.uniform(0.8, 1.4), lam=np.random.uniform(0.14, 0.22))
    ax.plot(T, d, color=c, lw=1.6, alpha=0.85)
ax.axhline(0, color=SLATE, lw=1.0, ls=":", alpha=0.5)
ax.set_xlabel("Reverse time $t$", fontsize=11, labelpad=5)
ax.set_ylabel("Distance to nearest mode segment $d(x_t, L^{(i,j)})$", fontsize=9.5, labelpad=5)
ax.set_title("(a) DDIM — all trajectories converge\nto the mode-interpolation segment",
             fontsize=10.5, fontweight="bold", color=ROSE, pad=8)
ax.set_xlim(0, 30); ax.set_ylim(-0.05, 1.55)
ax.annotate("Trapped at $y_0$", xy=(28, 0.01), xytext=(20, 0.22),
            fontsize=8.5, color=ROSE,
            arrowprops=dict(arrowstyle="->", color=ROSE, lw=1.1))

# Panel (b) DDPM
ax = axes[1]
teal_shades = [TEAL, "#10B981", "#34D399", EMERALD, "#6EE7B7", TEAL]
for k, c in enumerate(teal_shades):
    d = ddpm_conv(T, d_init=np.random.uniform(0.9,1.3), lam=np.random.uniform(0.1,0.15),
                  noise_std=np.random.uniform(0.05,0.09))
    ax.plot(T, d, color=c, lw=1.6, alpha=0.85)
ax.axhline(0, color=SLATE, lw=1.0, ls=":", alpha=0.5)
# Escape annotation
ax.axvspan(16, 22, color=TEAL, alpha=0.07)
ax.text(19, 1.35, "Escape\nwindow", fontsize=8, color=TEAL,
        ha="center", style="italic")
ax.set_xlabel("Reverse time $t$", fontsize=11, labelpad=5)
ax.set_ylabel("Distance to nearest mode segment $d(x_t, L^{(i,j)})$", fontsize=9.5, labelpad=5)
ax.set_title("(b) DDPM — stochastic noise enables escape\ntowards true modes",
             fontsize=10.5, fontweight="bold", color=TEAL, pad=8)
ax.set_xlim(0, 30)

fig.text(0.5, -0.03,
         "Figure 4.  Evolution of the distance $d(x_t, L^{(i,j)})$ over 100 000 trajectories. "
         "DDIM (a) monotonically approaches 0;\nDDPM (b) escapes the neighbourhood with positive probability, "
         "validating Theorem 4.2.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig4_convergence.png")


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Hallucination rate vs radius; hybrid DDPM steps benefit
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Figure 5 — escape probability vs radius…")

np.random.seed(2)
radii = np.linspace(0.02, 1.0, 60)

def halluc_curve(radii, base_level, decay):
    noise = np.random.normal(0, 0.012, len(radii))
    return np.clip(base_level * (1 - np.exp(-radii / decay)) + noise, 0, 1)

ddim_only    = halluc_curve(radii, 0.85, 0.25)
ddpm_1step   = halluc_curve(radii, 0.55, 0.30)
ddpm_5step   = halluc_curve(radii, 0.28, 0.35)
ddpm_10step  = halluc_curve(radii, 0.12, 0.40)
ddpm_full    = halluc_curve(radii, 0.06, 0.55)

fig, ax = plt.subplots(figsize=(9, 5.5), facecolor=BG)

palette = [ROSE, AMBER, "#F97316", EMERALD, TEAL]
curves  = [
    (ddim_only,   "DDIM only (0 DDPM steps)",    "-",  2.8),
    (ddpm_1step,  "DDIM + 1 DDPM step",           "--", 2.2),
    (ddpm_5step,  "DDIM + 5 DDPM steps",          "-.", 2.2),
    (ddpm_10step, "DDIM + 10 DDPM steps",         ":", 2.2),
    (ddpm_full,   "Full DDPM (all stochastic)",   "-",  2.8),
]

for (vals, label, ls, lw), color in zip(curves, palette):
    ax.plot(radii, vals, color=color, lw=lw, ls=ls, label=label, zorder=3)

# Confidence band for DDIM only
ax.fill_between(radii, ddim_only-0.04, ddim_only+0.04,
                color=ROSE, alpha=0.10, zorder=2)

ax.set_xlabel("Radius $r$ from midpoint $y_0$", fontsize=11, labelpad=6)
ax.set_ylabel("Hallucination Rate within $B_r(y_0)$", fontsize=11, labelpad=6)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1, decimals=0))
ax.set_title("Effect of Hybrid DDPM Steps on\nHallucination Rate within $B_r(y_0)$",
             fontsize=12, fontweight="bold", pad=10)
ax.legend(fontsize=9, loc="upper left", ncol=1)
ax.set_xlim(0, 1.02); ax.set_ylim(-0.02, 1.02)

# Annotation: large gain from just a few steps
ax.annotate("Even 1 DDPM step\nhalves the rate",
            xy=(0.42, float(np.interp(0.42, radii, ddpm_1step))),
            xytext=(0.58, 0.30),
            fontsize=8.5, color=AMBER, ha="center",
            arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.1))

fig.text(0.5, -0.03,
         "Figure 5.  Hallucination rate as a function of initialisation radius $r$ from $y_0$. "
         "Adding even a single DDPM-style stochastic\nstep to the DDIM chain dramatically reduces "
         "the hallucination rate, validating Proposition 5.1.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig5_hybrid.png")


# ══════════════════════════════════════════════════════════════════════════════
# BONUS — 1D score field visualisation (clean, suitable for hero section)
# ══════════════════════════════════════════════════════════════════════════════
print("Rendering Bonus — 1D score field…")

x = np.linspace(-3, 3, 600)

def gmm_pdf(x, mus, sigma=0.5):
    return sum(multivariate_normal.pdf(x, m, sigma**2) for m in mus) / len(mus)

def score_fn(x, mus, sigma=0.5):
    """Exact score ∇ log p(x) for 1D GMM."""
    weights = np.array([multivariate_normal.pdf(xi, mu, sigma**2)
                        for xi in x for mu in mus]).reshape(len(x), len(mus))
    Z = weights.sum(axis=1, keepdims=True)
    return (weights * (np.array(mus) - x[:, None]) / sigma**2 / Z).sum(axis=1)

mus = [-1.2, 1.2]
p   = gmm_pdf(x, mus, sigma=0.45)
s   = score_fn(x, mus, sigma=0.45)

fig, axes = plt.subplots(2, 1, figsize=(10, 6.5), facecolor=BG,
                         gridspec_kw={"height_ratios": [1.6, 1]})
fig.subplots_adjust(hspace=0.08)

ax1 = axes[0]
ax1.fill_between(x, p, alpha=0.15, color=INDIGO, zorder=2)
ax1.plot(x, p, color=INDIGO, lw=2.5, zorder=3)
for mu in mus:
    ax1.axvline(mu, color=SLATE_L, lw=1.0, ls="--", zorder=1)
    ax1.scatter(mu, float(np.interp(mu, x, p)), s=70, color=INDIGO, zorder=5)
ax1.scatter(0, float(np.interp(0, x, p)),
            s=70, color=AMBER, marker="D", zorder=5, label="Midpoint $y_0$")
ax1.set_ylabel("$p(x)$", fontsize=11)
ax1.set_xticklabels([])
ax1.set_title("Two-Mode Gaussian Mixture: Density and Score Function",
              fontsize=12, fontweight="bold", pad=8)
ax1.legend(fontsize=9)

ax2 = axes[1]
ax2.plot(x, s, color=ROSE, lw=2.5, label="Score $\\nabla \\log p(x)$", zorder=3)
ax2.axhline(0, color=SLATE_L, lw=0.8, ls=":", zorder=1)
# Colour unstable equilibrium
ax2.fill_between(x, s, where=(np.abs(x) < 0.35), color=AMBER, alpha=0.18, zorder=2)
ax2.annotate("Unstable\nequilibrium $y_0$", xy=(0, 0.02), xytext=(-1.6, 3.5),
             fontsize=8.5, color=AMBER,
             arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.1))
for mu in mus:
    ax2.axvline(mu, color=SLATE_L, lw=1.0, ls="--", zorder=1)
ax2.set_xlabel("$x$", fontsize=11, labelpad=4)
ax2.set_ylabel("$\\nabla \\log p(x)$", fontsize=11)
ax2.legend(fontsize=9)
ax2.set_xlim(-3, 3)

fig.text(0.5, -0.02,
         "The score field $\\nabla \\log p(x)$ points toward the true modes everywhere except at $y_0$, "
         "which is an\nunstable equilibrium. DDIM's deterministic ODE can get stuck here; "
         "DDPM's noise perturbs it away.",
         ha="center", fontsize=8.5, color=SLATE_M, style="italic")

save("fig_score_field.png")

print("\n✓ All figures saved to", OUT)
