"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();

    if (username && password) {
      router.push("/home"); // ✅ redirect to Page1
    } else {
      alert("Please enter username and password");
    }
  };

  // 🔑 Prevent hydration mismatch by only rendering on client
  if (!mounted) return null;

  return (
    <main className="flex items-center justify-center min-h-screen bg-white font-[Outfit]">
      <div className="bg-[#A9E4D0] p-10 rounded-3xl w-[400px] shadow-lg">
        {/* Title */}
        <h1 className="text-2xl font-bold text-center text-[#2F6153] mb-6">
          Safe World
        </h1>

        {/* Form */}
        <form onSubmit={handleLogin} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2F6153]"
          />

          <input
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#2F6153]"
          />

          <p className="text-sm text-gray-600 cursor-pointer hover:underline">
            Forgot password?
          </p>

          <button
            type="submit"
            className="bg-[#2F6153] text-white py-3 rounded-full font-bold hover:bg-[#245043] transition"
          >
            Login
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center my-6">
          <hr className="flex-grow border-t border-gray-300" />
          <span className="px-2 text-gray-500">or</span>
          <hr className="flex-grow border-t border-gray-300" />
        </div>

        {/* Google Login */}
        <button
          onClick={() => router.push("/home")}
          className="w-full py-3 bg-white rounded-full border font-semibold shadow-sm hover:bg-gray-100"
        >
          Login with GOOGLE
        </button>

        {/* Signup link */}
        <p className="text-center text-sm mt-6">
          Don’t have an account?{" "}
          <span className="text-[#00BFFF] font-medium cursor-pointer hover:underline">
            Sign-up
          </span>
        </p>
      </div>
    </main>
  );
}
