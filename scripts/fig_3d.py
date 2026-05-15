"""
3D probability-landscape figure for the DDPM vs DDIM paper site.
Renders a beautiful publication-quality 3D surface of a 2-mode Gaussian mixture,
with annotated DDIM (trapped) and DDPM (escape) trajectories.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D          # noqa: F401
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# ── Palette ──────────────────────────────────────────────────────────────────
BG     = "#F8F7F4"
SLATE  = "#1E293B"
SLATEM = "#475569"
SLATEL = "#94A3B8"
INDIGO = "#4F46E5"
ROSE   = "#F43F5E"
TEAL   = "#0D9488"
AMBER  = "#D97706"

OUT = "/Users/revanshphull/ddpm-site/public/assets"

# ── GMM definition ────────────────────────────────────────────────────────────
MU1 = np.array([-1.65,  0.0])
MU2 = np.array([ 1.65,  0.0])
SIG = 0.52

def gmm2d(x, y):
    p1 = np.exp(-0.5 * ((x - MU1[0])**2 + (y - MU1[1])**2) / SIG**2)
    p2 = np.exp(-0.5 * ((x - MU2[0])**2 + (y - MU2[1])**2) / SIG**2)
    return (p1 + p2) / (2 * 2 * np.pi * SIG**2)

def score2d(x, y):
    w1 = np.exp(-0.5 * ((x - MU1[0])**2 + (y - MU1[1])**2) / SIG**2)
    w2 = np.exp(-0.5 * ((x - MU2[0])**2 + (y - MU2[1])**2) / SIG**2)
    Z  = w1 + w2 + 1e-12
    sx = (w1 * (MU1[0] - x) + w2 * (MU2[0] - x)) / (SIG**2 * Z)
    sy = (w1 * (MU1[1] - y) + w2 * (MU2[1] - y)) / (SIG**2 * Z)
    return sx, sy

# ── Custom colourmap: deep indigo → teal → amber (peak) ──────────────────────
CMAP_COLORS = [
    (0.00, "#1E1B4B"),   # deep indigo-950 (valley / saddle)
    (0.18, "#3730A3"),   # indigo-700
    (0.40, "#4F46E5"),   # indigo-600
    (0.62, "#0D9488"),   # teal-600
    (0.80, "#F59E0B"),   # amber-500
    (1.00, "#FDE68A"),   # amber-200 (peak highlight)
]
cmap = LinearSegmentedColormap.from_list(
    "gmm", [(v, c) for v, c in CMAP_COLORS]
)

# ── Grid ──────────────────────────────────────────────────────────────────────
N = 120
xs = np.linspace(-3.2, 3.2, N)
ys = np.linspace(-2.4, 2.4, N)
X, Y = np.meshgrid(xs, ys)
Z    = gmm2d(X, Y)

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 9), facecolor=BG)
ax  = fig.add_subplot(111, projection="3d", facecolor=BG)

# Surface
surf = ax.plot_surface(
    X, Y, Z,
    cmap=cmap,
    linewidth=0,
    antialiased=True,
    alpha=0.92,
    rcount=90,
    ccount=90,
)

# Contour shadow on the floor (z = 0)
cset = ax.contourf(X, Y, Z, zdir="z", offset=0, cmap=cmap, alpha=0.22, levels=14)

# ── Mode peak markers ─────────────────────────────────────────────────────────
z_peak = gmm2d(*MU1)
for mu in [MU1, MU2]:
    zp = gmm2d(*mu)
    ax.scatter(*mu, zp, s=120, c=AMBER, marker="*", zorder=10, depthshade=False)
    ax.plot([mu[0], mu[0]], [mu[1], mu[1]], [0, zp],
            color=AMBER, lw=1.0, ls="--", alpha=0.5)

# Midpoint / saddle marker
z_saddle = gmm2d(0, 0)
ax.scatter(0, 0, z_saddle, s=90, c=ROSE, marker="D", zorder=10, depthshade=False)
ax.plot([0, 0], [0, 0], [0, z_saddle], color=ROSE, lw=1.0, ls="--", alpha=0.5)

# ── Simulate DDIM trajectory (x-axis only, y=0) ───────────────────────────────
def score1d_x(x, y=0.0):
    sx, _ = score2d(x, y)
    return sx

def ddim_step(x, y, dt=0.055, sig=0.6):
    sx, sy = score2d(x, y)
    return x + dt * sig * sx, y + dt * sig * sy

def ddpm_step(x, y, dt=0.055, sig=0.6, rng=None):
    rng = rng or np.random.default_rng()
    sx, sy = score2d(x, y)
    nx = x + dt * sig * sx + np.sqrt(2 * dt * sig) * rng.normal() * 0.55
    ny = y + dt * sig * sy + np.sqrt(2 * dt * sig) * rng.normal() * 0.25
    return nx, ny

rng = np.random.default_rng(seed=7)

# DDIM
dx_traj, dy_traj = [0.22], [0.0]
cx, cy = 0.22, 0.0
for _ in range(60):
    cx, cy = ddim_step(cx, cy)
    cx = np.clip(cx, -3.1, 3.1); cy = np.clip(cy, -2.3, 2.3)
    dx_traj.append(cx); dy_traj.append(cy)
dz_traj = [gmm2d(x, y) + 0.003 for x, y in zip(dx_traj, dy_traj)]

# DDPM
px_traj, py_traj = [0.22], [0.0]
cx, cy = 0.22, 0.0
for _ in range(60):
    cx, cy = ddpm_step(cx, cy, rng=rng)
    cx = np.clip(cx, -3.1, 3.1); cy = np.clip(cy, -2.3, 2.3)
    px_traj.append(cx); py_traj.append(cy)
pz_traj = [gmm2d(x, y) + 0.003 for x, y in zip(px_traj, py_traj)]

# Draw trajectories
ax.plot(dx_traj, dy_traj, dz_traj, color=ROSE, lw=2.8, zorder=6,
        label="DDIM (ODE) — trapped at $y_0$", solid_capstyle="round")
ax.plot(px_traj, py_traj, pz_traj, color=TEAL, lw=2.8, zorder=6,
        label="DDPM (SDE) — escapes to mode $\\mu$", solid_capstyle="round")

# Start dot
ax.scatter(0.22, 0.0, gmm2d(0.22, 0.0) + 0.005, s=80, c="white", zorder=8,
           edgecolors=SLATEL, linewidths=1.2, depthshade=False)

# End dots
ax.scatter(dx_traj[-1], dy_traj[-1], dz_traj[-1] + 0.004,
           s=100, c=ROSE, zorder=8, depthshade=False)
ax.scatter(px_traj[-1], py_traj[-1], pz_traj[-1] + 0.004,
           s=100, c=TEAL, zorder=8, depthshade=False)

# ── Styling ───────────────────────────────────────────────────────────────────
ax.set_xlabel("$x_1$",    fontsize=12, color=SLATEM, labelpad=8)
ax.set_ylabel("$x_2$",    fontsize=12, color=SLATEM, labelpad=8)
ax.set_zlabel("$p(x_1, x_2)$", fontsize=11, color=SLATEM, labelpad=8)

ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor("#E2E8F0")
ax.yaxis.pane.set_edgecolor("#E2E8F0")
ax.zaxis.pane.set_edgecolor("#E2E8F0")
ax.grid(True, color="#E2E8F0", alpha=0.5, linewidth=0.5)
ax.tick_params(colors=SLATEL, labelsize=8)

ax.view_init(elev=32, azim=-52)
ax.set_zlim(0, Z.max() * 1.05)
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-2.4, 2.4)

# Annotation text
ax.text2D(0.50, 0.97,
          "3D Probability Landscape — $p(x_1, x_2)$ of a Two-Mode Gaussian Mixture",
          transform=ax.transAxes, ha="center", va="top",
          fontsize=13, fontweight="bold", color=SLATE)

ax.text2D(0.50, 0.915,
          "The saddle at $y_0 = (0,0)$ is an unstable equilibrium. "
          "DDIM (rose) converges here; DDPM (teal) escapes to a true mode.",
          transform=ax.transAxes, ha="center", va="top",
          fontsize=9.5, color=SLATEM, style="italic")

# Colourbar
cbar = fig.colorbar(surf, ax=ax, shrink=0.42, pad=0.08, aspect=18,
                    location="right")
cbar.set_label("$p(x_1, x_2)$", fontsize=10, color=SLATEM)
cbar.ax.tick_params(colors=SLATEL, labelsize=8)
cbar.outline.set_edgecolor("#E2E8F0")

# Mode / saddle legend entries
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color=ROSE, lw=2.5, label="DDIM (ODE) — trapped at $y_0$"),
    Line2D([0], [0], color=TEAL, lw=2.5, label="DDPM (SDE) — escapes to mode"),
    Line2D([0], [0], marker="*", color="w", markerfacecolor=AMBER,
           markersize=10, lw=0, label="True modes $\\mu^{(1)}, \\mu^{(2)}$"),
    Line2D([0], [0], marker="D", color="w", markerfacecolor=ROSE,
           markersize=8,  lw=0, label="Midpoint $y_0$  (hallucination locus)"),
]
ax.legend(handles=legend_elements, loc="upper left", fontsize=9,
          framealpha=0.9, edgecolor="#E2E8F0", facecolor="white")

fig.text(0.50, 0.01,
         "Figure.  The DDIM reverse ODE follows the score field deterministically, "
         "converging to $y_0$ — a point of zero true probability mass.\n"
         "DDPM's Brownian noise breaks the symmetry and drives the trajectory "
         "toward one of the two true modes, avoiding hallucination.",
         ha="center", fontsize=9, color=SLATEM, style="italic")

plt.savefig(f"{OUT}/fig_3d_landscape.png", dpi=300, bbox_inches="tight", facecolor=BG)
print("Saved fig_3d_landscape.png")
plt.close()
