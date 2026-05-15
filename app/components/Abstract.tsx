"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";

const ABSTRACT = `We theoretically study the hallucination phenomena in two canonical diffusion samplers: the stochastic Denoising Diffusion Probabilistic Model (DDPM) and the deterministic Denoising Diffusion Implicit Model (DDIM). We analyze the reverse ODE (DDIM) and SDE (DDPM) for a Gaussian mixture target, proving that after a critical time, (a) DDIM can become stuck on the segment connecting the two nearest modes and (b) DDPM stochasticity helps it become unstuck from this region, thus avoiding hallucination. Our empirical validation verifies that DDPM has a significantly lower hallucination rate than DDIM when this region is entered. Building on our observations, we exhibit how using additional stochastic steps can help DDIM avoid hallucinations and offer new insights on how to design improved samplers.`;

const KEYWORDS = [
  "Diffusion Models",
  "DDPM",
  "DDIM",
  "Hallucination",
  "Reverse SDE/ODE",
  "Gaussian Mixture",
  "Sampler Design",
];

export default function Abstract() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="abstract" className="py-24 px-6">
      <hr className="section-divider mb-24" />
      <div className="max-w-4xl mx-auto" ref={ref}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] as const }}
          className="flex flex-col gap-8"
        >
          {/* Section label */}
          <div className="flex items-center gap-3">
            <div className="w-6 h-px bg-indigo-400" />
            <span className="text-xs font-semibold text-indigo-500 uppercase tracking-widest">
              Abstract
            </span>
          </div>

          {/* Abstract text */}
          <div className="relative">
            {/* Decorative quote mark */}
            <div
              className="absolute -top-4 -left-3 text-8xl text-indigo-100 font-serif leading-none select-none pointer-events-none"
              aria-hidden
            >
              "
            </div>
            <p className="font-serif text-[1.0625rem] leading-[1.85] text-slate-700 relative z-10 pl-1">
              {ABSTRACT}
            </p>
          </div>

          {/* Keyword pills */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={inView ? { opacity: 1 } : {}}
            transition={{ duration: 0.5, delay: 0.25 }}
            className="flex flex-wrap gap-2 pt-2"
          >
            {KEYWORDS.map((kw) => (
              <span
                key={kw}
                className="text-[12px] font-medium text-slate-600 bg-slate-100 border border-slate-200 px-3 py-1 rounded-full"
              >
                {kw}
              </span>
            ))}
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}
