import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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

def delete_image(entry):
    image_labels[entry].config(image='', text=frame_texts[entry])  # Reset text
    image_labels[entry].image = None
    image_paths[entry] = None
    delete_buttons[entry].config(state=tk.DISABLED)  # Disable the delete button

def run_script():
    # Assuming 'process_images.py' is your script and it takes two image paths
    import process_images
    process_images.process(image_paths[0], image_paths[1])

# Create the main window
root = tk.Tk()
root.title("Image Input GUI")

image_paths = [None, None]
frame_texts = ["Add your picture here", "Add your garment here"]

# Create frames for image selectors
frames = [tk.Frame(root, bd=2, relief="solid", padx=10, pady=10) for _ in range(2)]
image_labels = [tk.Label(frame, text=frame_texts[i], font=('Arial', 12)) for i, frame in enumerate(frames)]
delete_buttons = []

for i, frame in enumerate(frames):
    frame.grid(row=0, column=i, padx=20, pady=20)
    image_labels[i].pack(fill='both', expand=True)
    image_labels[i].bind("<Button-1>", lambda event, idx=i: load_image(idx))  # Bind click event to the label
    # Creating delete buttons beneath the frames
    delete_button = tk.Button(root, text="Delete", command=lambda idx=i: delete_image(idx), state=tk.DISABLED)
    delete_button.grid(row=1, column=i, pady=5)
    delete_buttons.append(delete_button)

# Create a process button
process_button = tk.Button(root, text="Run Script", command=run_script)
process_button.grid(row=2, column=0, columnspan=2, pady=20)

# Run the GUI
root.mainloop()
