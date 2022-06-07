import { useState, useEffect } from "react";
import "../styles/globals.css";
import type { AppProps } from "next/app";
import { ThemeProvider } from "../components/ThemeContext";

function MyApp({ Component, pageProps }: AppProps) {
  const [showChild, setShowChild] = useState(false);
  useEffect(() => {
    setShowChild(true);
  }, []);

  if (!showChild) {
    return null;
  }

  if (typeof window === "undefined") {
    return <></>;
  } else {
    return (
      <ThemeProvider>
        <Component {...pageProps} />
      </ThemeProvider>
    );
  }
}

export default MyApp;
