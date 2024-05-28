import time
import os
from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from os_functions import move_first_images_by_date, move_first_images_by_date_ootd, clear_directory, find_image_path, copy_picture
from category_number import category_number

from generics import OOTD_OUTPUT_PATH, OUTPUT_TEST, PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH_TEST, ALL_OUTPUT_TEST
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


def test_multiple_pictures(model_folder, garment_folder, output_file):
    results = []

    model_files = [os.path.join(model_folder, f) for f in os.listdir(model_folder) if os.path.isfile(os.path.join(model_folder, f))]
    garment_files = [os.path.join(garment_folder, f) for f in os.listdir(garment_folder) if os.path.isfile(os.path.join(garment_folder, f))]

    for model_path in model_files:
        for garment_path in garment_files:
            model_name = os.path.basename(model_path)
            garment_name = os.path.basename(garment_path)
            new_name = f"{model_name}_{garment_name}"
            
            print(f"Processing model: {model_name} with garment: {garment_name}")
            
            time_prepro, time_ootd = return_final_pictures_test(model_path, garment_path, new_name)
            results.append((model_name, garment_name, time_prepro, time_ootd))
            
            with open(output_file, 'a') as f:
                f.write(f"{model_name}, {garment_name}, {time_prepro}, {time_ootd}\n")

    return results

if __name__ == "__main__":
    model_folder = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/test/test_model_pics"
    garment_folder = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/garment_database/topwear/test_topwear"
    output_file = "time_measurements.csv"
    
    test_multiple_pictures(model_folder, garment_folder, output_file)
