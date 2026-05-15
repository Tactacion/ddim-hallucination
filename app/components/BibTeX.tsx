"use client";

import { motion } from "framer-motion";
import { useInView } from "framer-motion";
import { useRef, useState } from "react";

const BIBTEX = `@inproceedings{ashiq2026ddim,
  title     = {Why {DDIM} Hallucinates More than {DDPM}:
               A Theoretical Analysis of Reverse Dynamics},
  author    = {Ashiq, Muhammad H. and Arora, Samanyu and
               Harish, Abhinav N. and Kharbanda, Ishaan and
               Tseng, Hung Yun and Chrysos, Grigorios G.},
  booktitle = {Proceedings of the 43rd International Conference
               on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  year      = {2026},
  address   = {Seoul, South Korea},
  publisher = {PMLR},
  note      = {ICML 2026}
}`;

export default function BibTeX() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: "-80px" });
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(BIBTEX);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback: select text
      const pre = document.querySelector(".bibtex-block");
      if (pre) {
        const range = document.createRange();
        range.selectNodeContents(pre);
        window.getSelection()?.removeAllRanges();
        window.getSelection()?.addRange(range);
      }
    }
  };

  return (
    <section id="bibtex" className="py-24 px-6 bg-slate-50/60" ref={ref}>
      <hr className="section-divider mb-24" />
      <div className="max-w-4xl mx-auto">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-col gap-3 mb-10"
        >
          <div className="flex items-center gap-3">
            <div className="w-6 h-px bg-indigo-400" />
            <span className="text-xs font-semibold text-indigo-500 uppercase tracking-widest">
              Citation
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            BibTeX
          </h2>
          <p className="text-slate-500 text-[15px]">
            If you find this work useful, please cite our paper.
          </p>
        </motion.div>

        {/* BibTeX block */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1], delay: 0.1 }}
          className="relative rounded-xl overflow-hidden border border-slate-700 shadow-[0_8px_32px_0_rgb(0,0,0,0.18)]"
        >
          {/* Top bar */}
          <div className="flex items-center justify-between px-5 py-3 bg-slate-800 border-b border-slate-700">
            <div className="flex items-center gap-2">
              {/* Traffic light dots */}
              <span className="w-3 h-3 rounded-full bg-slate-600" />
              <span className="w-3 h-3 rounded-full bg-slate-600" />
              <span className="w-3 h-3 rounded-full bg-slate-600" />
              <span className="ml-3 text-[12px] text-slate-400 font-medium tracking-wide">
                citation.bib
              </span>
            </div>
            <button
              onClick={handleCopy}
              className={`inline-flex items-center gap-1.5 text-[12px] font-medium px-3 py-1.5 rounded-md transition-all duration-200 ${
                copied
                  ? "bg-teal-500/20 text-teal-300 border border-teal-500/30"
                  : "bg-slate-700 hover:bg-slate-600 text-slate-300 border border-slate-600"
              }`}
              aria-label="Copy BibTeX to clipboard"
            >
              {copied ? (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                  Copied!
                </>
              ) : (
                <>
                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round"
                      d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  Copy
                </>
              )}
            </button>
          </div>

          {/* Code body */}
          <div className="bg-slate-900 px-6 py-5 overflow-x-auto">
            <pre className="bibtex-block text-slate-300">{BIBTEX}</pre>
          </div>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={inView ? { opacity: 1 } : {}}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-8 text-[13px] text-slate-400 leading-relaxed max-w-2xl"
        >
          <strong className="text-slate-500">Acknowledgements.</strong>{" "}
          The authors thank the members of the Machine Learning Group at the University
          of Wisconsin–Madison for valuable discussions and feedback throughout this work.
          This research was conducted at UW–Madison and presented at ICML 2026, Seoul, South Korea.
        </motion.p>
      </div>
    </section>
  );
}
