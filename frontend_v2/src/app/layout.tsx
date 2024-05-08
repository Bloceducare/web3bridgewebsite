import type { Metadata } from "next";
import { Encode_Sans_Expanded } from "next/font/google";
import "@/styles/globals.css";
import { cn } from "@/lib/utils";
import Header from "@/components/shared/Header";
import { ThemeProvider } from "@/providers/ThemeProvider";
import Footer from "@/components/shared/Footer";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import { Toaster } from "@/components/ui/sonner";

const fontSans = Encode_Sans_Expanded({
  subsets: ["latin"],
  weight: ["100", "200", "300", "400", "500", "600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "Web3Bridge",
  description: "web3bridgeafrica website",
  icons: {
    icon: "/favicon.ico",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={cn(
          "min-h-screen overflow-x-hidden antialiased flex flex-col bg-background dark:bg-[url('../../public/dark.svg')] bg-fixed",
          fontSans.className
        )}>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange>
          <Toaster richColors />
          <Header />

          <main className="flex-1">{children}</main>

          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
