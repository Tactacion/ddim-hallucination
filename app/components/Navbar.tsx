"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Image from "next/image";

const NAV_LINKS = [
  { label: "Abstract",      href: "#abstract"       },
  { label: "Theory",        href: "#theory"         },
  { label: "Figures",       href: "#figures"        },
  { label: "BibTeX",        href: "#bibtex"         },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handler = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", handler, { passive: true });
    return () => window.removeEventListener("scroll", handler);
  }, []);

  return (
    <AnimatePresence>
      <motion.header
        initial={{ y: -16, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
        className={`fixed top-0 inset-x-0 z-50 transition-all duration-300 ${
          scrolled
            ? "bg-[#f8f7f4]/90 backdrop-blur-md border-b border-slate-200/80 shadow-[0_1px_12px_0_rgb(0,0,0,0.05)]"
            : "bg-transparent"
        }`}
      >
        <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
          {/* Logo */}
          <a href="#hero" className="flex items-center gap-2.5 group">
            <div className="relative w-7 h-7 rounded overflow-hidden">
              <Image
                src="/uw-logo.png"
                alt="University of Wisconsin–Madison"
                fill
                sizes="28px"
                className="object-contain"
              />
            </div>
            <span className="text-xs font-medium text-slate-500 group-hover:text-slate-800 transition-colors hidden sm:block tracking-wide">
              UW–Madison
            </span>
          </a>

          {/* Nav links */}
          <nav className="flex items-center gap-6">
            {NAV_LINKS.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-[13px] font-medium text-slate-500 hover:text-indigo-600 transition-colors duration-200 hidden sm:block"
              >
                {link.label}
              </a>
            ))}
            <a
              href="/paper.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-[13px] font-medium px-3.5 py-1.5 rounded-full transition-colors duration-200"
            >
              <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              Paper
            </a>
          </nav>
        </div>
      </motion.header>
    </AnimatePresence>
  );
}
