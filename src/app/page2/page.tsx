"use client";

import Link from "next/link";

export default function Page2() {
  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center text-center font-[Outfit]">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#C7EED9] to-[#A9D8B8] overflow-hidden -z-10">
        {/* Diamond Glow */}
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-[500px] h-[500px] bg-white/40 blur-[150px] rounded-full"></div>
        </div>
      </div>

      {/* Top Navbar */}
      <header className="absolute top-0 left-0 w-full flex items-center justify-between px-12 py-6 z-10">
        {/* Left logo bubble */}
        <div className="w-[180px] h-[180px] bg-white rounded-full flex items-center justify-center shadow-md">
          <span className="text-[#2F6153] font-bold text-xl">Safe World</span>
        </div>

        {/* Right nav bubble */}
        <div className="w-[320px] h-[120px] bg-white rounded-full flex items-center justify-center gap-6 shadow-md">
          <Link href="/" className="text-[#2F6153] font-medium">
            Home
          </Link>
          <a href="#" className="text-[#2F6153] font-medium">
            About
          </a>
          <Link href="/page3" className="text-[#2F6153] font-medium">
            My Journal
          </Link>
          <a href="#" className="text-[#2F6153] font-medium">
            Log out
          </a>
        </div>
      </header>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center mt-32 w-full px-8 gap-8">
        {/* Smaller content box */}
        <div className="w-full max-w-2xl h-[300px] bg-white rounded-2xl shadow-md flex items-center justify-center">
          <span className="text-[#2F6153] text-lg">This is Page 2 content</span>
        </div>

        {/* Button to go to Page 3 */}
        <Link href="/page3">
          <button className="mt-6 px-8 py-3 bg-[#2F6153] text-white rounded-full shadow-md hover:bg-[#244d42] transition">
            View Previous Worlds
          </button>
        </Link>
      </div>
    </main>
  );
}
