import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Abstract from "./components/Abstract";
import Contributions from "./components/Contributions";
import Experiments from "./components/Experiments";
import Figures from "./components/Figures";
import BibTeX from "./components/BibTeX";
import Footer from "./components/Footer";

export default function Home() {
  return (
    <main className="min-h-screen" style={{ background: "var(--bg-page)" }}>
      <Navbar />
      <Hero />
      <Abstract />
      <Contributions />
      <Experiments />
      <Figures />
      <BibTeX />
      <Footer />
    </main>
  );
}
