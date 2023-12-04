import axios from "axios";

const testApiKey = "87c7d061538f397245ceb7ccc99fa376";

// OUR API
// outfit
// selfie
// email

export const submitForm = async ({
  email,
  selfieFile,
  outfitFile,
}: {
  email: string;
  selfieFile: File;
  outfitFile: File;
}) => {
  const formData = new FormData();
  formData.append("selfie", selfieFile);
  formData.append("outfit", outfitFile);
  formData.append("email", email);

  // the below is a dummy api's requirement
  formData.append("image", outfitFile);

  console.log("**LOG** formData: ", formData);

  try {
    // const response = await axios.post(
    //   `https://api.imgbb.com/1/upload?key=${testApiKey}`,
    //   formData,
    //   {
    //     headers: {
    //       "Content-Type": "multipart/form-data",
    //     },
    //   }
    // );

    const response = await axios.post(
      `http://192.168.3.21:8000/api/try_on/try_on_outfit/${email}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    console.log("**LOG** response.data: ", response.data);
    return response.data;
  } catch (error) {
    console.error("Error uploading image: ", error);
    throw error;
  }
};
