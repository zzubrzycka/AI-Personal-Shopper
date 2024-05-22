from generics import DRESSES_PATH, BOTTOMWEAR_PATH, TOPWEAR_PATH

#category nubmers are 0 upperbody, 1 lowerbody, 2 dress
def category_number(garment_path):
    if garment_path.startswith(TOPWEAR_PATH):
        category_number = "0"
    elif garment_path.startswith(BOTTOMWEAR_PATH):
        category_number = "1"
    elif garment_path.startswith(DRESSES_PATH):
        category_number = "2"
    return category_number

