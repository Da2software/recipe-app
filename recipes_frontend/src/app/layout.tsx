import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

// reduxtoolkit
import { Providers } from "./provider";
import { store } from "./store";

import ThemeProviderContainer from "./theme";
import Navbar from "@/components/navbar/navbar";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <Providers>
      <html lang="en">
        <body className={inter.className}>
          <ThemeProviderContainer>
            <Navbar></Navbar>
            {children}
          </ThemeProviderContainer>
        </body>
      </html>
    </Providers>
  );
}
