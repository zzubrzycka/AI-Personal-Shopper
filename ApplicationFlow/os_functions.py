import os
import shutil
from datetime import datetime



def get_creation_date_of_first_image(folder_path):
    """
    Get the creation date of the first image in a folder.
    
    Args:
    folder_path (str): The path to the folder containing the images.
    
    Returns:
    datetime: The creation date of the first image found.
    """
    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        
        # Filter out image files (you can adjust this based on the image file extensions you have)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        
        if not image_files:
            print("No image files found in the folder.")
            return None
        
        # Get the creation time of the first image file
        first_image_path = os.path.join(folder_path, image_files[0])
        creation_time = os.path.getctime(first_image_path)
        
        # Convert creation timestamp to a datetime object
        creation_date = datetime.fromtimestamp(creation_time)
        
        return creation_date
    except FileNotFoundError:
        print("Folder not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage:
# Assuming you have a folder named "images" containing image files
# folder_path = "images"
# creation_date = get_creation_date_of_first_image(folder_path)
# print("Creation date of the first image:", creation_date)


def move_first_images_by_date(start_path, end_path, n_images):
    """
    Move between folders the first n images of a folder, sorted by date created.
    
    Args:
    start_path (str): The path to the folder containing the images.
    end_path (str): The path to the destination folder.
    n_images (int): Number of images to be moved.

    """
    try:
        # Get a list of all files in the folder
        files = os.listdir(start_path)
        
        # Filter out image files (you can adjust this based on the image file extensions you have)
        image_files = [file for file in files if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')))]
        

        if not image_files:
            print("No image files found in the folder.")
            return None
        
        # Sort image files by creation date (newest first)
        image_files.sort(key=lambda x: os.path.getctime(os.path.join(start_path, x)), reverse=True)
        
        # Move the first N images to the destination directory
        for i in range(min(n_images, len(image_files))):
            image_name = image_files[i]
            source_path = os.path.join(start_path, image_name)
            dest_path = os.path.join(end_path, image_name)
            shutil.move(source_path, dest_path)
        
    except FileNotFoundError:
        print("Folder not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def move_first_images_by_date_ootd(start_path, end_path, n_images):
    """
    Move between folders the first n images of a folder, sorted by date created.
    
    Args:
    start_path (str): The path to the folder containing the images.
    end_path (str): The path to the destination folder.
    n_images (int): Number of images to be moved.

    """
    try:
        # Get a list of all files in the folder
        files = os.listdir(start_path)
        
        # Filter out image files (you can adjust this based on the image file extensions you have)
        image_files = [file for file in files if (file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')) and file.lower().startswith('out'))]
        

        if not image_files:
            print("No image files found in the folder.")
            return None
        
        # Sort image files by creation date (newest first)
        image_files.sort(key=lambda x: os.path.getctime(os.path.join(start_path, x)), reverse=True)
        
        # Move the first N images to the destination directory
        for i in range(min(n_images, len(image_files))):
            image_name = image_files[i]
            source_path = os.path.join(start_path, image_name)
            dest_path = os.path.join(end_path, image_name)
            shutil.move(source_path, dest_path)
        
    except FileNotFoundError:
        print("Folder not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None


def clear_directory(path):
    """
    Clear the contents of the directory specified by the path.
    
    Args:
    path (str): The path to the directory to be cleared.
    
    Returns:
    bool: True if the directory was successfully cleared, False otherwise.
    """
    if not os.path.isdir(path):
        print(f"The path {path} is not a directory or just doesn't exist")
        return False
    
    try:
        # Iterate over all the items in the directory and remove them
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove the directory and all its contents
            else:
                os.remove(item_path)  # Remove the file
        
        print(f"The directory {path} has been cleared.")
        return True
    except Exception as e:
        print(f"An error occurred while clearing the directory: {e}")
        return False
    
def print_current_environment():
    # Get the value of the CONDA_DEFAULT_ENV environment variable
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    
    if conda_env:
        print("Current Conda environment:", conda_env)
    else:
        print("No Conda environment activated.")


def find_image_path(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter out only JPG files
    jpg_files = [f for f in files if f.lower().endswith('.jpg')]
    
    if len(jpg_files) == 0:
        print("No JPG files found in the directory.")
        return None
    elif len(jpg_files) > 1:
        print("More than one JPG file found in the directory. Returning the first one.")
    
    # Construct the full path to the JPG file
    jpg_path = os.path.join(directory, jpg_files[0])
    return jpg_path


# Example usage
if __name__ == "__main__":
    directory_path = R"C:\\sy\\semestr6\\PAESAV\\"
    jpg_path = find_image_path(directory_path)
    if jpg_path:
        print("Path to the JPG file:", jpg_path)



if __name__ == '__main__':
    print(f"fresh pic: {get_creation_date_of_first_image(R'//home//user//OOTDiffusion//run//images_output')}")