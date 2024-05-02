import tkinter as tk
from tkinter import filedialog, ttk, simpledialog
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *


def load_image(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        img = Image.open(file_path)
        img.thumbnail((200, 200))  # Resize the image to fit into the GUI
        img = ImageTk.PhotoImage(img)
        image_labels[entry].config(image=img, text='')  # Remove text when image is loaded
        image_labels[entry].image = img  # Keep a reference to avoid garbage collection
        image_paths[entry] = file_path
        delete_buttons[entry].config(state=tk.NORMAL)  # Enable the delete button

        # Add loaded image to input_img_tab
        img_input = Image.open(file_path)
        img_input.thumbnail((200, 200))
        img_input = ImageTk.PhotoImage(img_input)
        input_labels[entry].config(image=img_input)
        input_labels[entry].image = img_input


def delete_image(entry):
    image_labels[entry].config(image='', text=frame_texts[entry])  # Reset text
    image_labels[entry].image = None
    image_paths[entry] = None
    delete_buttons[entry].config(state=tk.DISABLED)  # Disable the delete button


def run_script():
    # Assuming 'process_images.py' is your script and it takes two image paths
    import process_images
    process_images.process(image_paths[0], image_paths[1])


def choose_image_source(idx):

    newWindow = Toplevel(root)
    newWindow.title("Choose Type of Image")
    newWindow.geometry("300x150")
    Label(newWindow, text="Do you want to use an Avatar or your own picture?").pack()
    avatar_button = Button(newWindow, text="Avatar", command=lambda: select_own_image(idx))

    #WRITE THE FUNCTION TO SELECT AVATARS

    avatar_button.pack(pady=10)
    own_pic_button = Button(newWindow, text="My own picture", command=lambda: select_own_image(idx))
    own_pic_button.pack(pady=10)

def select_own_image(idx):
    response = tk.messagebox.askyesno("Choose Image Source", "Do you want to use a previously uploaded image?")
    if response:
            # Load existing image
        print("user chose their own picture")

    else:
            # Open file dialog to upload a new image
            load_image(idx)


# Create the main window
root = tk.Tk()
root.title("Image Input GUI")

image_paths = [None, None]
frame_texts = ["Add your picture here", "Add your garment here"]

tab_control = ttk.Notebook(root)
main_tab = ttk.Frame(tab_control)
input_img_tab = ttk.Frame(tab_control)
avatars_tab = ttk.Frame(tab_control)
clothes_tab = ttk.Frame(tab_control)
output_img_tab = ttk.Frame(tab_control)

tab_control.add(main_tab, text="Virtual try-on")
tab_control.add(input_img_tab, text="Input images")
tab_control.add(avatars_tab, text="Avatars")
tab_control.add(clothes_tab, text="Clothes to try on")
tab_control.add(output_img_tab, text="Output images")

tab_control.pack(expand=1, fill='both')

# Create frames for image selectors
frames = [tk.Frame(main_tab, bd=2, relief="solid", padx=10, pady=10) for _ in range(2)]
image_labels = [tk.Label(frame, text=frame_texts[i], font=('Arial', 12)) for i, frame in enumerate(frames)]
delete_buttons = []

input_frames = [tk.Frame(input_img_tab, bd=2, relief="solid", padx=10, pady=10) for _ in range(2)]
input_labels = [tk.Label(frame, text=frame_texts[i], font=('Arial', 12)) for i, frame in enumerate(input_frames)]

for i, frame in enumerate(frames):
    frame.grid(row=0, column=i, padx=20, pady=20)
    image_labels[i].pack(fill='both', expand=True)
    image_labels[i].bind("<Button-1>", lambda event, idx=i: choose_image_source(idx))  # Bind click event to the label
    # Creating delete buttons beneath the frames
    delete_button = tk.Button(main_tab, text="Delete", command=lambda idx=i: delete_image(idx), state=tk.DISABLED)
    delete_button.grid(row=1, column=i, pady=5)
    delete_buttons.append(delete_button)

for i, frame in enumerate(input_frames):
    frame.grid(row=0, column=i, padx=20, pady=20)
    input_labels[i].pack(fill='both', expand=True)

# Create a process button
process_button = tk.Button(root, text="Run Script", command=run_script)
process_button.pack(pady=20)

# Run the GUI
root.mainloop()
