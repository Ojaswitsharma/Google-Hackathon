export default function Page3() {
  return (
    <main className="relative min-h-screen flex flex-col items-center bg-gradient-to-br from-[#C7EED9] to-[#A9D8B8] overflow-x-hidden font-[Outfit]">
      {/* Background dots */}
      <div className="absolute inset-0 bg-[radial-gradient(white_1px,transparent_1px)] bg-[length:40px_40px] opacity-40 pointer-events-none" />

      {/* Top Navbar */}
      <header className="absolute top-0 left-0 w-full flex items-center justify-between px-12 py-6 z-10">
        {/* Left logo bubble */}
        <div className="w-[180px] h-[180px] bg-white rounded-full flex items-center justify-center shadow-md">
          <span className="text-[#2F6153] font-bold text-xl">Safe World</span>
        </div>

        {/* Right nav bubble */}
        <div className="w-[320px] h-[120px] bg-white rounded-full flex items-center justify-center gap-6 shadow-md">
          <a href="/" className="text-[#2F6153] font-medium">
            Home
          </a>
          <a href="#" className="text-[#2F6153] font-medium">
            About
          </a>
          <a href="/page3" className="text-[#2F6153] font-medium">
            My Journal
          </a>
          <a href="#" className="text-[#2F6153] font-medium">
            Log out
          </a>
        </div>
      </header>

      {/* Card Grid */}
      <section className="mt-72 w-11/12 max-w-5xl z-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
          {Array.from({ length: 4 }).map((_, i) => (
            <div
              key={i}
              className="bg-white rounded-2xl shadow-md p-4 transition-transform hover:-translate-y-1 hover:shadow-xl"
            >
              <div
                className="rounded-xl h-48 flex items-center justify-center font-medium text-lg text-[#2F6153]
                           bg-gradient-to-br from-[#C7EED9] to-[#A9D8B8]"
              >
                previous world
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
