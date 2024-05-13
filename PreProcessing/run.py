import os
import image_processing
import argparse
from image_processing import removebg, centercut, white34


def main():

    # Define data directory path
    data_dir = image_processing.data_dir

    # Define paths
    parser = argparse.ArgumentParser(description="run pre-processing")
    parser.add_argument("--user_img", type=str, help="User input image name", required=True)
    args = parser.parse_args()
    input_image_name = args.user_img
    input_image_path = os.path.join(data_dir, "initial_model", input_image_name)
    input_image_png = os.path.splitext(input_image_name)[0] + ".png"
    output_bg_removed_path = os.path.join(data_dir, "stickers", input_image_png)
    output_centercut_path = os.path.join(data_dir, "cropped", input_image_png)
    input_image_jpg = os.path.splitext(input_image_name)[0] + ".jpg"
    output_white34_path = os.path.join(data_dir, "final_model", input_image_jpg)

    # Call functions from image_processing.py
    removebg(input_image_path, output_bg_removed_path)
    centercut(output_bg_removed_path, output_centercut_path)
    white34(output_centercut_path, output_white34_path)

if __name__ == "__main__":
    main()
