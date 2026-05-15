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
    caption: (
      <>
        DDIM on a 25-mode Gaussian grid: the left panel traces the reverse
        trajectory; the right panel demonstrates the final sample distribution.
        The legend reports ~9.4% of samples as <em>mode interpolations</em>:
        regions of low probability mass between the true Gaussian modes.
      </>
    ),
    width: 1440,
    height: 660,
    tag: "Hallucination Demo",
    tagColor: "rose",
  },
  {
    id: "midpoint",
    src: "/assets/midpoint_neighborhood.gif",
    title: "DDIM Trapping vs. DDPM Escape Near Midpoint",
    caption:
      "We prove that after Asm. 4.4 holds, in a neighborhood around the midpoint, DDIM trajectories (blue) can get stuck while DDPM trajectories (red) can escape, explaining the hallucination rate gap between the two samplers.",
    width: 1468,
    height: 677,
    tag: "Props. 4.7, 5.1",
    tagColor: "indigo",
  },
  {
    id: "convergence",
    src: "/assets/exp_convergence.gif",
    title: "Exponential Convergence to Nearby Line",
    caption:
      'We demonstrate that after Asm. 4.1 holds in the reverse process, DDIM trajectories converge towards the line segment joining modes "i" and "j" exponentially fast.',
    width: 1580,
    height: 684,
    tag: "Theorem 4.2",
    tagColor: "teal",
  },
  {
    id: "tracking",
    src: "/assets/tracking_stability.gif",
    title: "Tracking Stability Near Modes",
    caption:
      "We prove that after Asm. 4.4 holds in the reverse process, trajectories that land on the line segment near a mode attract to a stable trajectory near that mode.",
    width: 1940,
    height: 602,
    tag: "Prop. 4.5, Cor. 4.6",
    tagColor: "indigo",
  },
  {
    id: "modes-far",
    src: "/assets/modes_far_apart.gif",
    title: "Modes Sufficiently Far Apart",
    caption:
      'We assume that there exists a time so that the distance between modes "i" and "j" (solid blue) is sufficiently large (dotted blue). This assumption is natural for an analysis of mode interpolation of hallucinations, since otherwise there are no regions of low probability mass.',
    width: 1500,
    height: 648,
    tag: "Asm. 4.4",
    tagColor: "amber",
  },
  {
    id: "dominance",
    src: "/assets/two_mode_dominance.gif",
    title: "Two Mode Dominance",
    caption:
      'We assume that there exists a time, so that the trajectory is sufficiently closer (dotted red line) to a pair of modes "i" and "j" than any other pair. We find that this assumption holds empirically, visualized by the red diamond for a DDIM trajectory with 50 steps.',
    width: 1581,
    height: 686,
    tag: "Asm. 4.1",
    tagColor: "violet",
  },
];

type Experiment = (typeof EXPERIMENTS)[number];

const THEORY_SECTIONS = [
  {
    title: "Mode Interpolations",
    experimentIds: ["mode-interp"],
  },
  {
    title: "Assumptions",
    experimentIds: ["dominance", "modes-far"],
  },
  {
    title: "Key Results",
    experimentIds: ["convergence", "tracking", "midpoint"],
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
  exp: Experiment;
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
  const getExperiment = (id: string) => EXPERIMENTS.find((exp) => exp.id === id);

  return (
    <section id="theory" className="py-24 px-6 bg-slate-50/50" ref={ref}>
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
              Theory
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Theory in Motion
          </h2>
          <p className="text-slate-500 text-[15px] leading-relaxed max-w-2xl">
            Frame-by-frame simulations showing the theoretical phenomena playing out in practice.
            Each animation corresponds to a key concept or theorem from the paper.
          </p>
        </motion.div>

        <div className="flex flex-col gap-16">
          {THEORY_SECTIONS.map((section, sectionIndex) => {
            const experiments = section.experimentIds
              .map(getExperiment)
              .filter((exp): exp is Experiment => Boolean(exp));

            return (
              <div key={section.title} className="flex flex-col gap-7">
                <motion.h3
                  initial={{ opacity: 0, y: 16 }}
                  animate={inView ? { opacity: 1, y: 0 } : {}}
                  transition={{
                    duration: 0.55,
                    ease: [0.16, 1, 0.3, 1] as const,
                    delay: 0.08 * sectionIndex,
                  }}
                  className="text-lg font-bold text-slate-800 tracking-tight"
                >
                  {section.title}
                </motion.h3>
                <div
                  className={
                    experiments.length === 1
                      ? "grid grid-cols-1 gap-10"
                      : "grid grid-cols-1 sm:grid-cols-2 gap-10"
                  }
                >
                  {experiments.map((exp, i) => (
                    <ExperimentCard
                      key={exp.id}
                      exp={exp}
                      index={sectionIndex + i}
                      inView={inView}
                    />
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
