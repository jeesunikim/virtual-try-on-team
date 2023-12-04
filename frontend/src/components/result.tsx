import React from "react";

export const Result = ({
  isLoading,
  responseMessage,
}: {
  isLoading: boolean;
  responseMessage: string;
}) => {
  console.log("**LOG** isLoading :", isLoading);

  return (
    <div>
      <h3>{isLoading && "waiting..."}</h3>
      <h3>{responseMessage && responseMessage}</h3>
    </div>
  );
};
