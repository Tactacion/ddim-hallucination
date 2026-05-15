"use client";

import Image from "next/image";

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 py-10 px-6">
      <div className="max-w-4xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-5">
        {/* Left: institution */}
        <div className="flex items-center gap-3">
          <div className="relative w-8 h-8 rounded overflow-hidden">
            <Image src="/uw-logo.png" alt="University of Wisconsin–Madison" fill className="object-contain" />
          </div>
          <div className="flex flex-col">
            <span className="text-[13px] font-semibold text-slate-700">University of Wisconsin–Madison</span>
            <span className="text-[12px] text-slate-400">Machine Learning Group</span>
          </div>
        </div>

        {/* Center: conference */}
        <div className="text-center">
          <span className="inline-flex items-center gap-1.5 text-[12px] text-slate-500 bg-indigo-50 border border-indigo-100 px-3 py-1 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
            ICML 2026 · Seoul, South Korea
          </span>
        </div>

        {/* Right: links */}
        <div className="flex items-center gap-4 text-[12px] text-slate-400">
          <a href="/paper.pdf" target="_blank" rel="noopener noreferrer"
            className="hover:text-indigo-600 transition-colors">Paper</a>
          <span className="text-slate-200">|</span>
          <a href="https://arxiv.org/abs/2605.06831" target="_blank" rel="noopener noreferrer"
            className="hover:text-indigo-600 transition-colors">arXiv</a>
          <span className="text-slate-200">|</span>
          <a href="https://github.com" target="_blank" rel="noopener noreferrer"
            className="hover:text-indigo-600 transition-colors">Code</a>
        </div>
      </div>

      <div className="max-w-4xl mx-auto mt-6 pt-5 border-t border-slate-100 text-center">
        <p className="text-[11px] text-slate-400">
          © 2026 The Authors. Website template inspired by NeurIPS/ICML project pages.
        </p>
      </div>
    </footer>
  );
}
