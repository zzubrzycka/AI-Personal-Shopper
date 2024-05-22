from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from os_functions import move_first_images_by_date, clear_directory, find_image_path
from category_number import category_number

from generics import OOTD_OUTPUT_PATH, OUTPUT_GENERAL, MASKS_BIN
from generics import EXAMPLE_MODEL_PATH, EXAMPLE_GARMENT_PATH, EXAMPLE_MODEL_PATH2_topwear


def return_final_pictures(model_path, garment_path):
    clear_directory(OUTPUT_GENERAL)

    numb_cat = category_number(garment_path)

    # run_prepro(model_path)

    print(f"Category number of cloth: {numb_cat}")

    run_ootd(model_path=model_path, cloth_path=garment_path, category_number=numb_cat, sample_number="1")
    print("OTTD with success")
    

    move_first_images_by_date(OOTD_OUTPUT_PATH, OUTPUT_GENERAL, 1)

    # output_path = find_image_path(OUTPUT_GENERAL)
    # print(f"Path of the image: {output_path}")
    # return output_path
    print()
    return OUTPUT_GENERAL + "/out_dc_0.jpg"


if __name__ == "__main__":
    return_final_pictures(EXAMPLE_MODEL_PATH, EXAMPLE_MODEL_PATH2_topwear)