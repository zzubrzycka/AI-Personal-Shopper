from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from os_functions import move_first_images_by_date, clear_directory
from generics import OOTD_OUTPUT_PATH, OUTPUT_GENERAL, MASKS_BIN
from generics import EXAMPLE_MODEL_PATH, EXAMPLE_GARMENT_PATH


def return_final_pictures(model_path, garment_path):
    
    clear_directory(OUTPUT_GENERAL)

    run_ootd(model_path=model_path, cloth_path=garment_path, category_number="1", sample_number="1")
    print("OTTD with success")
    

    move_first_images_by_date(OOTD_OUTPUT_PATH, OUTPUT_GENERAL, 1)

if __name__ == "__main__":
    return_final_pictures(EXAMPLE_MODEL_PATH, EXAMPLE_GARMENT_PATH)