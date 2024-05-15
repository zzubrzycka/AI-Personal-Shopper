import os
import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
import urllib.request
from ultralytics import YOLO


def get_project_root():
    return os.path.dirname(os.path.dirname(__file__))

# Define data directory path
data_dir = os.path.join(get_project_root(), "PreProcessing/images")


def masks(image_path, output_path):
    # Use the model
    model = YOLO("yolov8m-seg.pt")
    results = model.predict(image_path)
    result = results[0]
    masks = result.masks
    len(masks)
    mask1 = masks[0]
    mask = mask1.data[0].numpy()
    polygon = mask1.xy[0]

    mask_img = Image.fromarray(mask,"I")
    mask_img.save(output_path)


# Remove background function (output has to be .png to support transparency)
def removebg(image_path, output_path):
    # Define input image
    input_image = Image.open(image_path)

    # Convert the input image to a numpy array
    input_array = np.array(input_image)

    # Remove background
    output_array = rembg.remove(input_array)

    # Convert numpy array back to image
    output_image = Image.fromarray(output_array)

    # Save output image
    output_image.save(output_path)

    # Close all OpenCV windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()



# Obtaining the center of the previous image
def centercut(image_path, output_path):
    # Load YOLO model
    net = download_yolo_model(weights_url, cfg_url, weights_path, cfg_path)

    # Define input image
    image = cv2.imread(image_path)

    # Get image dimensions
    (height, width) = image.shape[:2]

    # Define the neural network input
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Perform forward propagation
    output_layer_name = net.getUnconnectedOutLayersNames()
    output_layers = net.forward(output_layer_name)
    expansion_factor = 1.2

    # Initialize list of detected people
    people = []

    # Loop over the output layers
    for output in output_layers:
        # Loop over the detections
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Only keep detections with a high confidence
            if class_id == 0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Expand the bounding box by a certain factor
                expanded_x = max(0, x - int((expansion_factor - 1) * w / 2))
                expanded_y = max(0, y - int((expansion_factor - 1) * h / 2))
                expanded_w = min(width - expanded_x, int(expansion_factor * w))
                expanded_h = min(height - expanded_y, int(expansion_factor * h))

                # Add the detection to the list of people
                people.append((expanded_x, expanded_y, expanded_w, expanded_h))

    # If no people detected, return original image
    if not people:
        print("No people detected.")
        return

    # Find the bounding box of the person with the largest area
    (x, y, w, h) = max(people, key=lambda box: box[2] * box[3])

    # Crop the image
    cropped_image = image[y:y+h, x:x+w].copy()

    # The next lines are to maintain transparency in the output picture
    # Open the input image using Pillow to get the alpha channel
    input_image = Image.open(image_path)
    # Extract the alpha channel
    alpha_channel = np.array(input_image.split()[-1])
    # Create the cropped image with alpha channel
    cropped_image_with_alpha = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2BGRA)
    # Set the alpha channel of the cropped image
    cropped_image_with_alpha[:, :, 3] = alpha_channel[y:y+h, x:x+w]

    # Save the result
    cv2.imwrite(output_path, cropped_image_with_alpha)



# Pasting the png "sticker" to a 3:4 aspect ratio background
def white34(image_path, output_path):
    # Load the PNG image with alpha channel (transparency)
    foreground = Image.open(image_path)

    # Create a new white background image with a 3:4 aspect ratio
    new_width = foreground.height * 3 // 4
    background = Image.new("RGB", (new_width, foreground.height), "white")

    # Calculate the position to center the PNG image
    x_offset = (new_width - foreground.width) // 2

    # Paste the PNG image onto the white background
    background.paste(foreground, (x_offset, 0), foreground)

    # Save the resulting image
    background.save(output_path)