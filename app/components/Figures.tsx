"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef, useState } from "react";
import Image from "next/image";

const FIGURES = [
  // {
  //   id: "fig3d",
  //   src: "/assets/fig_3d_landscape.png",
  //   title: "3D Probability Landscape",
  //   caption:
  //     "3D surface of p(x₁, x₂) for a two-mode Gaussian mixture. The deep indigo valley between the two amber peaks is the hallucination locus. DDIM (rose) slides into the saddle at y₀; DDPM (teal) climbs toward a true mode. Colour encodes density: indigo = low, amber = high.",
  //   width: 1400,
  //   height: 900,
  //   badge: "3D Visualisation",
  //   badgeColor: "violet",
  // },
  {
    id: "fig3",
    src: "/assets/paper_fig3_halluc.png",
    title: "Hallucination Rate vs. Discretization",
    caption:
      "We find that DDIM hallucinates more than DDPM across discretization levels, invalidating that DDIM discretization explains its higher hallucination rate.",
    width: 1284,
    height: 759,
  },
  {
    id: "fig4",
    src: "/assets/paper_fig4_convergence.png",
    title: "Convergence to Nearby Line Segment",
    caption:
      "After Asm. 4.1 holds, trajectories converge to the nearby line segment (Thm. 4.2).",
    width: 2470,
    height: 854,
  },
  {
    id: "fig5",
    src: "/assets/paper_fig5_radius.png",
    title: "DDIM Trapping vs. DDPM Escape Near Midpoint",
    caption:
      "We find for trajectories started near the midpoint after Asm. 4.1 and 4.4 hold, DDIM trajectories get stuck while DDPM trajectories escape. Furthermore, adding DDPM timesteps to DDIM samplers helps escape the midpoint neighborhood, suggesting new approaches for hybrid diffusion samplers.",
    width: 999,
    height: 654,
  },
  // {
  //   id: "figs",
  //   src: "/assets/fig_score_field.png",
  //   title: "Score Field — Density & ∇ log p(x)",
  //   caption:
  //     "The score function ∇ log p(x) for a two-mode Gaussian mixture. The midpoint y₀ is an unstable equilibrium: the score is zero there, so the DDIM ODE has no gradient to drive it toward a true mode. DDPM's Brownian noise perturbs trajectories away from this saddle point.",
  //   width: 1500,
  //   height: 975,
  //   badge: "Intuition",
  //   badgeColor: "violet",
  // },
];

function FigureCard({ fig, index, inView }: {
  fig: typeof FIGURES[number];
  index: number;
  inView: boolean;
}) {
  const [enlarged, setEnlarged] = useState(false);

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
          <span className="text-[13px] font-semibold text-slate-800">{fig.title}</span>
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
              Experiments
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Empirical Results
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            Click any figure to enlarge. These experiments demonstrate that discretization is not responsible for DDIM&apos;s higher hallucination rate and validate our theoretical results.
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
