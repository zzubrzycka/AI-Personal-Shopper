import time
import os
from tqdm import tqdm
from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from os_functions import move_first_images_by_date, move_first_images_by_date_ootd, clear_directory, find_image_path, copy_picture
from category_number import category_number

from generics import OOTD_OUTPUT_PATH, OUTPUT_TEST, PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH_TEST, ALL_OUTPUT_TEST, ALL_PREPRO_OUTPUT
from generics import EXAMPLE_MODEL_PATH, EXAMPLE_GARMENT_PATH, EXAMPLE_MODEL_PATH2_topwear, EXAMPLE_PREPRO_MODEL


def return_final_pictures_test(model_path, garment_path, new_name=None):

    clear_directory(OUTPUT_TEST)
    clear_directory(OOTD_INPUT_MODEL_PATH_TEST)

    start_time_prepro = time.time()
    run_prepro(model_path)
    end_time_prepro = time.time()
    time_prepro = end_time_prepro - start_time_prepro
    print(f"PREPRO finished working in {time_prepro} seconds")
    

    move_first_images_by_date(PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH_TEST, 1)
    copy_picture(OOTD_INPUT_MODEL_PATH_TEST, ALL_PREPRO_OUTPUT, new_name+"_prepro")

    ootd_input_model_path = find_image_path(OOTD_INPUT_MODEL_PATH_TEST)

    numb_cat = category_number(garment_path)
    print(f"Category number of cloth: {numb_cat}")

    start_time_ootd = time.time()
    run_ootd(model_path=ootd_input_model_path, cloth_path=garment_path, category_number=numb_cat, sample_number="1")
    end_time_ootd = time.time()
    time_ootd = end_time_ootd - start_time_ootd
    print(f"OOTD finished working in {time_ootd} seconds")

    move_first_images_by_date_ootd(OOTD_OUTPUT_PATH, OUTPUT_TEST, 1) #OUTPUT_TEST + "/out_dc_0.png" path of the final pic
    copy_picture(OUTPUT_TEST+"/out_dc_0.png", ALL_OUTPUT_TEST, new_name)
     

    return time_prepro, time_ootd


def get_color(progress):
    if progress < 0.33:
        return '\033[91m'  # Red
    elif progress < 0.66:
        return '\033[93m'  # Yellow
    else:
        return '\033[92m'  # Green

def test_multiple_pictures(model_folder, garment_folder, output_file):
    results = []

    model_files = [os.path.join(model_folder, f) for f in os.listdir(model_folder) if os.path.isfile(os.path.join(model_folder, f))]
    garment_files = [os.path.join(garment_folder, f) for f in os.listdir(garment_folder) if os.path.isfile(os.path.join(garment_folder, f))]

    total_iterations = len(model_files) * len(garment_files)

    with tqdm(total=total_iterations, bar_format='{l_bar}{bar:30}{r_bar}{bar:-30b}') as pbar:
        for i, model_path in enumerate(model_files):
            for j, garment_path in enumerate(garment_files):
                model_name = os.path.basename(model_path)
                garment_name = os.path.basename(garment_path)
                new_name = f"{model_name}_{garment_name}"

                pbar.set_description(f"Processing model: {model_name} with garment: {garment_name}")

                time_prepro, time_ootd = return_final_pictures_test(model_path, garment_path, new_name)
                results.append((model_name, garment_name, time_prepro, time_ootd))

                with open(output_file, 'a') as f:
                    f.write(f"{model_name}, {garment_name}, {time_prepro}, {time_ootd}\n")

                progress = (i * len(garment_files) + j + 1) / total_iterations
                color = get_color(progress)
                pbar.bar_format = f'{color}{{l_bar}}{{bar:30}}{{r_bar}}{{bar:-30b}}\033[0m'
                pbar.update(1)

    return results

if __name__ == "__main__":
    model_folder = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/test/test_model_pics/GoodModels"
    garment_folder = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/garment_database/topwear/test_topwear/ShirtTest"
    output_file = "shirts_and_goodmodels.csv"
    
    test_multiple_pictures(model_folder, garment_folder, output_file)
