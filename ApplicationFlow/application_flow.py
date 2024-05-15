from run_prepro_flow import run_prepro
from run_ootd_flow import run_ootd
from move_images import move_first_images_by_date


def return_final_pictures(model_path, garment_path):
    
    run_ootd(model_path=model_path, cloth_path=garment_path, category_number=1)
    
    move_first_images_by_date()