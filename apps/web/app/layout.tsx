import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "108-Jeevan Reader", description: "Jyotisha and 108-Jeevan professional reading console" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
