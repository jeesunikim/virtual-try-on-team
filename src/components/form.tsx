import React, { useState } from "react";
import { uploadImage } from "@/helpers/upload";

const FormRow = ({ children }: { children: React.ReactNode }) => (
  <div className="flex flex-col	">{children}</div>
);

const Input = ({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) => (
  <label className="border-solid block py-2">
    <span className="text-gray-700">{label}</span>
    {children}
  </label>
);
export const Form = () => {
  const [file, setFile] = useState(null);
  const [email, setEmail] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleEmailChange = (event) => {
    console.log("**LOG** handleEmailChange — event: ", event.target.value);
    setEmail(event.target.value);
  };

  const handleSubmit = async (event: HTMLFormElement) => {
    event.preventDefault();
    if (!file) {
      return;
    }
    try {
      const response = await uploadImage(file);
      console.log(response);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <form
      onSubmit={(e) => handleSubmit(e)}
      className="grid grid-cols-1 divide-y"
    >
      <FormRow>
        <Input label="Email">
          <input
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50 p-2"
            type="email"
            onChange={handleEmailChange}
            placeholder="hello@example.com"
          />
        </Input>
      </FormRow>

      <FormRow>
        <Input label="Image">
          <>
            <input className="block" type="file" onChange={handleFileChange} />
            <button className="bg-pink-600	 border-solid p-2" type="submit">
              Upload
            </button>
          </>
        </Input>
      </FormRow>
    </form>
  );
};
