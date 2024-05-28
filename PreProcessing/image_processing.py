import cv2
import numpy as np
import os
# import tensorflow as tf
# import tensorflow_hub as hub
from ultralytics import YOLO
from PIL import Image
from PIL import ImageDraw
import urllib.request


def get_project_root():
    return os.path.dirname(os.path.dirname(__file__))

# Define data directory path
data_dir = os.path.join(get_project_root(), "PreProcessing/images")


'''
def superresolution_image(image_path, model_url, output_path):
    # Load the original image
    img = cv2.imread(image_path)
    image_plot = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Load the super-resolution model
    model = hub.load(model_url)

    # Function to preprocess images
    def preprocessing(img):
        imageSize = (tf.convert_to_tensor(image_plot.shape[:-1]) // 4) * 4
        cropped_image = tf.image.crop_to_bounding_box(
            img, 0, 0, imageSize[0], imageSize[1])
        preprocessed_image = tf.cast(cropped_image, tf.float32)
        return tf.expand_dims(preprocessed_image, 0)

    # Function to apply super resolution
    def apply_superresolution(img):
        preprocessed_image = preprocessing(img)  # Preprocess the image
        new_image = model(preprocessed_image)  # Run the super resolution model
        return tf.squeeze(new_image) / 255.0

    # Apply super resolution to image
    hr_image = apply_superresolution(image_plot)

    # Save super resolved image
    cv2.imwrite(output_path, cv2.cvtColor(hr_image.numpy() * 255, cv2.COLOR_RGB2BGR))
    print("Imagen superresuelta guardada en:", output_path)
'''


## Instance segmentation and then paste it onto white bg 3:4
def masks(image_path, output_path):
  try:
    # Use the model
    model = YOLO("yolov8m-seg.pt")
    results = model.predict(image_path)
    result = results[0]
    masks = result.masks
    len(masks)
    mask1 = masks[0]
    mask = mask1.data[0].cpu().numpy()
    polygon = mask1.xy[0]

    mask_img = Image.fromarray(mask,"I")
    mask_img.save(output_path)

  except Exception as e:
    # Handle any unexpected errors
    print(f"No person detected: {e}")


def segmentation(image_path, masks_path, output_path):
  try:
    # Load the original image and the person's mask
    img = Image.open(image_path)
    mask_img1 = Image.open(masks_path)

    # Resize the mask so that it has the same dimensions as the original image
    mask_img1 = mask_img1.resize(img.size)

    # Calculate the bounding rectangle of the person in the mask
    bbox = mask_img1.getbbox()

    if bbox is not None:
        # Calculate the dimensions of the detected person
        person_width = bbox[2] - bbox[0]
        person_height = bbox[3] - bbox[1]

        # Calculate the dimensions of the white background image in a 3:4 ratio with respect to the person
        bg_width = int(person_height* 3 / 4)
        bg_height = person_height

        # Calculate the offset needed to center the person in the white background image
        offset_x = int((bg_width - person_width) // 2)
        offset_y = int((bg_height - person_height) // 2)

        # Create a new RGB image to store the cropped person
        person_img = Image.new("RGB", (bg_width, bg_height), (255, 255, 255))  # Initialize with white background

        # Combine original image with transparency mask
        for x in range(img.width):
            for y in range(img.height):
                pixel_value = mask_img1.getpixel((x, y))
                if pixel_value >= 128:  # If the pixel corresponds to the person
                    new_x = x - bbox[0] + offset_x
                    new_y = y - bbox[1] + offset_y
                    if 0 <= new_x < bg_width and 0 <= new_y < bg_height:
                        person_img.putpixel((new_x, new_y), img.getpixel((x, y)))  # Keep the original color

        # Save final result
        person_img.save(output_path)
    else:
        print("WARNING! No person was detected in the mask.")

  except Exception as e:
        # Handle any unexpected errors
        print(f"No person detected: {e}")