import csv


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

    vectors_dict[person_type_key] = converted_list



print(vectors_dict)

    #print(convert_strings_to_ints(all_vectors[i]))




#user input: gender, height, chest, waist, hips, inseam, weight
example_user_input = ['Women', 170, 85, 65, 87, 79, 60]



