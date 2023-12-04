"use client";

import React, { useState } from "react";

import Image from "next/image";

import { Form } from "@/components/form";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { Result } from "@/components/result";

export default function Home() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [responseMessage, setResponseMessage] = useState("");

  return (
    <main className="flex items-center flex-col min-h-screen font-mono ">
      <Header />
      <div className="flex items-center font-mono	py-14 w-3/5">
        <div className="max-w-3xl	 w-full h-4/6 pr-5">
          <Form
            setIsLoading={setIsLoading}
            setResponseMessage={setResponseMessage}
          />
        </div>
        <div className="max-w-3xl	 w-full h-4/6">
          <Result isLoading={isLoading} responseMessage={responseMessage} />
        </div>
        <Footer />
      </div>
    </main>
  );
}
