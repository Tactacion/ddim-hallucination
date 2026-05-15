"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";
import Image from "next/image";

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
            We study an N-component Gaussian mixture as a canonical theoretical testbed.
            The score field below reveals why deterministic reverse dynamics can become
            trapped near the midpoint between two modes — and why stochasticity
            provides the escape.
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
            <div className="bg-slate-50 border-t border-slate-100 px-5 py-3">
              <span className="text-[12px] text-slate-500">
                <strong className="text-slate-700">Figure.</strong>{" "}
                Density p(x) and score ∇ log p(x) for a two-mode Gaussian mixture.
                Near the midpoint y₀ the repulsive force on a deterministic trajectory
                is very weak, making escape unlikely — while DDPM&apos;s stochastic
                noise provides a nonzero probability of breaking free toward a true mode.
              </span>
            </div>
          </div>
        </motion.div>

        {/* ── 3D landscape ───────────────────────────────────────────── */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.14 }}
        >
          <div className="rounded-2xl overflow-hidden border border-slate-200 bg-white shadow-[0_4px_20px_0_rgb(0,0,0,0.07)]">
            <div className="relative w-full" style={{ aspectRatio: "14/9" }}>
              <Image
                src="/assets/fig_3d_landscape.png"
                alt="3D probability landscape p(x₁,x₂) illustrating the saddle between two modes"
                fill
                className="object-contain"
                sizes="(max-width: 768px) 100vw, 896px"
              />
            </div>
            <div className="bg-slate-50 border-t border-slate-100 px-5 py-3">
              <span className="text-[12px] text-slate-500">
                <strong className="text-slate-700">Figure.</strong>{" "}
                3D probability surface p(x₁, x₂) for a two-mode GMM. The saddle at
                y₀ sits in the low-density valley between the two peaks; a deterministic
                trajectory near it experiences very weak drift away, while Brownian noise
                provides the perturbation needed for escape.
              </span>
            </div>
          </div>
        </motion.div>

      </div>
    </section>
  );
}
