import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton,
                             QFileDialog, QDialog, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up main window properties
        self.setWindowTitle("AI Personal Shopper")
        self.setGeometry(100, 100, 1100, 600)

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create the tabs
        self.home_tab = QWidget()
        self.avatar_tab = QWidget()
        self.uploaded_images_tab = QWidget()
        self.output_images_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.avatar_tab, "Avatars")
        self.tabs.addTab(self.uploaded_images_tab, "User Images")
        self.tabs.addTab(self.output_images_tab, "Output Images")

        # Set up content for each tab
        self.setup_home_tab()
        self.setup_avatar_tab()
        self.setup_uploaded_images_tab()
        self.setup_output_images_tab()

        # A list to store uploaded images
        self.user_uploaded_images = []
        # Store paths to images to be processed
        self.image_1_path = None
        self.image_2_path = None

        # Ensure input and output directories exist
        self.input_dir = "input_images"
        self.output_dir = "output_images"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def setup_home_tab(self):
        # Create a horizontal layout to separate left and right sections
        horizontal_layout = QHBoxLayout()

        # Left side: title and instructions
        vertical_layout1 = QVBoxLayout()

        title = QLabel("AI Personal Shopper")
        title_font = QFont("Arial", 20, QFont.Bold)
        title.setFont(title_font)
        vertical_layout1.addWidget(title)

        instructions = QLabel("Instructions:\n1. Choose images.\n2. Run the script.\n3. View the results.")
        instructions_font = QFont("Arial", 12)
        instructions.setFont(instructions_font)
        instructions.setWordWrap(True)
        vertical_layout1.addWidget(instructions)


        # Right side: image loading
        images_layout = QVBoxLayout()

        # Button and image label for the first image
        images_layout.addSpacing(20)
        self.upload_button_1 = QPushButton("1. Upload a picture of yourself")
        self.upload_button_1.setStyleSheet("font-size: 14px;")
        self.upload_button_1.setMinimumWidth(300)
        self.upload_button_1.setMinimumHeight(40)
        self.image_label_1 = QLabel("No Image Loaded")
        self.image_label_1.setFixedSize(250, 250)
       # self.image_label_1.setAlignment(Qt.AlignCenter)
        self.image_label_1.setStyleSheet("border: 2px solid black")
        images_layout.addWidget(self.upload_button_1, alignment=Qt.AlignHCenter)
        images_layout.addWidget(self.image_label_1, alignment=Qt.AlignHCenter)

        # Add some extra vertical space
        images_layout.addSpacing(40)

        # Button and image label for the second image
        self.upload_button_2 = QPushButton("2. Upload the picture of the clothing")
        self.upload_button_2.setStyleSheet("font-size: 14px;")

        self.upload_button_2.setMinimumWidth(300)
        self.upload_button_2.setMinimumHeight(40)
        self.image_label_2 = QLabel("No Image Loaded")
        self.image_label_2.setFixedSize(250, 250)
        self.image_label_2.setStyleSheet("border: 2px solid black")
        images_layout.addWidget(self.upload_button_2, alignment=Qt.AlignHCenter)
        images_layout.addWidget(self.image_label_2, alignment=Qt.AlignHCenter)
        images_layout.addSpacing(40)

        # "Run script" button to process the images
        self.run_script_button = QPushButton("3. Try it on!")
        self.run_script_button.setStyleSheet("background-color: green; color: white; font-size: 26px;")
        self.run_script_button.setMinimumHeight(50)
        self.run_script_button.setFixedWidth(250)
        images_layout.addWidget(self.run_script_button, alignment=Qt.AlignHCenter)
        images_layout.addSpacing(25)

        # Connect button actions
        self.upload_button_1.clicked.connect(lambda: self.upload_image(1))
        self.upload_button_2.clicked.connect(lambda: self.upload_image(2))
        self.run_script_button.clicked.connect(self.process_images)

        vertical_layout3 = QVBoxLayout()

        self.output_label = QLabel("Your Output:")
        self.output_label.setFont(QFont("Arial", 14, QFont.Bold))


        self.output_image_label = QLabel("No Output Image Yet")
        #self.output_image_label.setMinimumHeight(300)
        #self.output_image_label.setMinimumWidth(250)
        self.output_image_label.setFixedSize(300, 400)
        self.output_image_label.setStyleSheet("border: 3px solid black")

        vertical_layout3.addSpacing(100)
        vertical_layout3.addWidget(self.output_label, alignment=Qt.AlignHCenter)
        vertical_layout3.addWidget(self.output_image_label, alignment=Qt.AlignHCenter)
        vertical_layout3.addSpacing(150)

        # Set stretch to control the relative space
        vertical_layout3.setStretch(0, 1)  # Adjust the stretch factor of the label
        vertical_layout3.setStretch(1, 3)  # Adjust the stretch factor of the image

        horizontal_layout.addLayout(vertical_layout1)
        horizontal_layout.addLayout(images_layout)

        horizontal_layout.setStretch(1, 500)
        horizontal_layout.addLayout(vertical_layout3)

        #horizontal_layout.addLayout(vertical_layout3)
        self.home_tab.setLayout(horizontal_layout)

    def setup_avatar_tab(self):
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
        # Open a file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if image_path:
            # Copy the image to the input_images directory
            image_name = os.path.basename(image_path)
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

        # Execute the process_images.py script and save output to the output_images folder
        try:
            output_image_name = "output_image.png"  # Adjust this to your desired filename
            output_image_path = os.path.join(self.output_dir, output_image_name)
            subprocess.run(
                ["python", "process_images.py", self.image_1_path, self.image_2_path, output_image_path],
                check=True
            )

            # Add the output image to the "Output Images" tab
            output_label = QLabel()
            output_label.setPixmap(QPixmap(output_image_path).scaled(200, 200, Qt.KeepAspectRatio))
            self.output_images_layout.addWidget(output_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while processing images: {e}")

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
