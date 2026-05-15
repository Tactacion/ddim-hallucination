"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";
import Image from "next/image";

const THEOREM_CARDS = [
  {
    label: "Theorem 4.2",
    title: "DDIM Trapping Condition",
    body: "For an N-component Gaussian mixture, there exists a critical time τ★ such that for all t < τ★, any DDIM trajectory that enters an ε-ball around the midpoint y₀ = (μᵢ + μⱼ)/2 converges to y₀ rather than to either mode — independently of the number of reverse steps employed.",
    color: "rose",
  },
  {
    label: "Proposition 5.1",
    title: "DDPM Escape Probability",
    body: "Under the same Gaussian mixture, the DDPM reverse SDE has strictly positive probability of escaping the midpoint neighbourhood B_ε(y₀) at each discrete step. The escape probability is lower-bounded by a term that grows with the noise level σₜ, explaining the empirically observed order-of-magnitude reduction in hallucination rate.",
    color: "teal",
  },
];

export default function Theory() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="theory" className="py-24 px-6" ref={ref}>
      <hr className="section-divider mb-24" />
      <div className="max-w-4xl mx-auto">

        {/* ── Section header ─────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] as const }}
          className="flex flex-col gap-3 mb-14"
        >
          <div className="flex items-center gap-3">
            <div className="w-6 h-px bg-indigo-400" />
            <span className="text-xs font-semibold text-indigo-500 uppercase tracking-widest">
              Theory
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Reverse Dynamics in a Gaussian Mixture
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            We study a well-separated N-component Gaussian mixture as a canonical theoretical
            testbed. The density and score field below expose exactly why deterministic reverse
            dynamics can become trapped, and why stochasticity provides the escape.
          </p>
        </motion.div>

        {/* ── Score field figure (full width) ────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.08 }}
          className="mb-10"
        >
          <div className="rounded-2xl overflow-hidden border border-slate-200 bg-white shadow-[0_4px_20px_0_rgb(0,0,0,0.07)]">
            <div className="relative w-full" style={{ aspectRatio: "1500/975" }}>
              <Image
                src="/assets/fig_score_field.png"
                alt="Density p(x) and score function ∇ log p(x) for a two-mode Gaussian mixture"
                fill
                className="object-contain"
                sizes="(max-width: 768px) 100vw, 896px"
                priority
              />
            </div>
            <div className="bg-slate-50 border-t border-slate-100 px-5 py-3 flex items-center justify-between">
              <span className="text-[12px] text-slate-500">
                <strong className="text-slate-700">Figure.</strong>{" "}
                Density p(x) and score ∇ log p(x) for a two-mode Gaussian mixture.
                The midpoint y₀ is an{" "}
                <span className="text-amber-600 font-medium">unstable equilibrium</span> — the
                score is zero there, providing no gradient to push a deterministic trajectory
                toward a true mode.
              </span>
            </div>
          </div>
        </motion.div>

        {/* ── Side-by-side geometry + 3D landscape ───────────────────── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-10">
          {/* Geometry figure */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.14 }}
          >
            <div className="rounded-2xl overflow-hidden border border-slate-200 bg-white shadow-[0_4px_20px_0_rgb(0,0,0,0.07)] h-full flex flex-col">
              <div className="relative w-full flex-1" style={{ aspectRatio: "1125/870" }}>
                <Image
                  src="/assets/fig2_geometry.png"
                  alt="Geometry of mode interpolation: bisector, segment, escape and trap trajectories"
                  fill
                  className="object-contain"
                  sizes="(max-width: 640px) 100vw, 448px"
                />
              </div>
              <div className="bg-slate-50 border-t border-slate-100 px-4 py-2.5">
                <p className="text-[12px] text-slate-500">
                  <strong className="text-slate-700">Figure 2.</strong>{" "}
                  Bisector H(i,j), segment L(i,j), and the ε-ball around y₀.
                  DDIM (rose, dashed) converges; DDPM (teal, solid) escapes.
                </p>
              </div>
            </div>
          </motion.div>

          {/* 3D landscape figure */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.20 }}
          >
            <div className="rounded-2xl overflow-hidden border border-slate-200 bg-white shadow-[0_4px_20px_0_rgb(0,0,0,0.07)] h-full flex flex-col">
              <div className="relative w-full flex-1" style={{ aspectRatio: "14/9" }}>
                <Image
                  src="/assets/fig_3d_landscape.png"
                  alt="3D probability landscape p(x₁,x₂) with DDIM and DDPM trajectories"
                  fill
                  className="object-contain"
                  sizes="(max-width: 640px) 100vw, 448px"
                />
              </div>
              <div className="bg-slate-50 border-t border-slate-100 px-4 py-2.5">
                <p className="text-[12px] text-slate-500">
                  <strong className="text-slate-700">Figure.</strong>{" "}
                  3D probability surface p(x₁, x₂). The saddle at y₀ traps
                  DDIM; DDPM noise drives escape toward a true peak.
                </p>
              </div>
            </div>
          </motion.div>
        </div>

        {/* ── Theorem cards ───────────────────────────────────────────── */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
          {THEOREM_CARDS.map((t, i) => {
            const isRose = t.color === "rose";
            return (
              <motion.div
                key={t.label}
                initial={{ opacity: 0, y: 20 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{
                  duration: 0.6,
                  ease: [0.16, 1, 0.3, 1] as const,
                  delay: 0.28 + i * 0.1,
                }}
                className="bg-white rounded-2xl border border-slate-200 p-6 flex flex-col gap-4 shadow-[0_2px_12px_0_rgb(0,0,0,0.05)]"
              >
                <span
                  className={`self-start text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${
                    isRose
                      ? "bg-rose-50 border-rose-200 text-rose-700"
                      : "bg-teal-50 border-teal-200 text-teal-700"
                  }`}
                >
                  {t.label}
                </span>
                <h3 className="text-[15px] font-bold text-slate-800 leading-snug">
                  {t.title}
                </h3>
                <p className="font-serif text-[14px] leading-[1.8] text-slate-600 italic">
                  {t.body}
                </p>
              </motion.div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
