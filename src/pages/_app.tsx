import React from 'react'
import '../../styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/globals/Layout'
import { ThemeProvider } from 'next-theme'
function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ThemeProvider attribute="class">
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </ThemeProvider>
  )
}

export default MyApp
