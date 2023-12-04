import React, { useState } from "react";

import { submitForm } from "@/helpers/upload";
import { validateEmail } from "@/helpers/validateEmail";

import { Button } from "@/components/button";

type FormProps = {
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
  setResponseMessage: React.Dispatch<React.SetStateAction<string>>;
};

const Input = ({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) => (
  <div className="flex flex-col	">
    <label className="border-solid block py-2">
      <span className="text-gray-700">{label}</span>
      {children}
    </label>
  </div>
);

export const Form: React.FC<FormProps> = ({
  setIsLoading,
  setResponseMessage,
}) => {
  const [selfieFile, setSelfieFile] = useState<File | null>(null);
  const [outfitFile, setOutfitFile] = useState<File | null>(null);
  const [email, setEmail] = useState("");

  const handleSelfieChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event?.target?.files) {
      return;
    }

    setSelfieFile(event.target.files[0]);
  };

  const handleOutfitChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event?.target?.files) {
      return;
    }

    setOutfitFile(event.target.files[0]);
  };

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    console.log("**LOG** handleEmailChange — event: ", event.target.value);
    console.log("validateEmail: ", validateEmail(event.target.value));
    setEmail(event.target.value);
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!selfieFile || !outfitFile) {
      return;
    }

    try {
      console.log("**LOG** handleSubmit email: ", email);
      console.log("**LOG** handleSubmit selfieFile: ", selfieFile);

      setIsLoading(true);
      const response = await submitForm({ email, selfieFile, outfitFile });

      console.log("**LOG** response: ", response);
      setResponseMessage(response.message);
      setIsLoading(false);
    } catch (error) {
      console.error("Error uploading file:", error);
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={(e) => handleSubmit(e)}
      className="grid grid-cols-1 divide-y"
    >
      <Input label="Email">
        <input
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2"
          type="email"
          onChange={handleEmailChange}
          placeholder="hello@example.com"
        />
      </Input>

      <Input label="Your Selfie">
        <>
          <input className="block" type="file" onChange={handleSelfieChange} />
        </>
      </Input>

      <Input label="Outfit Image">
        <>
          <input className="block" type="file" onChange={handleOutfitChange} />
        </>
      </Input>

      <Button isDisabled={!validateEmail(email)} title="Upload" />
    </form>
  );
};
