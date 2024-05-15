import os
from os_functions import get_creation_date_of_first_image
from generics import RUN_OOTD_PATH

# Define the command


def run_ootd(model_path, cloth_path, sample_number, category_number): #category nubmers are 0 upperbody, 1 lowerbody, 2 dress
    command = f"conda run -n ootd --cwd {RUN_OOTD_PATH} python run_ootd.py --model_path {model_path} --cloth_path {cloth_path} --model_type dc --category {category_number} --scale 2.0 --sample {sample_number}"
    os.system(command)


if __name__ == '__main__':
    command = "conda run -n ootd --cwd /home/user/OOTDiffusion/run python run_ootd.py --model_path /home/user/OOTDiffusion/run/examples/model/051962_0.jpg --cloth_path /home/user/OOTDiffusion/run/examples/garment/051517_1.jpg --model_type dc --category 1 --scale 2.0 --sample 1"
    
    # Run the command using os.system()
    os.system(command)

    print(f"fresh pic: {get_creation_date_of_first_image(R'//home//user//OOTDiffusion//run//images_output')}")