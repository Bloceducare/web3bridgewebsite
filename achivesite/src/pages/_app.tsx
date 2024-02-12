import React from 'react'
import 'react-dropzone-uploader/dist/styles.css'
import 'react-phone-input-2/lib/style.css'
import '../../styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/globals/Layout'
import { ThemeProvider } from '../components/ThemeContext'
function MyApp({ Component, pageProps }: AppProps) {
  return (
  <ThemeProvider >
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </ThemeProvider>
  )
}

export default MyApp
