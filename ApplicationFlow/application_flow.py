from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from os_functions import move_first_images_by_date, move_first_images_by_date_ootd, clear_directory, find_image_path
from category_number import category_number

from generics import OOTD_OUTPUT_PATH, OUTPUT_GENERAL, PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH
from generics import EXAMPLE_MODEL_PATH, EXAMPLE_GARMENT_PATH, EXAMPLE_MODEL_PATH2_topwear, EXAMPLE_PREPRO_MODEL


def return_final_pictures(model_path, garment_path):
    

    #WITH GUI UNCOMMENT THE CODE BELOW!
    model_path = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/" + model_path
    # garment_path = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/" + garment_path

    clear_directory(OUTPUT_GENERAL)
    clear_directory(OOTD_INPUT_MODEL_PATH)

    run_prepro(model_path)
    print("PREPRO finished working")

    move_first_images_by_date(PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH, 1)

    ootd_input_model_path = find_image_path(OOTD_INPUT_MODEL_PATH)

    numb_cat = category_number(garment_path)
    print(f"Category number of cloth: {numb_cat}")

    run_ootd(model_path=ootd_input_model_path, cloth_path=garment_path, category_number=numb_cat, sample_number="1")
    print("OTTD finished work")

    move_first_images_by_date_ootd(OOTD_OUTPUT_PATH, OUTPUT_GENERAL, 1)

    # output_path = find_image_path(OUTPUT_GENERAL)
    # print(f"Path of the image: {output_path}")
    # return output_path

    return OUTPUT_GENERAL + "/out_dc_0.jpg"


def return_final_pictures_avatar(model_path, garment_path):

    #WITH GUI UNCOMMENT THE CODE BELOW!
    model_path = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/" + model_path
    # garment_path = "/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/" + garment_path

    clear_directory(OUTPUT_GENERAL)
    # clear_directory(OOTD_INPUT_MODEL_PATH)

    # run_prepro(model_path)
    # print("PREPRO finished working")

    # move_first_images_by_date(PREPRO_OUTPUT_PATH, OOTD_INPUT_MODEL_PATH, 1)

    # ootd_input_model_path = find_image_path(OOTD_INPUT_MODEL_PATH)

    ootd_input_model_path = model_path

    numb_cat = category_number(garment_path)
    print(f"Category number of cloth: {numb_cat}")

    run_ootd(model_path=ootd_input_model_path, cloth_path=garment_path, category_number=numb_cat, sample_number="1")
    print("OTTD finished work")

    move_first_images_by_date_ootd(OOTD_OUTPUT_PATH, OUTPUT_GENERAL, 1)

    # output_path = find_image_path(OUTPUT_GENERAL)
    # print(f"Path of the image: {output_path}")
    # return output_path

    return OUTPUT_GENERAL + "/out_dc_0.jpg"


if __name__ == "__main__":
    return_final_pictures(EXAMPLE_PREPRO_MODEL, EXAMPLE_MODEL_PATH2_topwear)