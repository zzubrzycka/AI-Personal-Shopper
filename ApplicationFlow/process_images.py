from PIL import Image
import os

def blend_images(image_path1, image_path2):
    # Open the images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Resize second image to match the first
    image2 = image2.resize(image1.size)

    # Blend images
    blended_image = Image.blend(image1, image2, alpha=0.5)
    return blended_image

def apply_sepia_tone(image):
    # Convert image to grayscale
    gray = image.convert('L')
    # Apply a sepia tone by adding red and green channels
    sepia = gray.copy().convert('RGB')
    sepia_data = sepia.getdata()
    sepia_data = [
        (int(r * 0.9), int(g * 0.6), int(b * 0.3)) for r, g, b in sepia_data
    ]
    sepia.putdata(sepia_data)
    return sepia

def process(image_path1, image_path2):
    blended = blend_images(image_path1, image_path2)
    sepia = apply_sepia_tone(blended)

    # Define the directory to save the image
    save_directory = "output_images"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Construct a unique filename based on the input filenames
    base_name1 = os.path.splitext(os.path.basename(image_path1))[0]
    base_name2 = os.path.splitext(os.path.basename(image_path2))[0]
    output_filename = f"{base_name1}_{base_name2}.png"
    output_path = os.path.join(save_directory, output_filename)

    # Save the image to the specified directory
    sepia.save(output_path, "PNG")

    # Return the path to the saved image
    return output_path

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        print(process(sys.argv[1], sys.argv[2]))
