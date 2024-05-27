import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFileDialog, QDialog, QMessageBox, QGridLayout, QComboBox, QLineEdit, QFormLayout)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window properties
        self.setWindowTitle("AI Personal Shopper")
        self.setGeometry(100, 100, 1250, 600)
        self.setStyleSheet("background-color: #f5f6f1;")  # Soft gray background

        # Initialize main content widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.setup_main_layout()

        # Ensure directories exist
        self.input_dir = "input_images"
        self.user_input_image_dir = "user_input_image"
        self.garment_input_image_dir = "garment_input_image"
        self.output_dir = "output_images"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def setup_main_layout(self):
        # Create a layout to separate left and right sections
        main_layout = QHBoxLayout(self.main_widget)

        # Left side: title and picture
        vertical_layout1 = QVBoxLayout()
        
        # Load and display the guide image
        guide_image = QLabel()
        guide_image_path = "guide.png"
        pixmap = QPixmap(guide_image_path)
        if pixmap.isNull():
            print("Failed to load guide image.")
        else:
            guide_image.setPixmap(pixmap.scaled(675, 900, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        vertical_layout1.addWidget(guide_image)

        # Right side: image loading and button for image upload
        images_layout = QVBoxLayout()
        self.setup_image_upload_section(images_layout, 1, "Upload a picture of yourself")
        self.setup_image_upload_section(images_layout, 2, "Upload the picture of the clothing")

        # "Run script" button to process the images
        self.run_script_button = QPushButton("Try it on!")
        self.run_script_button.setStyleSheet(
            "QPushButton {"
            "background-color: #4CAF50;"
            "color: white;"
            "border-radius: 10px;"
            "font-size: 18px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #45a049;"
            "}"
        )
        self.run_script_button.setMinimumHeight(50)
        self.run_script_button.clicked.connect(self.process_images)
        images_layout.addWidget(self.run_script_button, alignment=Qt.AlignHCenter)

        # Organize layouts
        main_layout.addLayout(vertical_layout1)
        main_layout.addLayout(images_layout)

    def setup_image_upload_section(self, layout, index, text):
        button = QPushButton(text)
        button.setStyleSheet(
            "QPushButton {"
            "font-size: 16px;"
            "background-color: #ec98b8;"  
            "color: black;"
            "border-radius: 5px;"
            "padding: 12px;"
            "margin: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #f7b3cc;"
            "}"
        )
        button.setMinimumWidth(300)
        button.setMinimumHeight(50)
        label = QLabel("No Image Loaded")
        label.setAlignment(Qt.AlignCenter)
        label.setFixedSize(250, 250)
        label.setStyleSheet("border: 1px solid #ccc;")
        layout.addWidget(button, alignment=Qt.AlignHCenter)
        layout.addWidget(label, alignment=Qt.AlignHCenter)

        # Ensure the lambda captures the index and passes it to the function
        button.clicked.connect(lambda: self.open_popup(index))

        if index == 1:
            self.image_label_1 = label
        else:
            self.image_label_2 = label



    def open_popup(self, index):
        popup = PopupDialog(self, index)
        popup.accepted.connect(popup.close)
        popup.exec_()

    def closePopup(self):

        self.sender().close()

    def setup_avatar_tab_EARLIER(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Avatars:"))

        # Add placeholder avatars
        self.avatar_images = [QLabel(f"Avatar {i}") for i in range(1, 11)]
        for label in self.avatar_images:
            label.setPixmap(QPixmap('placeholder.png').scaled(100, 100))
            layout.addWidget(label)

        self.avatar_tab.setLayout(layout)

    def setup_uploaded_images_tab(self):
        # Initialize a layout to hold multiple uploaded images
        self.uploaded_images_layout = QVBoxLayout()
        self.uploaded_images_tab.setLayout(self.uploaded_images_layout)

    def setup_output_images_tab(self):
        # Initialize a layout to hold multiple output images
        self.output_images_layout = QVBoxLayout()
        self.output_images_tab.setLayout(self.output_images_layout)



    def upload_image(self, index):
        image_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if image_path:
            image_name = os.path.basename(image_path)

            if index == 1:
                target_dir = self.user_input_image_dir
            else:
                target_dir = self.garment_input_image_dir
            
            target_path = os.path.join(target_dir, image_name)

            try:
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir, exist_ok=True)
                    print(f"Directory created: {target_dir}")
                
                shutil.copy(image_path, target_path)
                print(f"File copied to {target_path}")
                
                self.set_image_label(index, target_path)

            except Exception as e:
                QMessageBox.critical(self, "File Copy Error", f"An error occurred while copying file: {str(e)}")
                print(f"Error copying file: {e}")


    def upload_avatar(self, index, avatar_path):
        print("jestesmy w funkcji upload avatar")
        image_path = avatar_path
        if image_path:
            image_name = os.path.basename(image_path)
            print("sciezka jest dobra")
        else:
            print("cos nie tak ze sciezka")

        if index == 1:
            print("mamy index=1")
            target_path2 = os.path.join(self.user_input_image_dir, image_name)
            print(target_path2)

            for item in os.listdir(self.user_input_image_dir):
                item_path = os.path.join(self.user_input_image_dir, item)
                os.remove(item_path)

            # shutil.rmtree(self.user_input_image_dir)
            shutil.copy(image_path, target_path2)

        if index == 2:
            target_path2 = os.path.join(self.garment_input_image_dir, image_name)
            print(target_path2)
            # shutil.rmtree(self.garment_input_image_dir)

            for item in os.listdir(self.garment_input_image_dir):
                item_path = os.path.join(self.garment_input_image_dir, item)
                os.remove(item_path)

            shutil.copy(image_path, target_path2)

            # Copy the image to the input_images directory
        print("pora na zapisanie obrazka do folderu")
        target_path = os.path.join(self.input_dir, image_name)
        shutil.copy(image_path, target_path)
        self.set_image_label(index, target_path)

        # Add the uploaded image to the "User Images" tab
        user_image_label = QLabel()
        user_image_label.setPixmap(QPixmap(target_path).scaled(100, 100, Qt.KeepAspectRatio))
        self.uploaded_images_layout.addWidget(user_image_label)


    def set_image_label(self, index, image_path):
        # Ensure the loaded image is displayed directly below the corresponding button
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
        if index == 1:
            self.image_label_1.setPixmap(pixmap)
            self.image_1_path = image_path
        elif index == 2:
            self.image_label_2.setPixmap(pixmap)
            self.image_2_path = image_path

    def process_images(self):
        # Ensure that both images are loaded before processing
        if self.image_1_path is None or self.image_2_path is None:
            QMessageBox.warning(self, "Missing Images", "Please load both images before running the script.")
            return

        # Extract file names without extensions
        name1 = os.path.splitext(os.path.basename(self.image_1_path))[0]
        name2 = os.path.splitext(os.path.basename(self.image_2_path))[0]
        output_image_name = f"{name1}_{name2}.png"
        output_image_path = os.path.join(self.output_dir, output_image_name)


        # Execute the process_images.py script and save output to the output_images folder
      #  try:
      #      subprocess.run(
       #         ["python", "process_images.py", self.image_1_path, self.image_2_path, output_image_path],
        #        check=True
         #   )
        try:
            output_path_from_script = return_final_pictures(self.image_1_path, self.image_2_path)
            pixmap = QPixmap(output_path_from_script).scaled(300, 400, Qt.KeepAspectRatio)
            self.output_image_label.setPixmap(pixmap)
            # Add the output image to the "Output Images" tab
            output_label = QLabel()
            output_label.setPixmap(QPixmap(output_path_from_script).scaled(200, 200, Qt.KeepAspectRatio))
            self.output_images_layout.addWidget(output_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while processing images: {e}")


    def setup_avatar_tab(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Avatars:"))

        # Load avatar images from a specified folder
        avatar_folder = "avatars"  # Specify the folder path containing avatar images
        avatar_images = os.listdir(avatar_folder)

        # Add avatar images to the layout
        for image_name in avatar_images:
            image_path = os.path.join(avatar_folder, image_name)
            avatar_label = QLabel()
            avatar_label.setPixmap(QPixmap(image_path).scaled(100, 100))  # Adjust the size as needed
            layout.addWidget(avatar_label)

        self.avatar_tab.setLayout(layout)

class PopupDialog(QDialog):
    def __init__(self, main_window, index):
        super().__init__(main_window)
        self.main_window = main_window
        self.index = index
        self.setWindowTitle("Picture source")
        self.setStyleSheet("background-color: #f5f5f5;")  # Consistent background color with the main window

        # Setup labels and buttons
        self.label = QLabel("Choose the source of your picture:")
        self.label.setFont(QFont("Arial", 12))  # Optional: Set font here if needed
        self.prev_uploaded_pic_button = QPushButton("Choose from previously uploaded pictures")
        self.avatars_button = QPushButton("Choose from avatars")
        self.new_pic_button = QPushButton("Upload a new picture")

        # Apply consistent button styling
        button_style = """
        QPushButton {
            font-size: 16px;
            background-color: #007BFF;
            color: white;
            border-radius: 5px;
            padding: 12px;
            margin: 5px;
        }
        QPushButton:hover {
            background-color: #0069D9;
        }
        """
        self.prev_uploaded_pic_button.setStyleSheet(button_style)
        self.avatars_button.setStyleSheet(button_style)
        self.new_pic_button.setStyleSheet(button_style)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_uploaded_pic_button)
        button_layout.addWidget(self.avatars_button)
        button_layout.addWidget(self.new_pic_button)

        # Main layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Connecting signals to slots
        self.prev_uploaded_pic_button.clicked.connect(self.close)
        self.avatars_button.clicked.connect(lambda: self.open_measurementsdialog(index))
        self.new_pic_button.clicked.connect(lambda: self.upload_new_picture())

    def upload_new_picture(self):
        self.main_window.upload_image(self.index)
        self.accept()

    def open_measurementsdialog(self, index):
        # Make sure to define how to handle opening measurement dialog if it's needed
        popup = MeasurementsDialog(self.main_window, index)
        popup.exec_()




class MeasurementsDialog(QDialog):

    def __init__(self, main_window, index):
        super().__init__(main_window)

        self.main_window = main_window
        self.index = index

        self.setWindowTitle("Measurements")

        self.label = QLabel("Please provide your measurements:")
        self.label.setAlignment(Qt.AlignCenter)

        self.gender_label = QLabel("Gender:")
        self.gender_combobox = QComboBox() 
        self.gender_combobox.addItems(["Woman", "Man"])

        # Fields for measurements
        self.measurement_labels = ["Height (cm):", "Chest (cm):", "Waist (cm):", "Hip (cm):", "Inseam (cm):", "Weight (kg):"]
        self.measurement_line_edits = [QLineEdit() for _ in range(len(self.measurement_labels))]

        # Layout for measurement fields
        self.measurement_layout = QFormLayout()
        for label, line_edit in zip(self.measurement_labels, self.measurement_line_edits):
            self.measurement_layout.addRow(label, line_edit)

        # Button to indicate measurements are done
        self.done_button = QPushButton("Send")
        self.done_button.clicked.connect(lambda: self.get_measurements(self.index))

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_combobox)
        layout.addLayout(self.measurement_layout)
        layout.addWidget(self.done_button)
        self.setLayout(layout)

    def get_measurements(self, index):
        gender = self.gender_combobox.currentText()
        measurements = [line_edit.text() for line_edit in self.measurement_line_edits]
        measurements.insert(0, gender)
        self.accept()
        try:
            result = subprocess.run(
                ["python", "choose_avatar.py"] + measurements,
                check=True,
                capture_output=True,
                text=True
            )
            nearest_size = result.stdout.strip()
            print("Nearest size:", nearest_size)

            avatar_path = os.path.join("avatars", nearest_size+".jpg")
            if os.path.exists(avatar_path):
                self.main_window.upload_avatar(self.index, avatar_path)
            else:
                print("Avatar for nearest size not found:", nearest_size)



        except Exception as e:
            print("An error occurred while running 'choose_avatar.py':", e)







class UploadDialog(QDialog):
    def __init__(self, main_window, index):
        super().__init__(main_window)

        self.main_window = main_window
        self.index = index

        layout = QGridLayout()
        avatar_button = QPushButton("Avatar")
        own_button = QPushButton("Own Image")

        avatar_button.clicked.connect(self.select_avatar)
        own_button.clicked.connect(self.select_own_image)

        layout.addWidget(QLabel("Choose the image source:"), 0, 0, 1, 2)
        layout.addWidget(avatar_button, 1, 0)
        layout.addWidget(own_button, 1, 1)

        self.setLayout(layout)

    def select_avatar(self):
        print("Avatar selected")
        self.accept()

    def select_own_image(self):
        self.main_window.upload_image(self.index)
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())