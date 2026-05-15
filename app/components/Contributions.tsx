"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";

const CONTRIBUTIONS = [
  {
    number: "01",
    title: "How DDIM Hallucinates",
    tag: "Theoretical Result #1",
    tagColor: "rose",
    body: `We rigorously study the source of DDIM hallucinations as observed in an N-mode Gaussian mixture, demonstrating that after a critical time, DDIM trajectories converge to the nearest line segment joining two modes and then can become stuck near the midpoint, thus ending up in regions of low probability mass. These are "mode interpolation hallucinations" (Aithal et al., 2024).`,
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
        <path strokeLinecap="round" strokeLinejoin="round"
          d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
      </svg>
    ),
  },
  {
    number: "02",
    title: "The DDPM Escape Mechanism",
    tag: "Theoretical Result #2",
    tagColor: "teal",
    body: "We leverage this to provide a theoretical justification for why DDIM hallucinates more than DDPM: the noise of DDPM can help it become unstuck from this hallucination region around the midpoint.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
        <path strokeLinecap="round" strokeLinejoin="round"
          d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
  },
  {
    number: "03",
    title: "Experiments",
    tag: "Empirical Validation",
    tagColor: "indigo",
    body: "Empirically, we invalidate that the DDIM hallucination rate gap can be explained by step skipping and demonstrate that adding a few DDPM steps after DDIM converges near the midpoint neighborhood can help the trajectory escape, lowering hallucination rate.",
    icon: (
      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.6}>
        <path strokeLinecap="round" strokeLinejoin="round"
          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    ),
  },
];

const TAG_COLORS: Record<string, { bg: string; border: string; text: string; icon: string }> = {
  rose: {
    bg: "bg-rose-50",
    border: "border-rose-200",
    text: "text-rose-700",
    icon: "text-rose-500 bg-rose-100",
  },
  teal: {
    bg: "bg-teal-50",
    border: "border-teal-200",
    text: "text-teal-700",
    icon: "text-teal-500 bg-teal-100",
  },
  indigo: {
    bg: "bg-indigo-50",
    border: "border-indigo-200",
    text: "text-indigo-700",
    icon: "text-indigo-500 bg-indigo-100",
  },
};

export default function Contributions() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });

  return (
    <section id="contributions" className="py-24 px-6 bg-slate-50/60">
      <hr className="section-divider mb-0" />
      <div className="max-w-4xl mx-auto pt-24" ref={ref}>
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
              Key Contributions
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            What We Demonstrate
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            We characterize where and when mode interpolation hallucinations arise in DDIM, describe why DDPM hallucinates less than DDIM, and validate our results empirically.
          </p>
        </motion.div>

        {/* Cards grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {CONTRIBUTIONS.map((c, i) => {
            const colors = TAG_COLORS[c.tagColor];
            return (
              <motion.div
                key={c.number}
                initial={{ opacity: 0, y: 24 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{
                  duration: 0.6,
                  ease: [0.16, 1, 0.3, 1] as const,
                  delay: 0.1 + i * 0.1,
                }}
                className="relative bg-white rounded-2xl border border-slate-200 p-6 flex flex-col gap-5 shadow-[0_2px_12px_0_rgb(0,0,0,0.05)] hover:shadow-[0_6px_24px_0_rgb(0,0,0,0.09)] hover:-translate-y-0.5 transition-all duration-300"
              >
                {/* Number + icon row */}
                <div className="flex items-start justify-between">
                  <span className="text-[11px] font-bold text-slate-300 tracking-widest">
                    {c.number}
                  </span>
                  <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${colors.icon}`}>
                    {c.icon}
                  </div>
                </div>

                {/* Tag */}
                <div>
                  <span
                    className={`inline-block text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${colors.bg} ${colors.border} ${colors.text}`}
                  >
                    {c.tag}
                  </span>
                </div>

                {/* Title */}
                <h3 className="text-[15px] font-bold text-slate-800 leading-snug">
                  {c.title}
                </h3>

                {/* Body */}
                <p className="text-[13.5px] text-slate-500 leading-relaxed flex-1">
                  {c.body}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
