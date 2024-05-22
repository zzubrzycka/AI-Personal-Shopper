import os
from generics import RUN_PREPRO_PATH



def run_prepro(user_img_path):
    command = f"""conda run -n prepro --cwd {RUN_PREPRO_PATH} python3 run.py --user_path {user_img_path}"""
    os.system(command)



if __name__ == '__main__':
    # Define the command
    command = """conda run -n prepro --cwd /home/user/PreProcessing python3 run.py --user_path /home/user/PreProcessing/images/initial_model/w4.jpeg"""

    # Run the command using os.system()
    os.system(command)