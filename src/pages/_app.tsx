import React from 'react'
import Script from "next/script";
import '../../styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/globals/Layout'
import { ThemeProvider } from '../components/ThemeContext'
import { useEffect } from "react";
import { useRouter } from "next/router";
import * as ga from "../google_analytics";
function MyApp({ Component, pageProps }: AppProps) {

  const router = useRouter();

  useEffect(() => {
    const handleRouteChange = (url) => {
      ga.pageview(url);
    };

    router.events.on("routeChangeComplete", handleRouteChange);
    return () => {
      router.events.off("routeChangeComplete", handleRouteChange);
    };
  }, [router.events]);

  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_MEASUREMENT_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', '${process.env.NEXT_PUBLIC_MEASUREMENT_ID}');
        `}
      </Script>

      <ThemeProvider>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </ThemeProvider>
    </>
  );
}

export default MyApp
