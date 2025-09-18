import type { Metadata } from "next";
import { Outfit, Readex_Pro } from "next/font/google";
import "./globals.css";

// Fonts
const outfit = Outfit({
  subsets: ["latin"],
  variable: "--font-outfit",
  weight: ["400", "500", "600", "700"],
});

const readexPro = Readex_Pro({
  subsets: ["latin"],
  variable: "--font-readex",
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "World Builder",
  description: "Your safe world app",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`${outfit.variable} ${readexPro.variable} antialiased bg-background text-foreground`}
      >
        {children}
      </body>
    </html>
  );
}
