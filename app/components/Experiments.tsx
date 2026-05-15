"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef } from "react";
import Image from "next/image";

const EXPERIMENTS = [
  {
    id: "mode-interp",
    src: "/assets/mode_interpolation.gif",
    title: "Mode Interpolation in Action",
    caption:
      "DDIM denoising on a 25-mode Gaussian grid: the left panel traces the live reverse trajectory; the right panel accumulates the final sample distribution. The legend reports ~9.4% of samples landing at mode-interpolated locations — the core hallucination phenomenon.",
    width: 1440,
    height: 660,
    tag: "Hallucination Demo",
    tagColor: "rose",
    theorem: "Fig. 1 · Theorem 4.2",
  },
  {
    id: "midpoint",
    src: "/assets/midpoint_neighborhood.gif",
    title: "Midpoint Neighbourhood — Binary Outcomes",
    caption:
      "Two trajectories initialised near the midpoint y₀ exhibit a sharp bifurcation: the blue trajectory escapes toward a true mode (τ_exp ≈ 35), while the red trajectory is trapped and converges to y₀. The right panel plots the distance to the mode segment, confirming Theorem 4.2's critical threshold.",
    width: 1468,
    height: 677,
    tag: "Theorem 4.2",
    tagColor: "indigo",
    theorem: "Theorem 4.2",
  },
  {
    id: "convergence",
    src: "/assets/exp_convergence.gif",
    title: "Trajectory Convergence to Mode Segment",
    caption:
      "A single DDIM trajectory colored by reverse step (purple→yellow = noisy→clean) converging toward the line segment L(i,j) between two modes. The log-scale curve on the right quantifies the exponential decrease in distance d(xₜ, L(i,j)), validating the convergence bound in Theorem 4.2.",
    width: 1580,
    height: 684,
    tag: "Fig. 4 · Convergence",
    tagColor: "teal",
    theorem: "Proposition 5.1",
  },
  {
    id: "tracking",
    src: "/assets/tracking_stability.gif",
    title: "Tracking Stability Along the Nearby Line",
    caption:
      "Three-panel view: the full 25-mode geometry (left), the ξₜ coordinate band showing both trajectories staying within the x-band (center), and the pairwise xi-gap |ξₜ⁽¹⁾ − ξₜ⁽²⁾| decaying at rate λ ≈ 0.19 (right). This validates the tracking stability lemma: trajectories that enter a common line segment stay together.",
    width: 1940,
    height: 602,
    tag: "Tracking Stability",
    tagColor: "indigo",
    theorem: "Lemma 3.1",
  },
  {
    id: "modes-far",
    src: "/assets/modes_far_apart.gif",
    title: "Modes Far Apart — T_far Threshold",
    caption:
      "When modes are far apart (‖μᵢ − μⱼ‖ large), the inter-mode distance (solid blue) stays below the T_far threshold (dashed) throughout the reverse process. This regime is where mode interpolation becomes most likely: the score field near y₀ is nearly flat and deterministic dynamics have no escape route.",
    width: 1500,
    height: 648,
    tag: "Mode Separation",
    tagColor: "amber",
    theorem: "Corollary 4.3",
  },
  {
    id: "dominance",
    src: "/assets/two_mode_dominance.gif",
    title: "Two-Mode Dominance Dynamics",
    caption:
      "The D_dom metric (minimum distance gap between near modes and far modes) evolves over 50 reverse steps for four labeled modes. The dotted envelope tracks the minimum-gap lower bound; the red dashed line marks the 2σₜ²κ threshold. Once D_dom rises above this threshold the trajectory is committed to its dominant mode pair.",
    width: 1581,
    height: 686,
    tag: "Mode Dominance",
    tagColor: "violet",
    theorem: "Proposition 4.4",
  },
];

const TAG_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  rose:    { bg: "bg-rose-50",    border: "border-rose-200",    text: "text-rose-700"    },
  indigo:  { bg: "bg-indigo-50",  border: "border-indigo-200",  text: "text-indigo-700"  },
  teal:    { bg: "bg-teal-50",    border: "border-teal-200",    text: "text-teal-700"    },
  amber:   { bg: "bg-amber-50",   border: "border-amber-200",   text: "text-amber-700"   },
  violet:  { bg: "bg-violet-50",  border: "border-violet-200",  text: "text-violet-700"  },
};

function ExperimentCard({ exp, index, inView }: {
  exp: typeof EXPERIMENTS[number];
  index: number;
  inView: boolean;
}) {
  const tc = TAG_COLORS[exp.tagColor];

  return (
    <motion.div
      initial={{ opacity: 0, y: 28 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] as const, delay: 0.07 * index }}
      className="flex flex-col gap-4"
    >
      <div className="rounded-xl overflow-hidden border border-slate-200 bg-white shadow-[0_2px_12px_0_rgb(0,0,0,0.05)]">
        <div className="relative w-full" style={{ aspectRatio: `${exp.width}/${exp.height}` }}>
          <Image
            src={exp.src}
            alt={exp.title}
            fill
            unoptimized
            className="object-contain"
            sizes="(max-width: 768px) 100vw, 50vw"
          />
        </div>
      </div>
      <div className="flex flex-col gap-2 px-1">
        <div className="flex items-center gap-2 flex-wrap">
          <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full border ${tc.bg} ${tc.border} ${tc.text}`}>
            {exp.tag}
          </span>
          <span className="text-[11px] text-slate-400 font-mono">{exp.theorem}</span>
        </div>
        <span className="text-[13px] font-semibold text-slate-800">{exp.title}</span>
        <p className="font-serif text-[13.5px] leading-relaxed text-slate-600 italic">
          {exp.caption}
        </p>
      </div>
    </motion.div>
  );
}

export default function Experiments() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-60px" });

  return (
    <section id="experiments" className="py-24 px-6 bg-slate-50/50" ref={ref}>
      <hr className="section-divider mb-24" />
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] as const }}
          className="flex flex-col gap-3 mb-14"
        >
          <div className="flex items-center gap-3">
            <div className="w-6 h-px bg-teal-400" />
            <span className="text-xs font-semibold text-teal-500 uppercase tracking-widest">
              Supplementary Experiments
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Theory in Motion
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            Frame-by-frame simulations showing the theoretical phenomena playing out in practice.
            Each animation directly corresponds to a theorem, proposition, or figure in the paper.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-10">
          {EXPERIMENTS.map((exp, i) => (
            <ExperimentCard key={exp.id} exp={exp} index={i} inView={inView} />
          ))}
        </div>
      </div>
    </section>
  );
}
