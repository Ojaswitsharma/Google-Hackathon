"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Mic } from "lucide-react";
import Link from "next/link";

export default function HomePage() {
  const [stars, setStars] = useState<{ top: string; left: string; opacity: number }[]>([]);
  const [listening, setListening] = useState(false);
  const [text, setText] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);

    const generated = Array.from({ length: 40 }, () => ({
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`,
      opacity: Math.random(),
    }));
    setStars(generated);
  }, []);

  const handleMicClick = () => {
    if (typeof window === "undefined") return;

    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Your browser does not support Speech Recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);

    recognition.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0].transcript)
        .join("");
      setText(transcript);
    };

    recognition.start();
  };

  if (!mounted) return null;

  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center text-center font-[Outfit]">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#C7EED9] to-[#A9D8B8] overflow-hidden -z-10">
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-[500px] h-[500px] bg-white/40 blur-[150px] rounded-full"></div>
        </div>
        {stars.map((star, i) => (
          <div
            key={i}
            className="absolute w-2 h-2 bg-white rounded-full"
            style={{ top: star.top, left: star.left, opacity: star.opacity }}
          />
        ))}
      </div>

      {/* Navbar */}
      <header className="absolute top-0 left-0 w-full flex items-center justify-between px-12 py-6 z-10">
        <div className="w-[180px] h-[180px] bg-white rounded-full flex items-center justify-center shadow-md">
          <span className="text-[#2F6153] font-bold text-xl">Safe World</span>
        </div>
        <div className="w-[320px] h-[120px] bg-white rounded-full flex items-center justify-center gap-6 shadow-md">
          <Link href="/home" className="text-[#2F6153] font-medium">
            Home
          </Link>
          <a href="#" className="text-[#2F6153] font-medium">
            About
          </a>
          <Link href="/page2" className="text-[#2F6153] font-medium">
            My Journal
          </Link>
          <Link href="/" className="text-[#2F6153] font-medium">
            Log out
          </Link>
        </div>
      </header>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center mt-32">
        <h1 className="text-[60px] font-bold text-[#2F6153] mb-6">
          Welcome to Your Safe World
        </h1>
        <p className="text-[24px] text-[#2F6153] mb-2">Step into a place made just for you</p>
        <p className="text-[24px] text-[#2F6153] mb-12">
          Your emotions, your world, your peace
        </p>

        {/* Input Box + Mic */}
        <div className="flex items-center gap-3 w-[523px] mb-8 bg-[#7BA894] rounded-full px-4 py-3 shadow-lg">
          <input
            type="text"
            placeholder="How are you feeling today?"
            className="flex-1 bg-transparent text-white placeholder-white text-[18px] focus:outline-none"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button
            onClick={handleMicClick}
            className={`p-4 rounded-full text-white ${
              listening ? "bg-red-500" : "bg-[#5f8570]"
            }`}
          >
            <Mic className="w-6 h-6" />
          </button>
        </div>

        {/* CREATE MY STORY */}
        <Link href="/page2" passHref>
          <Button
            className="text-white font-semibold shadow-md w-[523px] h-[85px] rounded-[40px] text-[30px]"
            style={{ backgroundColor: "#7BA894", fontFamily: "Readex Pro, sans-serif" }}
          >
            CREATE MY STORY
          </Button>
        </Link>
      </div>
    </main>
  );
}
