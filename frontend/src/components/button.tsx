import React, { useState } from "react";

export const Button = ({
  isDisabled,
  title,
}: {
  isDisabled: boolean;
  title: string;
}) => {
  return (
    <button
      disabled={isDisabled}
      className={`mt-4 block border-solid p-2 ${
        isDisabled ? "bg-pink-200 text-pink-100	" : "bg-pink-600"
      }`}
      type="submit"
    >
      {title}
    </button>
  );
};
