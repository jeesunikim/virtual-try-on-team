from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from PIL import Image
import requests
import matplotlib.pyplot as plt
import torch.nn as nn
import torch
import cv2
import numpy as np
import argparse
import sys
import os
import tqdm
from glob import glob
from pathlib import Path

MAPPING = {
    "Background": 0,
    "Hat": 1,
    "Hair": 2,
    "Sunglasses": 3,
    "Upper-clothes": 4,
    "Skirt": 5,
    "Pants": 6,
    "Dress": 7,
    "Belt": 8,
    "Left-shoe": 9,
    "Right-shoe": 10,
    "Left-arm": 11,
    "Right-arm": 12,
    "Bag": 16,
    "Scarf": 17
}


def augment_image(image):
    # Randomly rotate the image
    rotation_angle = np.random.uniform(-25, 25)
    rows, cols = image.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (cols, rows), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    # Randomly scale the image
    scale_factor = np.random.uniform(0.8, 1.2)
    scaled_image = cv2.resize(rotated_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    # Pad the image with white pixels while preserving aspect ratio
    target_height, target_width = rows, cols
    pad_color = (255, 255, 255)
    pad_top = max(0, (target_height - scaled_image.shape[0]) // 2)
    pad_bottom = max(0, target_height - scaled_image.shape[0] - pad_top)
    pad_left = max(0, (target_width - scaled_image.shape[1]) // 2)
    pad_right = max(0, target_width - scaled_image.shape[1] - pad_left)
    
    padded_image = cv2.copyMakeBorder(scaled_image, pad_top, pad_bottom, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=pad_color)

    # Ensure the final image has the desired resolution
    final_image = cv2.resize(padded_image, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
    return final_image

def crop_item(
        data_dir,
        output_dir,
        item,
        num_augment=5

    ):
    # from pudb import set_trace
    # set_trace()
    piece_of_clothes = MAPPING[item]
    output_dir = Path(output_dir) / f"10_xyzclothes {item.lower()}"
    output_dir.mkdir(exist_ok=True, parents=True)

    processor = SegformerImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")

    for image_path in tqdm.tqdm(glob(f"{data_dir}/*")):
        image_name = Path(image_path).name
        image = Image.open(image_path).convert('RGB')
        inputs = processor(images=image, return_tensors="pt")

        outputs = model(**inputs)
        logits = outputs.logits.cpu()

        upsampled_logits = nn.functional.interpolate(
            logits,
            size=image.size[::-1],
            mode="bilinear",
            align_corners=False,
        )

        pred_seg = upsampled_logits.argmax(dim=1)[0]
        # plt.imshowqq(pred_seg)

        
        grayscaleImage = ((pred_seg == piece_of_clothes).int() * 255).numpy()
        grayscaleImage = np.array(grayscaleImage, np.uint8)
        threshValue, binaryImage = cv2.threshold(grayscaleImage, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Find the big contours/blobs on the filtered image:
        contours, hierarchy = cv2.findContours(binaryImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        # Reading an image in default mode:
        image_cv = cv2.imread(image_path)
        # Deep copies of the input image to draw results:
        # minRectImage = inputImage.copy()
        # polyRectImage = inputImage.copy()


        if hierarchy[0][0][3] == -1:
            # Get contour area:
            contourArea = cv2.contourArea(contours[0])
            # Set minimum area threshold:
            minArea = 1000
            if contourArea > minArea:
                # print('yes')
                contoursPoly = cv2.approxPolyDP(contours[0], 3, True)
                boundRect = cv2.boundingRect(contoursPoly)
                # Set the rectangle dimensions:
                rectangleX = boundRect[0]
                rectangleY = boundRect[1]
                rectangleWidth = boundRect[0] + boundRect[2]
                rectangleHeight = boundRect[1] + boundRect[3]

                # # Draw the rectangle:
                # cv2.rectangle(polyRectImage, (int(rectangleX), int(rectangleY)),
                #             (int(rectangleWidth), int(rectangleHeight)), (0, 255, 0), 2)
                # image_mask = image_cv * (((pred_seg == piece_of_clothes).int()).unsqueeze(2).numpy())
                cropped_image = image_cv[rectangleY:rectangleHeight, rectangleX:rectangleWidth] 
                # img = resize_with_padding(Image.from_numpy(croppedImg), (224, 224))
                # resized_image = resize_image(cropped_image, new_width=512, new_height=768)
                # padded_image = pad_image(resized_image, target_height, target_width)
                cv2.imwrite(str((output_dir / image_name).with_suffix('.png')), cropped_image)
                # img = np.pad(img, ((2, 2), (2, 2)), 'reflect')
                # img.save(Path('/workspace/edeyneka/2023_11_05_finetuning_style/playground/cropped_and_resized') / Path(img_path).name)
                for i in range(num_augment):
                    aug_image = augment_image(cropped_image)

                    cv2.imwrite(str((output_dir / image_name).with_suffix("")) + f'_{i}.png', aug_image)



# def padding(img, expected_size):
#     desired_size = expected_size
#     delta_width = desired_size[0] - img.size[0]
#     delta_height = desired_size[1] - img.size[1]
#     pad_width = delta_width // 2
#     pad_height = delta_height // 2
#     padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
#     return ImageOps.expand(img, padding)

def resize_image(image, new_width=None, new_height=None):

    # Get the original dimensions
    height, width = image.shape[:2]

    # Calculate the new dimensions while maintaining the aspect ratio
    if new_width is not None and new_height is not None:
        # Both new width and height are provided, use them directly
        resized_image = cv2.resize(image, (new_width, new_height))
    elif new_width is not None:
        # Resize based on the provided width, maintaining the aspect ratio
        aspect_ratio = width / height
        new_height = int(new_width / aspect_ratio)
        resized_image = cv2.resize(image, (new_width, new_height))
    elif new_height is not None:
        # Resize based on the provided height, maintaining the aspect ratio
        aspect_ratio = width / height
        new_width = int(new_height * aspect_ratio)
        resized_image = cv2.resize(image, (new_width, new_height))
    else:
        # If neither new width nor new height is provided, return the original image
        resized_image = image

    return resized_image

def pad_image(image, target_height, target_width):

    # Calculate the amount of padding needed
    pad_height = max(0, target_height - image.shape[0])
    pad_width = max(0, target_width - image.shape[1])

    # Calculate padding on each side
    pad_top = pad_height // 2
    pad_bottom = pad_height - pad_top
    pad_left = pad_width // 2
    pad_right = pad_width - pad_left

    # Pad the image with mirroring pixels
    padded_image = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), mode='reflect')

    return padded_image


def resize_with_padding(img, expected_size):
    img.thumbnail((expected_size[0], expected_size[1]))
    # print(img.size)
    delta_width = expected_size[0] - img.size[0]
    delta_height = expected_size[1] - img.size[1]
    pad_width = delta_width // 2
    pad_height = delta_height // 2
    padding = (pad_width, pad_height, delta_width - pad_width, delta_height - pad_height)
    return ImageOps.expand(img, padding)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Croping clothes')
    parser.add_argument('--data_dir', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    parser.add_argument('--item', type=str, required=True)

    args = parser.parse_args()

    crop_item(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        item=args.item,
        )