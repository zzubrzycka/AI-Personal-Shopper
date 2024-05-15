import csv
import numpy as np


def convert_strings_to_ints(lst):
    #it converts strings to ints when its possible
    converted_list = []

    for item in lst:
        try:
            converted_item = int(item)
            converted_list.append(converted_item)

        except ValueError:
            converted_list.append(item)

    return converted_list


def read_csv_file(file_path, encoding='utf-8'):
    rows = []
    avatars_measurements = []
    try:
        with open(file_path, mode='r', newline='', encoding=encoding) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                rows.append(row)

            for row in rows:
                avatars_measurements.append(row[0].split(';')[1:])


    except UnicodeDecodeError:
        print(f"Error: Unable to decode file with {encoding} encoding.")
    return avatars_measurements

file_path = 'avatars_measurements2.csv'
all_data = read_csv_file(file_path, encoding='ISO-8859-1')


all_vectors = []
vectors_dict = {}

for i in range(0, 10):
    first_row = all_data[0]
    second_row = all_data[1]

    person_type = f"{first_row[i]}_{second_row[i]}"
    person_type = []

    for row in all_data:
        person_type.append(row[i])

    all_vectors.append(person_type)

    person_type_key = f"{first_row[i]}_{second_row[i]}"
    converted_list = convert_strings_to_ints(person_type)
    converted_list.pop(0)
    converted_list.pop(0)

    for j in range(0,6):
        converted_list[j] = (converted_list[j] + converted_list[j+1]) / 2
        converted_list.pop(j+1)


    vectors_dict[person_type_key] = converted_list



#print(vectors_dict)

    #print(convert_strings_to_ints(all_vectors[i]))




#user input: gender, height, chest, waist, hips, inseam, weight
example_user_input = ["Man", 170, 85, 65, 87, 79, 60]

def find_nearest_size(user_input, size_dict):
    min_distance = float('inf')
    nearest_size = None

    if user_input[0] == "Woman":
        user_input.pop(0)
        del size_dict["Man_S"]
        del size_dict["Man_M"]
        del size_dict["Man_L"]
        del size_dict["Man_XXL"]


    if user_input[0] == "Man":
        user_input.pop(0)
        del size_dict["Woman_XS"]
        del size_dict["Woman_S"]
        del size_dict["Woman_M"]
        del size_dict["Woman_L"]
        del size_dict["Woman_XL"]



    for size, size_vector in size_dict.items():
      distance = np.linalg.norm(np.array(user_input) - np.array(size_vector))
      if distance < min_distance:
          min_distance = distance
          nearest_size = size

    #print(f"your nearest size is {nearest_size}")
    return nearest_size


find_nearest_size(example_user_input, vectors_dict)



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(find_nearest_size(sys.argv[1], vectors_dict))



