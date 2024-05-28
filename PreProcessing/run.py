import os
import image_processing
import argparse
from image_processing import masks, segmentation


def main():

    # Define data directory path
    data_dir = image_processing.data_dir

    # Define paths
    parser = argparse.ArgumentParser(description="run pre-processing")
    parser.add_argument("--user_path", type=str, help="User input image path (file extension included)", required=True)
    args = parser.parse_args()
    # Input image and path
    input_image_path = args.user_path
    input_image_name = os.path.splitext(os.path.basename(input_image_path))[0]
    # Input image path converted to PNG
    input_image_png = input_image_name + ".png"
    # Mask image, saved in 'masks' folder
    mask_path = os.path.join(data_dir, "masks", input_image_png)
    # Final segmented image, converted to JPG, saved in 'final_model' folder
    final_image_jpg = os.path.splitext(input_image_png)[0] + ".jpg"
    final_image_path = os.path.join(data_dir, "final_model", final_image_jpg)

    # Call functions from image_processing.py
    masks(input_image_path, mask_path)
    segmentation(input_image_path, mask_path, final_image_path)

if __name__ == "__main__":
    main()
