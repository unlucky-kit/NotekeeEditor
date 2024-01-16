"""
Break function save_to_problems into two functions: save_current_problem and save_all_problems
"""

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QLabel, QScrollArea, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from styles import *
from PIL import Image, ImageOps
from OneLineTextEdit import *
import requests, webbrowser, uuid, os, zipfile, json
from settings import Settings
import appdirs



class CustomScrollArea(QScrollArea):
    def __init__(self, main_instance, parent=None):
        super().__init__(parent)
        self.main_instance = main_instance
        self.scroll_layout = None

    def showEvent(self, event):
        super().showEvent(event)
        if self.scroll_layout:
            self.main_instance.scale_images(self.scroll_layout, self)


class NotekeeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = Settings()
        self.styles = Styles(self.settings)

        self.export_or_import = 'import'

        self.current_problem_index = 0

        # Initialize current mode
        self.current_mode = 'question'

        # Initialize current chapter
        self.current_chapter = ''
        self.show_chapter_picker = False

        # Initialize question and solution strings
        self.question = ''
        self.solution = ''

        self.next_button_enabled = True
        self.previous_button_enabled = False

        self.zoomed_image_widget = None

        self.all_problems_layout_widget = None

        try:
            # This is the name of your application
            app_name = 'NotekeeEditor'

            # This is the path to the application data directory
            app_dir = appdirs.user_data_dir(app_name)

            # Create the problems.json and chapters.json files if they do not exist
            problems_file_path = os.path.join(app_dir, 'problems.json')
            chapters_file_path = os.path.join(app_dir, 'chapters.json')

            if not os.path.exists(problems_file_path):
                with open(problems_file_path, 'w') as problems_file:
                    json.dump([], problems_file)

            if not os.path.exists(chapters_file_path):
                with open(chapters_file_path, 'w') as chapters_file:
                    json.dump([], chapters_file)

            # Load problems and chapters from json files in the application data directory
            with open(problems_file_path, 'r') as problems_file, open(chapters_file_path, 'r') as chapters_file:
                # Put the data from the json files into lists
                self.problems = json.load(problems_file)
                self.chapters = json.load(chapters_file)

            if self.problems == []:
                raise FileNotFoundError

            temp_current_problem_index = self.settings.get_current_problem_index()
            if temp_current_problem_index > len(self.problems) - 1:
                self.current_problem_index = len(self.problems) - 1
            else: 
                self.current_problem_index = temp_current_problem_index

            current_problem = self.problems[self.current_problem_index]
            self.question = current_problem.get('question', '')
            self.solution = current_problem.get('solution', '')
            self.current_chapter = current_problem.get('chapter', '')

            if len(self.problems) > 1:
                self.export_or_import = 'export'

        except FileNotFoundError:
            print("JSON FILE DOES NOT EXIST")
            self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]
            self.chapters = []

        except json.JSONDecodeError:
            print("FAILED TO LOAD JSON FILE")
            self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]
            self.chapters = []

        self.init_ui()


    def build_top_button_layout(self) -> QHBoxLayout:
        button_layout = QHBoxLayout()

        chapter_button_title = self.current_chapter if self.current_chapter != '' else 'Set Chapter'
        self.chapter_button = QPushButton(chapter_button_title, self)

        self.question_button = QPushButton('Question', self)
        self.solution_button = QPushButton('Solution', self)
        
        self.previous_button = QPushButton('Previous', self)
        self.next_button = QPushButton('Next', self)

        # Connect the buttons to their respective functions
        self.question_button.clicked.connect(lambda: self.toggle_current_input_mode(self.question_button))
        self.solution_button.clicked.connect(lambda: self.toggle_current_input_mode(self.solution_button))
        self.previous_button.clicked.connect(lambda: self.previous_problem())
        self.next_button.clicked.connect(lambda: self.next_problem())
        self.chapter_button.clicked.connect(lambda: self.toggle_chapter_picker())

        if self.current_chapter != '':
            self.chapter_button.setStyleSheet(self.styles.top_chapter_button_style)
        else:
            self.chapter_button.setStyleSheet(unselected_top_chapter_button_style)

        # Set previous and next button styles
        if self.current_problem_index == 0:
            self.disable_button(self.previous_button)
            self.previous_button_enabled = False
        else:
            self.previous_button.setStyleSheet(self.styles.button_style)
        
        if self.current_problem_index == len(self.problems) - 1 and self.question == '':
            self.disable_button(self.next_button)
            self.next_button_enabled = False
        else:
            self.next_button.setStyleSheet(self.styles.button_style)

        # Set focus button style
        if self.current_mode == 'question':
            self.question_button.setStyleSheet(self.styles.focused_button_style)
            self.solution_button.setStyleSheet(self.styles.unfocused_button_style)
        else:
            self.question_button.setStyleSheet(self.styles.unfocused_button_style)
            self.solution_button.setStyleSheet(self.styles.focused_button_style)

        # Add the buttons to the layout
        button_layout.addWidget(self.chapter_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.question_button)
        button_layout.addWidget(self.solution_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)

        # Setting pointing hand cursor for buttons
        for button in [self.chapter_button, self.previous_button, self.next_button, self.question_button, self.solution_button]:
            button.setCursor(Qt.PointingHandCursor)

        return button_layout


    def delete_image(self, image):
        try:
            # Remove image from problems dictionary
            current_problem = self.problems[self.current_problem_index]
            current_problem[self.current_mode + '_images'].remove(image)

            # This is the name of your application
            app_name = 'NotekeeEditor'

            # This is the path to the application data directory
            app_dir = appdirs.user_data_dir(app_name)

            # Delete image file from the images folder in the application data directory
            os.remove(os.path.join(app_dir, 'images', f'{image}.webp'))

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

        except FileNotFoundError:
            pass
        finally:
            self.save_to_problems()
            self.update_images()


    def zoom_in_image(self, image):
        # Hide the right_layout widget
        self.right_layout_widget.hide()

        # Create a new QWidget for the zoomed image
        self.zoomed_image_widget = QWidget()

        # Create a QVBoxLayout for the zoomed image widget
        zoomed_image_layout = QVBoxLayout(self.zoomed_image_widget)

        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        # Load the image from the images folder in the application data directory
        label = QLabel(self)
        pixmap = QPixmap(os.path.join(app_dir, 'images', f'{image}.webp'))
        label.setPixmap(pixmap)
        label.setProperty('originalPixmap', pixmap)  # Set the original QPixmap as a property of the label
        zoomed_image_layout.addWidget(label)
        zoomed_image_layout.setAlignment(Qt.AlignCenter)

        # Create a QScrollArea and set zoomed_image_widget as its widget
        self.zoomed_image_scroll_area = QScrollArea()  # Store the scroll area as an instance variable
        self.zoomed_image_scroll_area.setWidget(self.zoomed_image_widget)
        self.zoomed_image_scroll_area.setWidgetResizable(True)

        zoomed_image_layout.setSpacing(0)

        # Add the QScrollArea to the workspace_layout
        self.workspace_layout.addWidget(self.zoomed_image_scroll_area, 1)

        # Add a QHBoxLayout to the bottom of the workspace_layout for the buttons
        self.image_button_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()  # Store the button layout as an instance variable
        zoom_out_button = QPushButton('Zoom out')
        delete_button = QPushButton('Delete')
        zoom_out_button.setStyleSheet(self.styles.zoom_button_style)
        delete_button.setStyleSheet(self.styles.delete_button_style)
        zoom_out_button.setCursor(Qt.PointingHandCursor)
        delete_button.setCursor(Qt.PointingHandCursor)
        self.image_button_layout.addWidget(self.zoomed_image_scroll_area)
        self.image_button_layout.addLayout(self.button_layout)
        zoom_out_button.clicked.connect(self.zoom_out_image)
        delete_button.clicked.connect(lambda: self.delete_image(image))
        self.button_layout.setSpacing(15)
        self.button_layout.addWidget(zoom_out_button)
        self.button_layout.addWidget(delete_button)
        self.workspace_layout.addLayout(self.image_button_layout, 1)


    def zoom_out_image(self):
        # Remove the zoomed image widget, the scroll area, and the button layout from the workspace_layout
        self.workspace_layout.removeWidget(self.zoomed_image_scroll_area)
        self.zoomed_image_scroll_area.deleteLater()
        self.zoomed_image_scroll_area = None
        self.zoomed_image_widget.deleteLater()
        self.zoomed_image_widget = None

        # Remove the button layout
        for i in reversed(range(self.button_layout.count())):  # Remove widgets from the layout
            widget = self.button_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.workspace_layout.removeItem(self.button_layout)  # Remove the layout from the workspace_layout
        self.workspace_layout.removeItem(self.image_button_layout)
        self.button_layout.deleteLater()
        self.button_layout = None

        # Show the right_layout widget
        self.right_layout_widget.show()


    def build_images_scroll_area(self) -> QScrollArea:
        scroll_area = CustomScrollArea(self, self)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_widget = QWidget()
        scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        self.scroll_layout = QHBoxLayout(scroll_widget)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setContentsMargins(5, 0, 5, 10)
        scroll_area.scroll_layout = self.scroll_layout

        current_problem = self.problems[self.current_problem_index]
        current_image_list = current_problem[self.current_mode + '_images']

        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        for image in current_image_list:
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)
            image_layout.setContentsMargins(5, 0, 5, 0)
            image_layout.setSpacing(0)  # Set spacing to 0 to remove space between image and buttons
            image_layout.setAlignment(Qt.AlignTop)  # Align the image and buttons to the top

            label = QLabel(self)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Load the image from the images folder in the application data directory
            pixmap = QPixmap(os.path.join(app_dir, 'images', f'{image}.webp'))
            label.setPixmap(pixmap)
            label.setProperty('originalPixmap', pixmap)
            label.setAlignment(Qt.AlignCenter)
            image_layout.addWidget(label)

            button_layout = QHBoxLayout()
            zoom_button = QPushButton('Zoom in')
            delete_button = QPushButton('Delete')
            button_layout.setSpacing(15)
            delete_button.clicked.connect(lambda checked, img=image: self.delete_image(img))
            zoom_button.clicked.connect(lambda: self.zoom_in_image(image))
            zoom_button.setStyleSheet(self.styles.zoom_button_style)
            delete_button.setStyleSheet(self.styles.delete_button_style)
            zoom_button.setCursor(Qt.PointingHandCursor)
            delete_button.setCursor(Qt.PointingHandCursor)
            button_layout.addWidget(zoom_button)
            button_layout.addWidget(delete_button)
            image_layout.addLayout(button_layout)

            self.scroll_layout.addWidget(image_widget)

        scroll_area.resizeEvent = lambda event: self.scale_images(scroll_area.scroll_layout, scroll_area)

        return scroll_area


    def scale_images(self, layout, scroll_area):
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if isinstance(widget, QWidget):
                image_layout = widget.layout()
                if image_layout is not None:  # Add this line
                    label = image_layout.itemAt(0).widget()  # Get the QLabel from the QVBoxLayout
                    if isinstance(label, QLabel):
                        original_pixmap = label.property('originalPixmap')  # Get the original QPixmap
                        if original_pixmap:
                            image = original_pixmap.toImage()  # Convert QPixmap to QImage
                            # Subtract a small amount from the height to ensure the image fits within the available vertical space
                            image = image.scaled(scroll_area.width(), scroll_area.height() - 45, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Scale the QImage
                            pixmap = QPixmap.fromImage(image)  # Convert QImage back to QPixmap
                            label.setPixmap(pixmap)


    def update_images(self):
        # Remove the current images_scroll_area from the layout
        if self.images_scroll_area_widget is not None:
            self.right_layout.removeWidget(self.images_scroll_area_widget)
            self.images_scroll_area_widget.deleteLater()
            self.images_scroll_area_widget = None

        # Add a new images_scroll_area to the layout if necessary
        current_problem = self.problems[self.current_problem_index]
        if current_problem[self.current_mode + '_images'] != []:
            self.images_scroll_area_widget = self.build_images_scroll_area()
            self.right_layout.addWidget(self.images_scroll_area_widget, 3)


    def build_chapters_scroll_area(self) -> QScrollArea:
        self.chapters_layout = QVBoxLayout()

        # Create a new widget for the chapters_layout and set it as the widget of a QScrollArea
        chapters_widget = QWidget()
        chapters_widget.setLayout(self.chapters_layout)
        self.chapters_scroll_area = QScrollArea()
        self.chapters_scroll_area.setWidget(chapters_widget)
        self.chapters_scroll_area.setWidgetResizable(True)
        
        chapter_input_layout = QHBoxLayout()
        checkmark_button = QPushButton('\u2713', self)
        self.chapter_input = OneLineTextEdit(self, ref = self)

        checkmark_button.setStyleSheet(self.styles.checkmark_button_style)
        checkmark_button.setCursor(Qt.PointingHandCursor)
        checkmark_button.clicked.connect(lambda: self.create_new_chapter(self.chapter_input.toPlainText().strip()))
        
        chapter_input_layout.addWidget(self.chapter_input)
        chapter_input_layout.addWidget(checkmark_button)

        self.chapters_layout.addLayout(chapter_input_layout, 0)

        for chapter in self.chapters:
            temp_chapter_button = QPushButton(chapter, self)

            if chapter == self.current_chapter:
                temp_chapter_button.setStyleSheet(chapter_button_style_selected)
            else:
                temp_chapter_button.setStyleSheet(self.styles.chapter_button_style)

            temp_chapter_button.setCursor(Qt.PointingHandCursor)
            temp_chapter_button.clicked.connect(lambda _, chapter=chapter: self.set_chapter(chapter))
            self.chapters_layout.addWidget(temp_chapter_button)

        self.chapters_layout.addStretch(1)

        self.chapters_scroll_area.setVisible(False)

        return self.chapters_scroll_area


    def build_workspace_layout(self) -> QHBoxLayout:
        self.workspace_layout = QHBoxLayout()

        # Create a QWebEngineView for displaying HTML
        self.right_layout = QVBoxLayout()
        self.webview = QWebEngineView(self)

        # Create a QTextEdit for KaTeX input
        self.katex_input = QTextEdit(self)
        font = QFont("Courier New")
        font.setPointSize(13)
        self.katex_input.setFont(font)
        self.katex_input.setPlaceholderText("Enter KaTeX here...")
        if self.question != '':
            self.katex_input.setPlainText(self.question)
            self.update_math()
        self.katex_input.textChanged.connect(self.update_math)

        self.right_layout_widget = QWidget()
        self.right_layout_widget.setLayout(self.right_layout)
        self.right_layout_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_layout.setContentsMargins(0, 0, 0, 0)


        self.right_layout.addWidget(self.webview, 4)

        self.images_scroll_area_widget = None
        current_problem = self.problems[self.current_problem_index]
        if current_problem['question_images'] != []:
            self.images_scroll_area_widget = self.build_images_scroll_area()
            self.right_layout.addWidget(self.images_scroll_area_widget, 3)

        # Add chapters_scroll_area to the workspace_layout instead of chapters_layout
        self.workspace_layout.addWidget(self.build_chapters_scroll_area(), 1)
        self.workspace_layout.addWidget(self.katex_input, 1)
        self.workspace_layout.addWidget(self.right_layout_widget, 1)

        return self.workspace_layout

    def check_for_updates(self):
        try:
            response = requests.get('https://api.github.com/repos/unlucky-kit/NotekeeEditor/releases/latest')
            latest_release = response.json()
            latest_version = latest_release['tag_name']

            current_version = 'v1.0.0'  # Replace with your app's current version

            if latest_version > current_version:
                return latest_release['html_url']
            else:
                return False
        except requests.exceptions.RequestException:
            print("Unable to check for updates: no internet connection")
            return False
        except KeyError:
            print("Unable to check for updates: invalid response")
            return False
        

    def build_bottom_button_layout(self) -> QHBoxLayout:
        button_layout = QHBoxLayout()

        all_problems_button = QPushButton('All problems', self)
        
        self.export_import_button = QPushButton(self.export_or_import.capitalize(), self)
        
        if self.settings.get_color_scheme() == 'dark':
            color_scheme_button = QPushButton("Light mode", self)
        else:
            color_scheme_button = QPushButton("Dark mode", self)
        
        upload_image_button = QPushButton('Upload Image', self)

        update_url = self.check_for_updates()
        if update_url:
            update_button = QPushButton('Update available', self)
            update_button.setStyleSheet(self.styles.link_button_style)
            update_button.setCursor(Qt.PointingHandCursor)
            update_button.clicked.connect(lambda: webbrowser.open(update_url))

        button_layout.addWidget(all_problems_button)
        button_layout.addSpacing(8)
        button_layout.addWidget(self.export_import_button)
        button_layout.addSpacing(8)
        button_layout.addWidget(color_scheme_button)
        button_layout.addStretch(1)
        button_layout.addWidget(upload_image_button)

        # Connect the buttons to their respective functions
        color_scheme_button.clicked.connect(lambda: self.toggle_color_scheme())
        all_problems_button.clicked.connect(lambda: self.toggle_all_problems_layout_widget())

        self.export_import_button.clicked.connect(lambda: self.handle_zip())

        upload_image_button.clicked.connect(lambda: self.upload_image())

        # Setting stylesheet and cursor for buttons
        for button in [all_problems_button, self.export_import_button, color_scheme_button, upload_image_button]:
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(self.styles.link_button_style)

        return button_layout

    def toggle_color_scheme(self):
        # Rebuild the whole UI
        self.settings.toggle_color_scheme()
        self.styles = Styles(self.settings)

        self.rebuild_ui()

    def reset_minor_variables(self):
        # Reset all instance variables excluding the ones that contain information about the current problem
        self.current_mode = 'question'
        self.show_chapter_picker = False
        self.zoomed_image_widget = None
        self.all_problems_layout_widget = None

    def upload_zip(self):
        try:
            # This is the name of your application
            app_name = 'NotekeeEditor'

            # This is the path to the application data directory
            app_dir = appdirs.user_data_dir(app_name)

            # Get the path to the Desktop
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")

            # Specify the name of the zip file
            zip_file_name = QFileDialog.getOpenFileName(self, 'Open file', desktop, 'Zip files (*.zip)')[0]

            # If the user didn't select a file, do nothing
            if zip_file_name == '':
                return

            # Extract the zip file to the application data directory
            with zipfile.ZipFile(zip_file_name, 'r') as zipf:
                zipf.extractall(app_dir)

            # Load the problems and chapters from the json files in the application data directory
            with open(os.path.join(app_dir, 'problems.json'), 'r') as problems_file, open(os.path.join(app_dir, 'chapters.json'), 'r') as chapters_file:
                self.problems = json.load(problems_file)
                self.chapters = list(set(self.chapters + json.load(chapters_file)))

            # Add images to the images folder in the application data directory
            for foldername, _, filenames in os.walk(os.path.join(app_dir, 'images')):
                for filename in filenames:
                    if filename != '.gitkeep':  # Exclude .gitkeep files
                        os.rename(os.path.join(foldername, filename), os.path.join(app_dir, 'images', filename))

            # Get the last problem's data
            if self.problems:
                current_problem = self.problems[self.current_problem_index]
                self.question = current_problem.get('question', '')
                self.solution = current_problem.get('solution', '')
                self.current_chapter = current_problem.get('chapter', '')
            else:
                raise Exception("No problems found in the problems.json file")

            if len(self.problems) > 1:
                self.export_or_import = 'export'
                self.export_import_button.setText('Export')
            elif self.problems == []:
                self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]

            # Rebuild the whole UI
            self.rebuild_ui()

        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except json.JSONDecodeError as json_error:
            print(f"Invalid JSON file: {json_error}")
        except zipfile.BadZipFile as zip_error:
            print(f"Invalid zip file: {zip_error}")
        except Exception as e:
            print(f"An error occurred: {e}")


    def handle_zip(self):
        if self.export_or_import == 'export':
            self.download_zip()
        else:
            self.upload_zip()

    def create_zip(self, destination):
        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        with zipfile.ZipFile(destination, 'w') as zipf:
            # Write the problems.json and chapters.json files from the application data directory to the zip file
            zipf.write(os.path.join(app_dir, 'problems.json'), arcname='problems.json')
            zipf.write(os.path.join(app_dir, 'chapters.json'), arcname='chapters.json')

            # Write the images from the images folder in the application data directory to the zip file
            for foldername, _, filenames in os.walk(os.path.join(app_dir, 'images')):
                for filename in filenames:
                    zipf.write(os.path.join(foldername, filename), arcname=os.path.join('images', filename))


    # Will return None if everything is good, otherwise will return an error message
    def problems_json_error_message(self):
        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        with open(os.path.join(app_dir, 'problems.json'), 'r') as file:
            data = json.load(file)
            
            for problem in data:
                if problem['question'] == '': 
                    return "At least one problem has no question!"
                elif problem['solution'] == '' and problem['solution_images'] == []:
                    return "At least one problem has no solution!"

            return None


    def download_zip(self):
        self.save_to_problems(can_delete_empty_problem = False, can_skip_saving = False)
        
        # Check if there are problems without solutions
        problems_json_error_message = self.problems_json_error_message()
        if problems_json_error_message != None:
            QMessageBox.critical(self, "Error", f"{problems_json_error_message} Check problems colored red when you click 'All problems' button.")
            return
            
        # Get the path to the Desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")

        # Specify the name of the zip file
        export_index = self.settings.get_export_index()
        zip_file_name = f"notekee-{export_index}.zip"

        # Create the full path
        destination = os.path.join(desktop, zip_file_name)

        self.create_zip(destination)

        if not os.path.isfile(destination):
            QMessageBox.critical(self, "Error", "Failed to export the problems!")
            return

        # Erase all problems
        self.solution = ''
        self.question = ''
        self.current_problem_index = 0
        self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]
        self.current_chapter = ''
        self.chapters = []
        self.save_to_chapters()
        self.save_to_problems()

        # Empty images folder, excluding .gitkeep file
        for foldername, _, filenames in os.walk('images'):
            for filename in filenames:
                if filename != '.gitkeep':
                    os.remove(os.path.join(foldername, filename))

        self.export_or_import = 'import'
        self.export_import_button.setText('Import')
        self.settings.increment_export_index()

        self.save_to_problems(can_delete_empty_problem = False, can_skip_saving = False)
        
        self.rebuild_ui()


    def rebuild_ui(self):
        self.settings.save_window_position_and_size(self)
        self.centralWidget().deleteLater()
        self.reset_minor_variables()
        self.init_ui()
        self.update_images()


    def remove_empty_problems(self):
        for problem in self.problems:
            if problem['question'] == '' and problem['solution'] == '':
                if problem['question_images'] == [] and problem['solution_images'] == []:
                    self.problems.remove(problem)

        if self.current_problem_index > len(self.problems) - 1:
            self.current_problem_index = len(self.problems) - 1

    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.setStyleSheet(self.styles.app_style)

        self.secondary_layout_widget = QWidget(self)
        secondary_layout = QVBoxLayout(self.secondary_layout_widget)
        secondary_layout.setContentsMargins(0, 0, 0, 0)

        # Removing vertical padding from the buttons
        spacer1 = QSpacerItem(-5, -5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        # spacer2 = QSpacerItem(-10, -10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer3 = QSpacerItem(-5, -5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        secondary_layout.addItem(spacer1)
        secondary_layout.addLayout(self.build_top_button_layout())
        # secondary_layout.addItem(spacer2)

        
        secondary_layout.addLayout(self.build_workspace_layout())

        secondary_layout.addItem(spacer3)
        secondary_layout.addLayout(self.build_bottom_button_layout())

        self.layout.addWidget(self.secondary_layout_widget)

        self.setWindowTitle("Notekee Editor")
        window_position = self.settings.get_window_position()
        window_size = self.settings.get_window_size()
        self.setGeometry(window_position[0], window_position[1], window_size[0], window_size[1])


    def toggle_all_problems_layout_widget(self):
        if self.all_problems_layout_widget is None:
            if self.current_chapter == '':
                return
            
            self.save_to_problems(can_skip_saving = False) # Makes sure current problem is saved
            self.remove_empty_problems()
            self.remove_empty_chapters()

            # Delete this after first release
            current_problem = self.problems[self.current_problem_index]
            if self.question != current_problem['question'] or self.solution != current_problem['solution']:
                self.question = current_problem['question']
                self.solution = current_problem['solution']

            self.save_to_problems(can_skip_saving = False) # Makes sure removal of empty problems is saved
            self.save_to_chapters() # Makes sure removal of empty chapters is saved


            # If current problem's chapter wasn't yet saved, assign it one.
            if self.problems[self.current_problem_index]['chapter'] == '':
                self.problems[self.current_problem_index]['chapter'] = self.current_chapter

            if self.current_chapter not in self.chapters:
                self.current_chapter = self.problems[self.current_problem_index]['chapter']
                self.chapter_button.setText(self.current_chapter)


            self.all_problems_layout_widget = QWidget()

            all_problems_layout = QVBoxLayout(self.all_problems_layout_widget)
            all_problems_scroll_area = QScrollArea()
            all_problems_scroll_area.setWidgetResizable(True)
            all_problems_layout_widget = QWidget()
            all_problems_scroll_area_layout = QVBoxLayout(all_problems_layout_widget)
            all_problems_scroll_area.setWidget(all_problems_layout_widget)

            chapter_problems = {}
            for chapter in self.chapters:
                chapter_problems[chapter] = []

            for problem in self.problems:
                chapter_problems[problem['chapter']].append(problem)

            for chapter in chapter_problems:
                chapter_button = QPushButton(f'▼ {chapter}', self)
                chapter_problem_layout = QVBoxLayout()
                chapter_button.setStyleSheet(self.styles.plain_chapter_button_style)
                chapter_button.setCursor(Qt.PointingHandCursor)

                for i in range(len(chapter_problems[chapter])):
                    problem = chapter_problems[chapter][i]
                    problem_question = problem['question'].replace('\n', ' ')
                    problem_button = QPushButton(f'{i + 1}. {problem_question}', self)
                    problem_button.clicked.connect(lambda _, problem=problem: self.load_problem(problem))
                    problem_button.setCursor(Qt.PointingHandCursor)
                    if self.problems.index(problem) != self.current_problem_index:
                        if problem['solution'] == '' and problem['solution_images'] == [] or problem['question'] == '':
                            problem_button.setStyleSheet(self.styles.error_with_problem_button_style)
                        else:
                            problem_button.setStyleSheet(self.styles.plain_problem_button_style)
            
                    else:
                        problem_button.setStyleSheet(self.styles.current_problem_button_style)

                    chapter_problem_layout.addWidget(problem_button)

                def toggle_visibility(button, layout, chapter_name):
                    for i in range(layout.count()):
                        widget = layout.itemAt(i).widget()
                        widget.setVisible(not widget.isVisible())
                    # Change the button text based on the visibility of the first problem
                    if layout.count() > 0 and layout.itemAt(0).widget().isVisible():
                        button.setText(f'▼ {chapter_name}')
                    else:
                        button.setText(f'▶ {chapter_name}')

                # Shortening this line will cause all buttons to toggle only one chapter
                chapter_button.clicked.connect(lambda _, button=chapter_button, layout=chapter_problem_layout, chapter=chapter: toggle_visibility(button, layout, chapter))

                all_problems_scroll_area_layout.addWidget(chapter_button)
                all_problems_scroll_area_layout.addLayout(chapter_problem_layout)

            all_problems_scroll_area_layout.addStretch(1)

            all_problems_layout.addWidget(all_problems_scroll_area)
            all_problems_layout.setContentsMargins(0, 0, 0, 0)

            # Create a "Back" button and add it to the layout
            back_button = QPushButton("Back", self)
            back_button.clicked.connect(lambda: self.toggle_all_problems_layout_widget())
            back_button.setCursor(Qt.PointingHandCursor)
            back_button.setStyleSheet(self.styles.link_button_style)

            back_button_layout = QHBoxLayout()
            back_button_layout.addWidget(back_button)
            back_button_layout.addStretch(1)

            all_problems_layout.addLayout(back_button_layout)

            self.layout.addWidget(self.all_problems_layout_widget)

            self.secondary_layout_widget.setVisible(False)

        else:
            if (self.solution == '' and self.question == '') or self.question != self.problems[self.current_problem_index]['question']:
                problem = self.problems[self.current_problem_index]
                self.question = problem['question']
                self.solution = problem['solution']
                self.current_chapter = problem['chapter']

                self.katex_input.setPlainText(self.question if self.current_mode == 'question' else self.solution)
                self.update_math()
            
            # Else if katex_input is empty and if there is something in the current problem's question or solution, load it
            elif self.katex_input != (self.question if self.current_mode == 'question' else self.solution):
                if self.current_mode == 'question':
                    self.katex_input.setPlainText(self.question)
                    if self.problems[self.current_problem_index]['question_images'] != []:
                        self.update_images()
                else:
                    self.katex_input.setPlainText(self.solution)
                    if self.problems[self.current_problem_index]['solution_images'] != []:
                        self.update_images()
                self.update_math()
                
                    

            self.layout.removeWidget(self.all_problems_layout_widget)
            self.all_problems_layout_widget.deleteLater()
            self.all_problems_layout_widget = None

            self.secondary_layout_widget.setVisible(True)


    def load_problem(self, problem):
        # If the problem is already loaded, do nothing
        if self.current_problem_index == self.problems.index(problem):
            if self.katex_input.toPlainText() == (self.question if self.current_mode == 'question' else self.solution):
                self.toggle_all_problems_layout_widget()
                return
    
        # Zoom out the image if it is zoomed in
        if self.zoomed_image_widget is not None:
            self.zoom_out_image()


        # Load new problem's data
        self.question = problem['question']
        self.solution = problem['solution']
        self.current_problem_index = self.problems.index(problem)
        if self.current_chapter != problem['chapter']:
            self.set_chapter(problem['chapter'])
            self.chapter_button.setText(self.current_chapter)
            
        
        
        if self.current_mode != 'question':
            self.katex_input.setPlainText(self.solution) # Prevents from self.solution getting the value of the previous problem's katex_input
            self.toggle_current_input_mode(self.question_button)

        if self.show_chapter_picker:
            self.toggle_chapter_picker()

        self.katex_input.setPlainText(self.question)
        self.toggle_all_problems_layout_widget()
        self.update_math()
        self.update_images()

        if self.current_problem_index == 0:
            self.disable_button(self.previous_button)
            self.previous_button_enabled = False
        else:
            self.enable_button(self.previous_button)
            self.previous_button_enabled = True
        
        if self.current_problem_index == len(self.problems) - 1 and self.question == '':
            self.disable_button(self.next_button)
            self.next_button_enabled = False
        else:
            self.enable_button(self.next_button)
            self.next_button_enabled = True


    def save_to_chapters(self):
        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        with open(os.path.join(app_dir, 'chapters.json'), 'w') as file:
            json.dump(self.chapters, file, indent=4)

    def delete_empty_problems(self):
        for problem in self.problems:
            if problem['question'] == '' and problem['solution'] == '':
                if problem['question_images'] == [] and problem['solution_images'] == []:
                    self.problems.remove(problem)

        if self.current_problem_index > len(self.problems) - 1:
            self.current_problem_index = len(self.problems) - 1

    # can_delete_empty_problem = True and can_skip_saving = False will always crash the program if current problem is empty
    def save_to_problems(self, can_delete_empty_problem = False, can_skip_saving = True):
        # If the current problem is empty and there are no images, skip saving
        if self.solution == '' and self.question == '':
            # Because we don't have self.solution_images and self.question_images, we have to get them from the problems list
            solution_images = self.problems[self.current_problem_index]['solution_images']
            question_images = self.problems[self.current_problem_index]['question_images']

            if solution_images == [] and question_images == []:
                if can_delete_empty_problem:
                    self.problems.pop(self.current_problem_index)
                if can_skip_saving:
                    return

        current_problem = self.problems[self.current_problem_index]

        # Update the current problem's data if it has changes
        if current_problem['question'] != self.question:
            current_problem['question'] = self.question
        if current_problem['solution'] != self.solution:
            current_problem['solution'] = self.solution
        if current_problem['chapter'] != self.current_chapter:
            current_problem['chapter'] = self.current_chapter

        # Remove empty problems from json's version of data
        clean_problems = []
        for problem in self.problems:
            if problem['question'] != '' or problem['solution'] != '' or problem['question_images'] != [] or problem['solution_images'] != []:
                clean_problems.append(problem)

        if self.export_or_import == 'import' and len(clean_problems) > 1:
            self.export_or_import = 'export'
            self.export_import_button.setText('Export')
        elif self.export_or_import == 'export' and len(clean_problems) <= 1:
            self.export_or_import = 'import'
            self.export_import_button.setText('Import')

        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        # Save the data to the json file in the application data directory
        with open(os.path.join(app_dir, 'problems.json'), 'w') as file:
            json.dump(clean_problems, file, indent=4)


    def create_new_chapter(self, chapter_name):

        chapter_name = chapter_name.strip()
        self.chapter_input.clear()
        if chapter_name == '' or chapter_name in self.chapters:
            return

        self.chapters.insert(0, chapter_name)  # Add chapter to the top of the list

        # Create a new chapter button and add it to the layout
        new_chapter_button = QPushButton(chapter_name, self)
        new_chapter_button.setStyleSheet(chapter_button_style_selected)
        new_chapter_button.setCursor(Qt.PointingHandCursor)
        new_chapter_button.clicked.connect(lambda _, chapter=chapter_name: self.set_chapter(chapter))
        self.chapters_layout.insertWidget(1, new_chapter_button)  # Insert button at the top
        
        self.set_chapter(chapter_name)

        self.remove_empty_chapters()
        self.save_to_chapters()


    def set_chapter(self, chapter):
        # Make style of the previously selected chapter button normal
        if self.current_chapter != '':
            index_of_previous_chapter = self.chapters.index(self.current_chapter)
            self.chapters_layout.itemAt(index_of_previous_chapter + 1).widget().setStyleSheet(self.styles.chapter_button_style)

        self.current_chapter = chapter
        index_of_current_chapter = self.chapters.index(self.current_chapter)
        self.chapters_layout.itemAt(index_of_current_chapter + 1).widget().setStyleSheet(self.styles.chapter_button_style)
        self.chapters_layout.itemAt(self.chapters.index(chapter) + 1).widget().setStyleSheet(chapter_button_style_selected)
        # self.current_chapter = chapter 
        self.problems[self.current_problem_index]['chapter'] = chapter
        

    def remove_empty_chapters(self):
        for i in range(1, self.chapters_layout.count() - 1):
            chapter_name = self.chapters_layout.itemAt(i).widget().text()
            for problem in self.problems:
                if problem['chapter'] == chapter_name:
                    break 
            else:
                self.chapters_layout.itemAt(i).widget().deleteLater()
                self.chapters.remove(chapter_name)


    def toggle_current_input_mode(self, clicked_button):
        if clicked_button is self.question_button:
            if self.current_mode != 'question':
                self.current_mode = 'question'
            else:
                return

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

            # Changing the style of the buttons
            self.question_button.setStyleSheet(self.styles.focused_button_style)
            self.solution_button.setStyleSheet(self.styles.unfocused_button_style)

            # Saving the question to the question string and setting the text to the solution
            self.solution = self.katex_input.toPlainText()
            self.katex_input.setPlainText(self.question)

        else:
            if self.current_mode != 'solution':
                self.current_mode = 'solution'
            else:  
                return

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

            # Changing the style of the buttons
            self.solution_button.setStyleSheet(self.styles.focused_button_style)
            self.question_button.setStyleSheet(self.styles.unfocused_button_style)

            # Saving the solution to the solution string and setting the text to the question
            self.question = self.katex_input.toPlainText()
            self.katex_input.setPlainText(self.solution)
            
        self.update_images()
        self.save_to_problems()


    def toggle_chapter_picker(self):
        if not self.show_chapter_picker: # Show chapter picker
            self.remove_empty_chapters()
            self.save_to_chapters()

            # Substituting the katex_input with the chapters_scroll_area
            self.workspace_layout.removeItem(self.workspace_layout.itemAt(0))
            self.workspace_layout.insertWidget(0, self.chapters_scroll_area, 1)  # Use insertWidget instead of insertLayout
            
            self.katex_input.clearFocus()
            self.katex_input.setVisible(False)
            self.chapter_button.setText('Done')
            self.chapter_button.setStyleSheet(self.styles.top_chapter_button_style)

            self.chapters_scroll_area.setVisible(True)

            self.show_chapter_picker = True

        else: # Hide chapter picker
            self.chapter_input.clear()
            self.workspace_layout.removeItem(self.workspace_layout.itemAt(0))
            self.workspace_layout.insertWidget(0, self.katex_input, 1)
            self.katex_input.setPlainText(self.question if self.current_mode == 'question' else self.solution)
            self.katex_input.setVisible(True)

            if self.current_chapter != '':
                self.chapter_button.setStyleSheet(self.styles.top_chapter_button_style)
            else:
                self.chapter_button.setStyleSheet(unselected_top_chapter_button_style)

            self.chapter_button.setText(self.current_chapter if self.current_chapter != '' else 'Set Chapter')

            self.chapters_scroll_area.setVisible(False)

            self.show_chapter_picker = False


    def disable_button(self, button):
        button.setStyleSheet(self.styles.disabled_button_style)
        button.setEnabled(False)


    def enable_button(self, button):
        button.setStyleSheet(self.styles.button_style)
        button.setEnabled(True)


    def next_problem(self):
        
        if self.current_chapter == '':
            QMessageBox.critical(self, "Error", "Please set a chapter for the current problem.")
            return
        elif (self.question == '' and self.current_problem_index == len(self.problems) - 1):
            return

        self.save_to_problems()
        

        # Zoom out the image if it is zoomed in
        if self.zoomed_image_widget is not None:
            self.zoom_out_image()
 
        # If the chapter picker is open, close it
        if self.show_chapter_picker:
            self.toggle_chapter_picker()

        # Increment the current problem index
        self.current_problem_index += 1

        # If there is a next problem, load it
        if self.current_problem_index <= len(self.problems) - 1:

            next_problem = self.problems[self.current_problem_index]
            self.question = next_problem.get('question', '')
            self.solution = next_problem.get('solution', '')
            if self.current_chapter != next_problem.get('chapter', ''):
                # self.current_chapter = next_problem.get('chapter', '')
                self.set_chapter(next_problem.get('chapter', ''))
                
            self.chapter_button.setText(self.current_chapter)

            previous_problem = self.problems[self.current_problem_index - 1]
            if previous_problem['chapter'] != self.current_chapter:
                self.set_chapter(self.current_chapter)

            # Set the text of the QTextEdit to the question or solution
            if self.current_mode == 'question':
                self.katex_input.setPlainText(self.question)
            else: 
                self.katex_input.setPlainText(self.solution)
           
        else:
            # Otherwise, create a new problem data
            new_problem = {'question': '', 'solution': '', 'chapter': self.current_chapter, 'question_images': [], 'solution_images': []}
            self.problems.append(new_problem)
            self.katex_input.clear()
            self.question = ''
            self.solution = ''
            
            if self.current_mode != 'question':
                self.current_mode = 'question'

                # Changing the style of the buttons
                self.question_button.setStyleSheet(self.styles.focused_button_style)
                self.solution_button.setStyleSheet(self.styles.unfocused_button_style)
            
            self.disable_button(self.next_button)
            self.next_button_enabled = False

        self.update_images()

        if not self.previous_button_enabled:
            self.enable_button(self.previous_button)
            self.previous_button_enabled = True


    def previous_problem(self):
        # If the current problem is the first problem, do nothing
        if self.current_problem_index == 0:
            return
        
        # If the previous problem is first problem, disable the previous button
        elif self.current_problem_index == 1:
            self.disable_button(self.sender())
            self.previous_button_enabled = False

            # If next if disabled, enable it
            if self.next_button_enabled:
                self.disable_button(self.next_button)
                self.next_button_enabled = False
                

        # Zoom out the image if it is zoomed in  
        if self.zoomed_image_widget is not None:
                self.zoom_out_image()

        # If the chapter picker is open, close it
        if self.show_chapter_picker:
            self.toggle_chapter_picker()

        self.save_to_problems(can_delete_empty_problem = True)

        if self.export_or_import == 'export' and len(self.problems) <= 2:
            self.export_or_import = 'import'
            self.export_import_button.setText('Import')


        # if len(self.problems) > 2:
        #     self.save_to_problems(can_delete_empty_problem = True)
        # else: 
        #     self.save_to_problems(can_skip_saving = False, can_delete_empty_problem = True)

        # Decrement the current problem index
        self.current_problem_index -= 1

        # Load the previous problem data
        previous_problem = self.problems[self.current_problem_index]
        self.question = previous_problem.get('question', '')
        self.solution = previous_problem.get('solution', '')
        if self.current_chapter != previous_problem.get('chapter', ''):
            # self.current_chapter = previous_problem.get('chapter', '')
            self.set_chapter(previous_problem.get('chapter', ''))
        self.katex_input.setPlainText(previous_problem.get(self.current_mode, ''))
        self.chapter_button.setText(self.current_chapter)

        self.update_images()

        try:
            next_problem = self.problems[self.current_problem_index + 1]
            if next_problem['chapter'] != self.current_chapter:
                self.set_chapter(self.current_chapter)
        except IndexError:
            pass


    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "", 
            "Image Files (*.webp *.jpeg *.jpg *.png *.heif *.heic)",
            options=options
        )

        if fileName:
            file_extension = os.path.splitext(fileName)[1].lower()
            if file_extension in ['.heif', '.heic']:
                QMessageBox.critical(self, "Error", "HEIF/HEIC images are not supported! In iPhone's Settings, go to Camera > Formats and select \"Most Compatible\".")
                return
            else:
                img = Image.open(fileName)

            img = ImageOps.exif_transpose(img)  # Correct the orientation of the image

            max_size = (1000, 1000)  # Maximum width and height
            img.thumbnail(max_size)  # Resize the image, maintaining aspect ratio

            uuid_str = str(uuid.uuid4())

            # This is the name of your application
            app_name = 'NotekeeEditor'

            # This is the path to the application data directory
            app_dir = appdirs.user_data_dir(app_name)

            # Create the images directory if it does not exist
            images_dir = os.path.join(app_dir, 'images')
            os.makedirs(images_dir, exist_ok=True)

            # Save the image in the images folder in the application data directory
            destination = os.path.join(images_dir, f'{uuid_str}.webp')

            current_problem = self.problems[self.current_problem_index]
            current_problem[self.current_mode + '_images'].append(uuid_str)

            img.save(destination, 'WEBP')  # Save the image in WebP format without checking the file size

            self.save_to_problems()

            # Create a QLabel with the image
            if self.images_scroll_area_widget is None:
                self.images_scroll_area_widget = self.build_images_scroll_area()
                self.right_layout.addWidget(self.images_scroll_area_widget, 3)
            else:
                self.right_layout.removeWidget(self.images_scroll_area_widget)
                self.images_scroll_area_widget.deleteLater()
                self.images_scroll_area_widget = self.build_images_scroll_area()
                self.right_layout.addWidget(self.images_scroll_area_widget, 3)
        

    def update_math(self):
        # Get KaTeX text from the QTextEdit
        katex_text = self.katex_input.toPlainText()

        # Determine whether to scroll to the bottom based on the cursor position in katex_input
        cursor_pos = self.katex_input.textCursor().position()
        text_length = len(katex_text)

        scroll_script = ""
        if cursor_pos > text_length / 2:
            # If the cursor is at the end of the text, prepare script to scroll to the bottom
            scroll_script = "<script>window.onload = function() { window.scrollTo(0, document.body.scrollHeight); }</script>"

        # Create HTML string with KaTeX script
        katex_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
        </head>
        <body>
            <div id="katex">{katex_text}</div>
            
            <script>
                renderMathInElement(document.getElementById("katex"));
            </script>
            {scroll_script}
        </body>
        </html>
        """

        # Set HTML content to the QWebEngineView
        self.webview.setHtml(katex_html)

        if self.current_mode == 'question':
            self.question = katex_text
        else:
            self.solution = katex_text

        if not self.next_button_enabled: # if button next is disabled
            if self.question != '':
                self.enable_button(self.next_button)
                self.next_button_enabled = True
            
        elif self.question == '' and self.current_problem_index == len(self.problems) - 1:
            self.disable_button(self.next_button)
            self.next_button_enabled = False


    def closeEvent(self, event):
        self.save_to_problems(can_delete_empty_problem = True)
        self.save_to_chapters()
        self.settings.save_window_position_and_size(self)
        self.settings.save_current_problem_index(self.current_problem_index)
        event.accept()