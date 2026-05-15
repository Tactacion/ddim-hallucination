"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef, useState } from "react";
import Image from "next/image";

const FIGURES = [
  {
    id: "fig3d",
    src: "/assets/fig_3d_landscape.png",
    title: "3D Probability Landscape",
    caption:
      "3D surface of p(x₁, x₂) for a two-mode Gaussian mixture. The deep indigo valley between the two amber peaks is the hallucination locus. DDIM (rose) slides into the saddle at y₀; DDPM (teal) climbs toward a true mode. Colour encodes density: indigo = low, amber = high.",
    width: 1400,
    height: 900,
    badge: "3D Visualisation",
    badgeColor: "violet",
  },
  {
    id: "fig1",
    src: "/assets/paper_fig1_samples.png",
    title: "Figure 1 — Sample Comparison (25-Mode GMM)",
    caption:
      "In 100,000 generated samples for a 25-mode Gaussian mixture target, DDPM (left) hallucinates significantly less than DDIM (right). Towards the beginning of the reverse process the trajectory selects a line segment to converge to — converging either to a true mode or to the midpoint neighbourhood where DDIM gets stuck.",
    width: 2470,
    height: 859,
    badge: "Empirical",
    badgeColor: "rose",
  },
  {
    id: "fig3",
    src: "/assets/paper_fig3_halluc.png",
    title: "Figure 3 — Hallucination Rate vs. Timesteps",
    caption:
      "Hallucination rate for varying number of DDIM steps used in the reverse process. The number of DDIM interpolated samples is consistently ~10× larger than DDPM across all discretisation budgets (200–1,000 steps), invalidating the hypothesis that finer discretisation resolves DDIM's mode-interpolation pathology.",
    width: 1284,
    height: 759,
    badge: "Empirical",
    badgeColor: "rose",
  },
  {
    id: "fig4",
    src: "/assets/paper_fig4_convergence.png",
    title: "Figure 4 — Convergence to Mode Segment",
    caption:
      "Convergence rate to the nearest i,j-mode segment across 100,000 trajectories. DDIM (a) converges monotonically: after τ₁ the dynamics fix to the line segment, then after τ₂ only the parallel component remains relevant. DDPM (b) undergoes a similar contraction but Brownian noise preserves finite escape probability, consistent with Theorem 4.2.",
    width: 2470,
    height: 854,
    badge: "Theory + Empirical",
    badgeColor: "teal",
  },
  {
    id: "fig5",
    src: "/assets/paper_fig5_radius.png",
    title: "Figure 5 — Hybrid DDPM Mitigation",
    caption:
      "Hallucination rate as a function of initialisation radius r from the midpoint y₀. Each curve adds a different number of DDPM-style stochastic steps to the DDIM chain. Even 2 DDPM steps significantly reduce hallucination; 8 steps virtually eliminate it — providing a practical, low-cost mitigation strategy directly motivated by the theory.",
    width: 999,
    height: 654,
    badge: "Practical",
    badgeColor: "emerald",
  },
  {
    id: "figs",
    src: "/assets/fig_score_field.png",
    title: "Score Field — Density & ∇ log p(x)",
    caption:
      "The score function ∇ log p(x) for a two-mode Gaussian mixture. The midpoint y₀ is an unstable equilibrium: the score is zero there, so the DDIM ODE has no gradient to drive it toward a true mode. DDPM's Brownian noise perturbs trajectories away from this saddle point.",
    width: 1500,
    height: 975,
    badge: "Intuition",
    badgeColor: "violet",
  },
];

const BADGE: Record<string, { bg: string; border: string; text: string }> = {
  rose:    { bg: "bg-rose-50",    border: "border-rose-200",    text: "text-rose-700"    },
  indigo:  { bg: "bg-indigo-50",  border: "border-indigo-200",  text: "text-indigo-700"  },
  teal:    { bg: "bg-teal-50",    border: "border-teal-200",    text: "text-teal-700"    },
  emerald: { bg: "bg-emerald-50", border: "border-emerald-200", text: "text-emerald-700" },
  violet:  { bg: "bg-violet-50",  border: "border-violet-200",  text: "text-violet-700"  },
};

function FigureCard({ fig, index, inView }: {
  fig: typeof FIGURES[number];
  index: number;
  inView: boolean;
}) {
  const [enlarged, setEnlarged] = useState(false);
  const badge = BADGE[fig.badgeColor];

  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 28 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.08 * index }}
        className="flex flex-col gap-4"
      >
        {/* Image card */}
        <button
          onClick={() => setEnlarged(true)}
          className="group relative rounded-xl overflow-hidden border border-slate-200 bg-white shadow-[0_2px_12px_0_rgb(0,0,0,0.05)] hover:shadow-[0_8px_28px_0_rgb(0,0,0,0.10)] hover:-translate-y-0.5 transition-all duration-300 text-left w-full"
          aria-label={`Enlarge ${fig.title}`}
        >
          <div className="relative w-full" style={{ aspectRatio: `${fig.width}/${fig.height}` }}>
            <Image
              src={fig.src}
              alt={fig.title}
              fill
              className="object-contain"
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          </div>
          {/* Hover overlay */}
          <div className="absolute inset-0 bg-slate-900/0 group-hover:bg-slate-900/04 transition-colors duration-300 flex items-center justify-center">
            <span className="opacity-0 group-hover:opacity-100 transition-opacity duration-200 bg-white/90 text-slate-700 text-[12px] font-medium px-3 py-1.5 rounded-full border border-slate-200 shadow-sm">
              Click to enlarge
            </span>
          </div>
        </button>

        {/* Caption */}
        <div className="flex flex-col gap-2 px-1">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${badge.bg} ${badge.border} ${badge.text}`}>
              {fig.badge}
            </span>
            <span className="text-[13px] font-semibold text-slate-800">{fig.title}</span>
          </div>
          <p className="font-serif text-[13.5px] leading-relaxed text-slate-600 italic">
            {fig.caption}
          </p>
        </div>
      </motion.div>

      {/* Lightbox */}
      {enlarged && (
        <div
          className="fixed inset-0 z-[100] bg-slate-900/80 backdrop-blur-sm flex items-center justify-center p-6"
          onClick={() => setEnlarged(false)}
        >
          <div className="relative max-w-5xl w-full max-h-[90vh] rounded-2xl overflow-hidden shadow-2xl"
            onClick={e => e.stopPropagation()}
          >
            <div className="relative w-full bg-[#F8F7F4]" style={{ aspectRatio: `${fig.width}/${fig.height}` }}>
              <Image src={fig.src} alt={fig.title} fill className="object-contain" sizes="90vw" />
            </div>
            <div className="bg-white px-5 py-3 flex items-center justify-between">
              <span className="text-[13px] font-semibold text-slate-700">{fig.title}</span>
              <button
                onClick={() => setEnlarged(false)}
                className="text-[12px] text-slate-500 hover:text-slate-800 transition-colors"
              >
                Close ✕
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function Figures() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });

  return (
    <section id="figures" className="py-24 px-6" ref={ref}>
      <hr className="section-divider mb-24" />
      <div className="max-w-4xl mx-auto">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] as const }}
          className="flex flex-col gap-3 mb-14"
        >
          <div className="flex items-center gap-3">
            <div className="w-6 h-px bg-indigo-400" />
            <span className="text-xs font-semibold text-indigo-500 uppercase tracking-widest">
              Results & Figures
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Theoretical and Empirical Evidence
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            Click any figure to enlarge. Figures 1–5 are reproduced directly from the paper.
            3D visualisations and the score-field plot are companion renderings.
          </p>
        </motion.div>

        {/* 2-column figure grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-10">
          {FIGURES.map((fig, i) => (
            <FigureCard key={fig.id} fig={fig} index={i} inView={inView} />
          ))}
        </div>
      </div>
    </section>
  );
}
