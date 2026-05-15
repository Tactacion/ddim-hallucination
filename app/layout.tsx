import type { Metadata } from "next";
import { Inter, Lora } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const lora = Lora({
  variable: "--font-lora",
  subsets: ["latin"],
  display: "swap",
  style: ["normal", "italic"],
});

export const metadata: Metadata = {
  title: "Why DDIM Hallucinates More than DDPM | ICML 2026",
  description:
    "A theoretical analysis of reverse dynamics in DDPM and DDIM diffusion samplers. Accepted at ICML 2026.",
  openGraph: {
    title: "Why DDIM Hallucinates More than DDPM: A Theoretical Analysis of Reverse Dynamics",
    description:
      "We theoretically study hallucination phenomena in two canonical diffusion samplers. Accepted at ICML 2026.",
    type: "article",
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${inter.variable} ${lora.variable} scroll-smooth`}>
      <body className="antialiased">{children}</body>
    </html>
  );
}
