"use client";

import { motion } from "framer-motion";
import Image from "next/image";

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] as const, delay },
});

const AUTHORS: { name: string; equal?: boolean }[] = [
  { name: "Muhammad H. Ashiq", equal: true },
  { name: "Samanyu Arora", equal: true },
  { name: "Abhinav N. Harish" },
  { name: "Ishaan Kharbanda" },
  { name: "Hung Yun Tseng" },
  { name: "Grigorios G. Chrysos" },
];

const HERO_ANIMATIONS = [
  { src: "/assets/GMMLandscape3D.mp4" },
  { src: "/assets/DDPMvsDDIMFinal.mp4" },
];

const HERO_ANIMATION_CAPTION =
  "Reverse dynamics: deterministic DDIM gets stuck in the midpoint neighborhood, while stochastic DDPM escapes.";

type ButtonProps = {
  href: string;
  icon: React.ReactNode;
  label: string;
  primary?: boolean;
};

function ActionButton({ href, icon, label, primary }: ButtonProps) {
  return (
    <a
      href={href}
      target={href.startsWith("http") || href.endsWith(".pdf") ? "_blank" : undefined}
      rel="noopener noreferrer"
      className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-200 ${
        primary
          ? "bg-indigo-600 text-white hover:bg-indigo-700 shadow-[0_2px_8px_0_rgb(79,70,229,0.25)] hover:shadow-[0_4px_16px_0_rgb(79,70,229,0.35)]"
          : "bg-white text-slate-700 border border-slate-200 hover:border-slate-300 hover:bg-slate-50 shadow-[0_1px_3px_0_rgb(0,0,0,0.06)]"
      }`}
    >
      {icon}
      {label}
    </a>
  );
}

function HeroAnimationCard({ animation }: { animation: typeof HERO_ANIMATIONS[number] }) {
  return (
    <div
      className="relative rounded-2xl overflow-hidden bg-[#F8F7F4] border border-slate-200 h-full flex flex-col"
      style={{ boxShadow: "0 20px 60px -12px rgba(0,0,0,0.10), 0 8px 24px -4px rgba(0,0,0,0.06)" }}
    >
      <video
        className="w-full block bg-[#F8F7F4]"
        autoPlay
        loop
        muted
        playsInline
        style={{ display: "block" }}
      >
        <source src={animation.src} type="video/mp4" />
      </video>
    </div>
  );
}

const PaperIcon = () => (
  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>
);
const CodeIcon = () => (
  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
  </svg>
);
const ArxivIcon = () => (
  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
    <path d="M3 3h18v18H3V3zm16 16V5H5v14h14zM7 7h10v2H7V7zm0 4h10v2H7v-2zm0 4h7v2H7v-2z" />
  </svg>
);
const VideoIcon = () => (
  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
    <path strokeLinecap="round" strokeLinejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

export default function Hero() {
  return (
    <section
      id="hero"
      className="relative min-h-screen flex flex-col items-center justify-center pt-24 pb-20 px-6"
    >
      {/* Subtle background texture */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(ellipse 80% 60% at 50% 0%, rgba(199, 210, 254, 0.18) 0%, transparent 70%)",
        }}
      />

      <div className="relative z-10 max-w-4xl mx-auto w-full flex flex-col items-center text-center gap-8">
        {/* Conference badge */}
        <motion.div {...fadeUp(0)}>
          <div className="inline-flex items-center gap-2 bg-indigo-50 border border-indigo-200 text-indigo-700 text-[13px] font-medium px-4 py-1.5 rounded-full">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-indigo-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-indigo-500" />
            </span>
            Accepted · ICML 2026 · Seoul, South Korea
          </div>
        </motion.div>

        {/* Title */}
        <motion.h1
          {...fadeUp(0.08)}
          className="text-3xl sm:text-4xl md:text-[2.625rem] font-bold text-slate-900 leading-[1.18] tracking-tight max-w-3xl"
        >
          Why DDIM Hallucinates More than DDPM:{" "}
          <span className="text-slate-600 font-normal font-serif italic">
            A Theoretical Analysis of Reverse Dynamics
          </span>
        </motion.h1>

        {/* Authors */}
        <motion.div {...fadeUp(0.16)} className="flex flex-col items-center gap-2">
          <p className="text-slate-600 text-sm leading-relaxed max-w-2xl">
            {AUTHORS.map((author, i) => (
              <span key={author.name}>
                <span className="text-slate-700 font-medium">{author.name}</span>
                {author.equal && (
                  <sup className="text-rose-500 font-semibold ml-px text-[10px]">†</sup>
                )}
                {i < AUTHORS.length - 1 && (
                  <span className="text-slate-400 mx-1.5">·</span>
                )}
              </span>
            ))}
          </p>
          <div className="text-[13px] text-slate-500 flex flex-col items-center gap-1.5">
            <a
              href="https://www.wisc.edu"
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-indigo-600 transition-colors duration-200 inline-flex items-center gap-1.5"
            >
              <div className="relative w-5 h-5 rounded overflow-hidden inline-block">
                <Image src="/uw-logo.png" alt="UW–Madison" fill sizes="20px" className="object-contain" />
              </div>
              University of Wisconsin–Madison
            </a>
            <p className="text-[12px] text-slate-400">
              <sup className="text-rose-400 font-semibold">†</sup> Equal contribution
            </p>
          </div>
        </motion.div>

        {/* Action buttons */}
        <motion.div {...fadeUp(0.22)} className="flex flex-wrap items-center justify-center gap-3">
          <ActionButton href="/paper.pdf" icon={<PaperIcon />} label="Paper" primary />
          <ActionButton href="https://github.com" icon={<CodeIcon />} label="Code" />
          <ActionButton href="https://arxiv.org/abs/2605.06831" icon={<ArxivIcon />} label="arXiv" />
          <ActionButton href="#figures" icon={<VideoIcon />} label="Videos" />
        </motion.div>

        {/* Hero — Manim animations */}
        <motion.div
          {...fadeUp(0.3)}
          className="w-full mt-4"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-stretch">
            {HERO_ANIMATIONS.map((animation) => (
              <HeroAnimationCard key={animation.src} animation={animation} />
            ))}
          </div>
          <div className="mt-3 bg-white/80 border border-slate-100 px-5 py-3 rounded-xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
            <span className="text-[12px] text-slate-500 text-left">
              {HERO_ANIMATION_CAPTION}
            </span>
            <span className="inline-flex items-center gap-1 text-[11px] text-indigo-500 font-medium whitespace-nowrap">
              <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
              Rendered with Manim
            </span>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
