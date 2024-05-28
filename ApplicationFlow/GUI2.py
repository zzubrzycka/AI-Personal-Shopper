import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel,
                             QPushButton,
                             QFileDialog, QDialog, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy, QComboBox,
                             QLineEdit, QFormLayout)
from PyQt5.QtGui import QPixmap, QFont, QMovie
from PyQt5.QtCore import Qt
from application_flow import return_final_pictures, return_final_pictures_avatar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_avatar = False

        # Set up main window properties
        self.setWindowTitle("AI Personal Shopper")
        self.setGeometry(100, 100, 1250, 450)
        self.setStyleSheet("background-color: #f5f6f1;")  # Soft gray background

        # Tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Create the tabs
        self.home_tab = QWidget()
       # self.avatar_tab = QWidget()
        #self.uploaded_images_tab = QWidget()
        #self.output_images_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.home_tab, "Home")
       # self.tabs.addTab(self.avatar_tab, "Avatars")
        #self.tabs.addTab(self.uploaded_images_tab, "User Images")
        #self.tabs.addTab(self.output_images_tab, "Output Images")

        # Set up content for each tab
        self.setup_home_tab()
       # self.setup_avatar_tab()
       # self.setup_uploaded_images_tab()
        #self.setup_output_images_tab()

        # A list to store uploaded images
        self.user_uploaded_images = []
        # Store paths to images to be processed
        self.image_1_path = None
        self.image_2_path = None

        # Ensure input and output directories exist
        self.input_dir = "input_images"

        self.user_input_image_dir = "user_input_image"
        self.garment_input_image_dir = "garment_input_image"
        self.output_dir = "output_images"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def setup_home_tab(self):
        # Create a horizontal layout to separate left and right sections
        horizontal_layout = QHBoxLayout()

        # Left side: title and instructions
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
        vertical_layout1.addSpacing(20)

        # Right side: image loading
        images_layout = QVBoxLayout()

        # Button and image label for the first image
        images_layout.addSpacing(20)
        self.upload_button_1 = QPushButton("1. Upload a picture of yourself")
        self.upload_button_1.setStyleSheet("QPushButton {"
            "font-size: 16px;"
            "background-color: #ec98b8;"  
            "color: black;"
            "border-radius: 5px;"
            "padding: 12px;"
            "margin: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #f7b3cc;"
            "}")
        self.upload_button_1.setMinimumWidth(300)
        self.upload_button_1.setMinimumHeight(40)
        self.image_label_1 = QLabel("No Image Loaded")
        self.image_label_1.setAlignment(Qt.AlignCenter)
        self.image_label_1.setFixedSize(250, 250)
       # self.image_label_1.setAlignment(Qt.AlignCenter)
        self.image_label_1.setStyleSheet("border: 1px solid #ccc;")
        images_layout.addWidget(self.upload_button_1, alignment=Qt.AlignHCenter)
        images_layout.addWidget(self.image_label_1, alignment=Qt.AlignHCenter)

        # Add some extra vertical space
        images_layout.addSpacing(40)

        # Button and image label for the second image
        self.upload_button_2 = QPushButton("2. Upload the picture of the clothing")
        self.upload_button_2.setStyleSheet( "QPushButton {"
            "font-size: 16px;"
            "background-color: #ec98b8;"  
            "color: black;"
            "border-radius: 5px;"
            "padding: 12px;"
            "margin: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #f7b3cc;"
            "}")

        self.upload_button_2.setMinimumWidth(300)
        self.upload_button_2.setMinimumHeight(40)
        self.image_label_2 = QLabel("No Image Loaded")
        self.image_label_2.setAlignment(Qt.AlignCenter)
        self.image_label_2.setFixedSize(250, 250)
        self.image_label_2.setStyleSheet("border: 1px solid #ccc;")
        images_layout.addWidget(self.upload_button_2, alignment=Qt.AlignHCenter)
        images_layout.addWidget(self.image_label_2, alignment=Qt.AlignHCenter)
        images_layout.addSpacing(40)

        # "Run script" button to process the images
        self.run_script_button = QPushButton("3. Try it on!")
        self.run_script_button.setStyleSheet("QPushButton {"
            "background-color: #4CAF50;"
            "color: white;"
            "border-radius: 10px;"
            "font-size: 18px;"
            "padding: 10px;"
            "}"
            "QPushButton:hover {"
            "background-color: #45a049;"
            "}")
        self.run_script_button.setMinimumHeight(50)
        self.run_script_button.setFixedWidth(250)
        images_layout.addWidget(self.run_script_button, alignment=Qt.AlignHCenter)
        images_layout.addSpacing(25)

        # Connect button actions
       # self.upload_button_1.clicked.connect(lambda: self.upload_image(1))
       # self.upload_button_2.clicked.connect(lambda: self.upload_image(2))

        self.upload_button_1.clicked.connect(lambda: self.open_popup(1))
      #  self.upload_button_2.clicked.connect(lambda: self.open_popup(2))
        self.upload_button_2.clicked.connect(lambda: self.upload_image(2))

        self.run_script_button.clicked.connect(self.process_images)

        vertical_layout3 = QVBoxLayout()

        #LOADING GIF
        self.loading_label = QLabel()
        self.loading_movie = QMovie("loading.gif")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setFixedSize(100, 100)
        self.loading_label.setVisible(True)
        vertical_layout3.addWidget(self.loading_label, alignment=Qt.AlignHCenter)



        self.output_label = QLabel("Your Output:")
        self.output_label.setFont(QFont("Arial", 14, QFont.Bold))


        self.output_image_label = QLabel("No Output Image Yet")
        self.output_image_label.setAlignment(Qt.AlignCenter)
        #self.output_image_label.setMinimumHeight(300)
        #self.output_image_label.setMinimumWidth(250)
        self.output_image_label.setFixedSize(300, 400)
        self.output_image_label.setStyleSheet("border: 1px solid #ccc;")

        vertical_layout3.addSpacing(150)
        vertical_layout3.addWidget(self.output_label, alignment=Qt.AlignHCenter)
        vertical_layout3.addWidget(self.output_image_label, alignment=Qt.AlignHCenter)
        vertical_layout3.addSpacing(260)

        # Set stretch to control the relative space
        vertical_layout3.setStretch(0, 1)  # Adjust the stretch factor of the label
        vertical_layout3.setStretch(1, 3)  # Adjust the stretch factor of the image

        horizontal_layout.addLayout(vertical_layout1)
        horizontal_layout.addLayout(images_layout)

        horizontal_layout.setStretch(1, 500)
        horizontal_layout.addLayout(vertical_layout3)

        #horizontal_layout.addLayout(vertical_layout3)
        self.home_tab.setLayout(horizontal_layout)

    def open_popup(self, index):
        popup = PopupDialog(self, index)
        popup.accepted.connect(popup.close)
        popup.exec_()

    def start_loading(self):
        self.loading_label.setVisible(True)
        self.loading_movie.start()

    def stop_loading(self):
        self.loading_movie.stop()
        self.loading_label.setVisible(False)



    def closePopup(self):

        self.sender().close()

    #def setup_avatar_tab_EARLIER(self):
     #   layout = QVBoxLayout()
      #  layout.addWidget(QLabel("Avatars:"))

        # Add placeholder avatars
       # self.avatar_images = [QLabel(f"Avatar {i}") for i in range(1, 11)]
        #for label in self.avatar_images:
         #   label.setPixmap(QPixmap('placeholder.png').scaled(100, 100))
          #  layout.addWidget(label)

        #self.avatar_tab.setLayout(layout)

   # def setup_uploaded_images_tab(self):
        # Initialize a layout to hold multiple uploaded images
        #self.uploaded_images_layout = QVBoxLayout()
        #self.uploaded_images_tab.setLayout(self.uploaded_images_layout)

   # def setup_output_images_tab(self):
        # Initialize a layout to hold multiple output images
       # self.output_images_layout = QVBoxLayout()
        #self.output_images_tab.setLayout(self.output_images_layout)

    def upload_image(self, index):

        # Open a file dialog to select an image
        image_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        print(image_path)
        if image_path:
            image_name = os.path.basename(image_path)

        if index == 1:

            target_path2 = os.path.join(self.user_input_image_dir, image_name)
           # print(target_path2)

            for item in os.listdir(self.user_input_image_dir):
                item_path = os.path.join(self.user_input_image_dir, item)
                os.remove(item_path)


            #shutil.rmtree(self.user_input_image_dir)
            shutil.copy(image_path, target_path2)
            target_path = os.path.join(self.input_dir, image_name)
            shutil.copy(image_path, target_path)

        if index ==2:
            target_path2 = os.path.join(self.garment_input_image_dir, image_name)
            #print(target_path2)
            #shutil.rmtree(self.garment_input_image_dir)


            for item in os.listdir(self.garment_input_image_dir):
                item_path = os.path.join(self.garment_input_image_dir, item)
                os.remove(item_path)

            shutil.copy(image_path, target_path2)
            target_path = image_path



        # Copy the image to the input_images directory

        #target_path = os.path.join(self.input_dir, image_name)

        self.set_image_label(index, target_path)

        # Add the uploaded image to the "User Images" tab
        #user_image_label = QLabel()
       # user_image_label.setPixmap(QPixmap(target_path).scaled(100, 100, Qt.KeepAspectRatio))
       # self.uploaded_images_layout.addWidget(user_image_label)

        if index == 2:
            folder_path = "garment_input_image"
            files = os.listdir(folder_path)
            if len(files) == 1:
                image_path = os.path.join(folder_path, files[0])
            popup2 = CategoryDialog(self, 2, image_path)
            popup2.accepted.connect(popup2.close)
            popup2.exec_()

            copied_image_database_path = popup2.target_path
            last_folder_category = os.path.basename(os.path.normpath(copied_image_database_path))

            if len(files) == 1:
                image_path = os.path.join(last_folder_category, files[0])
            self.set_image_label(index, image_path)

            pixmap = QPixmap(target_path).scaled(200, 200, Qt.KeepAspectRatio)
            self.image_label_2.setPixmap(pixmap)

    def upload_avatar(self, index, avatar_path):
        self.is_avatar = True
        print("UZYWAMY AVATAROW, upload_avatar")
        image_path = avatar_path
        if image_path:
            image_name = os.path.basename(image_path)
            print("avatar path:", image_path)
            print("avatar name:", image_name)
        else:
            print("The path to the avatar is not right.")

        if index == 1:
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

        target_path = os.path.join(self.input_dir, image_name)
        shutil.copy(image_path, target_path)
        self.set_image_label(index, target_path)

        # Add the uploaded image to the "User Images" tab
       # user_image_label = QLabel()
      #  user_image_label.setPixmap(QPixmap(target_path).scaled(100, 100, Qt.KeepAspectRatio))
       # self.uploaded_images_layout.addWidget(user_image_label)


    def set_image_label(self, index, image_path):
        # Ensure the loaded image is displayed directly below the corresponding button
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)

        if index == 1:
            self.image_label_1.setPixmap(pixmap)
            self.image_1_path = image_path
            print("path to image1:", image_path)
        elif index == 2:
            self.image_label_2.setPixmap(pixmap)
            image_name = os.path.basename(image_path)
            last_folder = os.path.basename(os.path.dirname(image_path))
            self.image_2_path = f"/home/user/AI_Personal_Shopper/AI_Personal_Shopper/ApplicationFlow/garment_database/{last_folder}/{image_name}"
            print("path to image2:", self.image_2_path)

    def process_images(self):
        # Ensure that both images are loaded before processing
        if self.image_1_path is None or self.image_2_path is None:
            QMessageBox.warning(self, "Missing Images", "Please load both images before running the script.")
            return

        # Show loading GIF
        self.start_loading()



        # Extract file names without extensions
        name1 = os.path.splitext(os.path.basename(self.image_1_path))[0]
        name2 = os.path.splitext(os.path.basename(self.image_2_path))[0]
        output_image_name = f"{name1}_{name2}.png"
        output_image_path = os.path.join(self.output_dir, output_image_name)

        output_path_to_show = "OutPut/out_dc_0.png"

        # Execute the process_images.py script and save output to the output_images folder
      #  try:
      #      subprocess.run(
       #         ["python", "process_images.py", self.image_1_path, self.image_2_path, output_image_path],
        #        check=True
         #   )
        try:
            if self.is_avatar:
                output_path_from_script = return_final_pictures_avatar(self.image_1_path, self.image_2_path)
                print("we're using avatars function")
            else:
                output_path_from_script = return_final_pictures(self.image_1_path, self.image_2_path)
                print("we're using the normal function")

            print(f"Output path from script: {output_path_from_script}")
            print(f"Output path to show: {output_path_to_show}")

            if not os.path.exists(output_path_to_show):
                raise FileNotFoundError(f"Output file not found: {output_path_to_show}")

            #pixmap = QPixmap(output_path_from_script).scaled(300, 400, Qt.KeepAspectRatio)
            pixmap = QPixmap(output_path_to_show).scaled(300, 400, Qt.KeepAspectRatio)
            self.output_image_label.setPixmap(pixmap)
            #shutil.copy(output_path_to_show, self.output_dir)
            shutil.copy(output_path_to_show, output_image_path)
            # Add the output image to the "Output Images" tab
            #output_label = QLabel()
            #output_label.setPixmap(QPixmap(output_path_from_script).scaled(200, 200, Qt.KeepAspectRatio))
            #self.output_images_layout.addWidget(output_label)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while processing images: {e}")
        finally:
            self.stop_loading()


   # def setup_avatar_tab(self):
    #    layout = QVBoxLayout()
     #   layout.addWidget(QLabel("Avatars:"))
#
        # Load avatar images from a specified folder
 #       avatar_folder = "avatars"  # Specify the folder path containing avatar images
  #      avatar_images = os.listdir(avatar_folder)

        # Add avatar images to the layout
   #     for image_name in avatar_images:
    #        image_path = os.path.join(avatar_folder, image_name)
     #       avatar_label = QLabel()
       #     avatar_label.setPixmap(QPixmap(image_path).scaled(100, 100))  # Adjust the size as needed
      #      layout.addWidget(avatar_label)

        #self.avatar_tab.setLayout(layout)

class PopupDialog(QDialog):

    def __init__(self, main_window, index):
        super().__init__(main_window)

        self.main_window = main_window
        self.index = index

        self.setWindowTitle("Picture source")
        self.setStyleSheet("background-color: #f5f5f5;")  # Consistent background color with the main window
        self.label = QLabel("Choose the source of your picture:")


        self.avatars_button = QPushButton("Choose from avatars")
        self.new_pic_button = QPushButton("Upload a new picture")
    	
        
        self.avatars_button.setStyleSheet("QPushButton {"
            "font-size: 16px;"
            "background-color: #ec98b8;"  
            "color: black;"
            "border-radius: 5px;"
            "padding: 12px;"
            "margin: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #f7b3cc;"
            "}")
        self.new_pic_button.setStyleSheet("QPushButton {"
            "font-size: 16px;"
            "background-color: #ec98b8;"  
            "color: black;"
            "border-radius: 5px;"
            "padding: 12px;"
            "margin: 5px;"
            "}"
            "QPushButton:hover {"
            "background-color: #f7b3cc;"
            "}")

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.avatars_button)
        button_layout.addWidget(self.new_pic_button)


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)

        self.setLayout(layout)


        self.new_pic_button.clicked.connect(self.upload_new_picture)
        #self.avatars_button.clicked.connect(self.open_measurementsdialog)
        self.avatars_button.clicked.connect(self.choose_avatar)

        self.avatars_button.clicked.connect(self.close)
        self.new_pic_button.clicked.connect(self.close)



    def upload_new_picture(self):

        self.main_window.upload_image(self.index)
        self.accept()

    def open_measurementsdialog(self, index):
        popup = MeasurementsDialog(self.main_window, index)

        popup.exec_()

    def choose_avatar(self):
        self.main_window.is_avatar = True
        self.open_measurementsdialog(self.index)
        self.accept()


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
                self.main_window.upload_avatar(1, avatar_path)
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


 #okienko do wyboru kategorii
class CategoryDialog(QDialog):
    def __init__(self, main_window, index, image_path):
        super().__init__(main_window)

        self.main_window = main_window
        self.index = index
        self.target_path = None

        layout = QGridLayout()

        # Create the combo box with options
        self.combo_box = QComboBox()
        self.combo_box.addItems(["topwear", "bottomwear", "dresses"])

        # Create the confirm button
        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(lambda: self.confirm_selection(2, image_path))
       # selected_category = self.confirm_selection(2, image_path)


        # Add widgets to the layout
        layout.addWidget(QLabel("Choose the category of your garment:"), 0, 0, 1, 2)
        layout.addWidget(self.combo_box, 1, 0, 1, 2)
        layout.addWidget(confirm_button, 2, 0, 1, 2)

        self.setLayout(layout)

        #return selected_category

    def confirm_selection(self, index, image_path):
        selected_category = self.combo_box.currentText()
        print(f"Selected category: {selected_category}")
        self.target_path = f"garment_database/{selected_category}"
        shutil.copy(image_path, self.target_path)
        self.accept()
        #return selected_category

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
