import Head from "next/head";
import Navbar from "./Navbar";
import React, { ReactNode } from "react";
import Footer from "./Footer";
import Background from "../Background";
import TopHeader from "./TopHeader";

interface Props {
  children?: ReactNode;
  // any props that come into the component
}
const Layout = ({ children }: Props) => {
  return (
    <>
      <Head>
        <title>Web3bridge</title>
        <link rel="shortcut icon" href="favicon.png" />
        <meta property="og:url" content="" />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="web3bride" />
        <meta property="og:description" content="Welcome to web3bridge" />
        <meta property="og:image" content="" />

        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" />
        <link
          href="https://fonts.googleapis.com/css2?family=DM+Sans&family=Poppins&display=swap"
          rel="stylesheet"
        ></link>
      </Head>
      <Background>
        <TopHeader />
        <Navbar />
        {children}
        <Footer />
      </Background>
    </>
  );
};

export default Layout;
