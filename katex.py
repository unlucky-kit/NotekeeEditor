from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QScrollArea, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QFont, QPixmap, QPainter, QImage
from styles import *
import json
import base64
from PIL import Image
from OneLineTextEdit import *
import os
import uuid
               

class CustomScrollArea(QScrollArea):
    def __init__(self, main_instance, parent=None):
        super().__init__(parent)
        self.main_instance = main_instance
        self.scroll_layout = None

    def showEvent(self, event):
        super().showEvent(event)
        if self.scroll_layout:
            self.main_instance.scale_images(self.scroll_layout, self)


class MathPlayground(QMainWindow):
    def __init__(self):
        super().__init__()

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
            # Load problems and chapters from json files
            problems_file = open('problems.json', 'r')
            chapters_file = open('chapters.json', 'r')

            # Put the data from the json files into lists
            self.problems = json.load(problems_file)
            self.chapters = json.load(chapters_file)

            # Get the last problem's index
            self.current_problem_index = len(self.problems) - 1

            # Get the last problem's data
            current_problem = self.problems[self.current_problem_index]
            self.question = current_problem.get('question', '')
            self.solution = current_problem.get('solution', '')
            self.current_chapter = current_problem.get('chapter', '')

        except FileNotFoundError:
            print("JSON FILE DOES NOT EXIST")
            self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]
            self.chapters = []
            
        except json.JSONDecodeError:
            print("FAILED TO LOAD JSON FILE")
            self.problems = [{'question': '', 'solution': '', 'chapter': '', 'question_images': [], 'solution_images': []}]
            self.chapters = []

        self.init_ui()


    def top_button_layout(self):
        button_layout = QHBoxLayout()

        chapter_button_title = self.current_chapter if self.current_chapter != '' else 'Set Chapter'
        self.chapter_button = QPushButton(chapter_button_title, self)

        self.question_button = QPushButton('Question', self)
        self.solution_button = QPushButton('Solution', self)
        
        self.previous_button = QPushButton('Previous', self)
        self.next_button = QPushButton('Next', self)

        # Connect the buttons to their respective functions
        self.question_button.clicked.connect(lambda: self.toggle_buttons(self.question_button))
        self.solution_button.clicked.connect(lambda: self.toggle_buttons(self.solution_button))
        self.previous_button.clicked.connect(lambda: self.previous_problem())
        self.next_button.clicked.connect(lambda: self.next_problem())
        self.chapter_button.clicked.connect(lambda: self.toggle_chapter_picker())

        if self.current_chapter != '':
            self.chapter_button.setStyleSheet(top_chapter_button_style)
        else:
            self.chapter_button.setStyleSheet(unselected_top_chapter_button_style)

        # Set previous and next button styles
        if self.current_problem_index == 0:
            self.disable_button(self.previous_button)
            self.previous_button_enabled = False
        else:
            self.previous_button.setStyleSheet(button_style)
        
        if self.current_problem_index == len(self.problems) - 1 and self.question == '':
            self.disable_button(self.next_button)
            self.next_button_enabled = False
        else:
            self.next_button.setStyleSheet(button_style)

        # Set focus button style
        self.question_button.setStyleSheet(focused_button_style)
        self.solution_button.setStyleSheet(unfocused_button_style)

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
        # Remove image from problems dictionary
        current_problem = self.problems[self.current_problem_index]
        current_problem[self.current_mode + '_images'].remove(image)

        # Delete image file
        os.remove(f'images/{image}.jpg')

        if self.zoomed_image_widget is not None:
            self.zoom_out_image()

        self.update_images()


    def zoom_in_image(self, image):
        # Hide the right_layout widget
        self.right_layout_widget.hide()

        # Create a new QWidget for the zoomed image
        self.zoomed_image_widget = QWidget()

        # Create a QVBoxLayout for the zoomed image widget
        zoomed_image_layout = QVBoxLayout(self.zoomed_image_widget)

        # Load the image
        label = QLabel(self)
        pixmap = QPixmap(f'images/{image}.jpg')
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
        zoom_out_button.setStyleSheet(zoom_button_style)
        delete_button.setStyleSheet(delete_button_style)
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


    def images_scroll_area(self):
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
        for image in current_image_list:
            image_widget = QWidget()
            image_layout = QVBoxLayout(image_widget)
            image_layout.setContentsMargins(5, 0, 5, 0)
            image_layout.setSpacing(0)  # Set spacing to 0 to remove space between image and buttons
            image_layout.setAlignment(Qt.AlignTop)  # Align the image and buttons to the top

            label = QLabel(self)
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            pixmap = QPixmap(f'images/{image}.jpg')
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
            zoom_button.setStyleSheet(zoom_button_style)
            delete_button.setStyleSheet(delete_button_style)
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
            self.images_scroll_area_widget = self.images_scroll_area()
            self.right_layout.addWidget(self.images_scroll_area_widget, 3)


    def chapters_scroll_area(self):
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

        checkmark_button.setStyleSheet(checkmark_button_style)
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
                temp_chapter_button.setStyleSheet(chapter_button_style)

            temp_chapter_button.setCursor(Qt.PointingHandCursor)
            temp_chapter_button.clicked.connect(lambda _, chapter=chapter: self.set_chapter(chapter))
            self.chapters_layout.addWidget(temp_chapter_button)

        self.chapters_layout.addStretch(1)

        self.chapters_scroll_area.setVisible(False)

        return self.chapters_scroll_area


    def workspace_layout(self):
        self.workspace_layout = QHBoxLayout()

        # Create a QWebEngineView for displaying HTML
        self.right_layout = QVBoxLayout()
        self.webview = QWebEngineView(self)

        # Create a QTextEdit for KaTeX input
        self.katex_input = QTextEdit(self)
        font = QFont("Courier New")
        font.setPointSize(15)
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
            self.images_scroll_area_widget = self.images_scroll_area()
            self.right_layout.addWidget(self.images_scroll_area_widget, 3)

        # Add chapters_scroll_area to the workspace_layout instead of chapters_layout
        self.workspace_layout.addWidget(self.chapters_scroll_area(), 1)
        self.workspace_layout.addWidget(self.katex_input, 1)
        self.workspace_layout.addWidget(self.right_layout_widget, 1)

        return self.workspace_layout


    def bottom_button_layout(self):
        button_layout = QHBoxLayout()

        self.all_problems_button = QPushButton('All problems', self)
        self.export_button = QPushButton('Export', self)
        self.color_scheme_button = QPushButton('Dark Mode', self)

        self.upload_image_button = QPushButton('Upload Image', self)

        button_layout.addWidget(self.all_problems_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.color_scheme_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.upload_image_button)

        self.upload_image_button.clicked.connect(lambda: self.upload_image())
        self.all_problems_button.clicked.connect(lambda: self.toggle_all_problems_layout_widget())

        for button in [self.all_problems_button, self.export_button, self.color_scheme_button, self.upload_image_button]:
            button.setCursor(Qt.PointingHandCursor)
            button.setStyleSheet(link_button_style)

        return button_layout


    def init_ui(self):
        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.secondary_layout_widget = QWidget(self)
        secondary_layout = QVBoxLayout(self.secondary_layout_widget)
        secondary_layout.setContentsMargins(0, 0, 0, 0)

        # Removing vertical padding from the buttons
        spacer1 = QSpacerItem(-5, -5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer2 = QSpacerItem(-10, -10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer3 = QSpacerItem(-5, -5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        secondary_layout.addItem(spacer1)
        secondary_layout.addLayout(self.top_button_layout())
        secondary_layout.addItem(spacer2)

        secondary_layout.addLayout(self.workspace_layout())

        secondary_layout.addItem(spacer3)
        secondary_layout.addLayout(self.bottom_button_layout())

        self.layout.addWidget(self.secondary_layout_widget)

        self.setWindowTitle("Notekee Editor")
        self.setGeometry(-1600, -400, 800, 400)
        

    def toggle_all_problems_layout_widget(self):
        if self.all_problems_layout_widget is None:
            if self.current_chapter == '':
                return
            
            self.remove_empty_chapters()

            if self.current_chapter != '' and self.problems[self.current_problem_index]['chapter'] == '':
                self.problems[self.current_problem_index]['chapter'] = self.current_chapter

            
            if self.current_mode == 'question':
                self.problems[self.current_problem_index]['question'] = self.question
            

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
                chapter_button.setStyleSheet(plain_chapter_button_style)
                chapter_button.setCursor(Qt.PointingHandCursor)

                for i in range(len(chapter_problems[chapter])):
                    problem = chapter_problems[chapter][i]
                    problem_button = QPushButton(f'{i + 1}. {problem['question'].replace('\n', '')}', self)
                    problem_button.clicked.connect(lambda _, problem=problem: self.load_problem(problem))
                    problem_button.setCursor(Qt.PointingHandCursor)
                    problem_button.setStyleSheet(plain_problem_button_style)

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

                chapter_button.clicked.connect(lambda _, button=chapter_button, layout=chapter_problem_layout, chapter_name=chapter: toggle_visibility(button, layout, chapter_name))

                all_problems_scroll_area_layout.addWidget(chapter_button)
                all_problems_scroll_area_layout.addLayout(chapter_problem_layout)

            all_problems_scroll_area_layout.addStretch(1)

            all_problems_layout.addWidget(all_problems_scroll_area)
            all_problems_layout.setContentsMargins(0, 0, 0, 0)

            # Create a "Back" button and add it to the layout
            back_button = QPushButton("Back", self)
            back_button.clicked.connect(lambda: self.toggle_all_problems_layout_widget())
            back_button.setCursor(Qt.PointingHandCursor)
            back_button.setStyleSheet(link_button_style)

            back_button_layout = QHBoxLayout()
            back_button_layout.addWidget(back_button)
            back_button_layout.addStretch(1)

            all_problems_layout.addLayout(back_button_layout)

            self.layout.addWidget(self.all_problems_layout_widget)

            self.secondary_layout_widget.setVisible(False)

        else:
            self.layout.removeWidget(self.all_problems_layout_widget)
            self.all_problems_layout_widget.deleteLater()
            self.all_problems_layout_widget = None

            self.secondary_layout_widget.setVisible(True)


    def load_problem(self, problem):
        pass


    def save_to_chapters(self):
        with open('chapters.json', 'w') as file:
            json.dump(self.chapters, file, indent=4)


    def save_to_problems(self):
        if self.solution == '' and self.question == '':
            solution_images = self.problems[self.current_problem_index]['solution_images']
            question_images = self.problems[self.current_problem_index]['question_images']
            if solution_images == [] and question_images == []:
                return
            
        
        current_problem = self.problems[self.current_problem_index]

        current_problem['question'] = self.question
        current_problem['solution'] = self.solution
        current_problem['chapter'] = self.current_chapter

        # Remove empty problems from json's version of data
        clean_problems = [problem for problem in self.problems if problem['question'] != '' or problem['solution'] != '']

        with open('problems.json', 'w') as file:
            json.dump(clean_problems, file, indent=4)


    def create_new_chapter(self, chapter_name):

        chapter_name = chapter_name.strip()
        self.chapter_input.clear()
        if chapter_name == '' or chapter_name in self.chapters:
            return

        self.chapters.insert(0, chapter_name)  # Add chapter to the top of the list


        new_chapter_button = QPushButton(chapter_name, self)
        new_chapter_button.setStyleSheet(chapter_button_style_selected)
        new_chapter_button.setCursor(Qt.PointingHandCursor)
        new_chapter_button.clicked.connect(lambda _, chapter=chapter_name: self.set_chapter(chapter))
        self.chapters_layout.insertWidget(1, new_chapter_button)  # Insert button at the top
        
        self.set_chapter(chapter_name)

        self.remove_empty_chapters()
        self.save_to_chapters()


    def set_chapter(self, chapter):
        self.current_chapter = chapter
        index_of_current_chapter = self.chapters.index(self.current_chapter)
        self.chapters_layout.itemAt(index_of_current_chapter + 1).widget().setStyleSheet(chapter_button_style)
        self.chapters_layout.itemAt(self.chapters.index(chapter) + 1).widget().setStyleSheet(chapter_button_style_selected)
        self.current_chapter = chapter 
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


    def toggle_buttons(self, clicked_button):
        if clicked_button is self.question_button:
            if self.current_mode == 'solution':
                self.current_mode = 'question'
            else:
                return

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

            # Changing the style of the buttons
            self.question_button.setStyleSheet(focused_button_style)
            self.solution_button.setStyleSheet(unfocused_button_style)

            # Saving the question to the question string and setting the text to the solution
            self.solution = self.katex_input.toPlainText()
            self.katex_input.setPlainText(self.question)

        else:
            if self.current_mode == 'question':
                self.current_mode = 'solution'
            else:  
                return

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

            # Changing the style of the buttons
            self.solution_button.setStyleSheet(focused_button_style)
            self.question_button.setStyleSheet(unfocused_button_style)

            # Saving the solution to the solution string and setting the text to the question
            self.question = self.katex_input.toPlainText()
            self.katex_input.setPlainText(self.solution)
            
        self.update_images()
        self.save_to_problems()


    def toggle_chapter_picker(self):
        print(self.show_chapter_picker)
        if not self.show_chapter_picker: # Show chapter picker
            self.remove_empty_chapters()

            self.workspace_layout.removeItem(self.workspace_layout.itemAt(0))
            self.workspace_layout.insertWidget(0, self.chapters_scroll_area, 1)  # Use insertWidget instead of insertLayout
            
            self.katex_input.setVisible(False)
            self.chapter_button.setText('Done')
            self.chapter_button.setStyleSheet(top_chapter_button_style)

            self.chapters_scroll_area.setVisible(True)

            print("SHOW CHAPTER PICKER")
            self.show_chapter_picker = True

        else: # Hide chapter picker
            self.chapter_input.clear()
            self.workspace_layout.removeItem(self.workspace_layout.itemAt(0))
            self.workspace_layout.insertWidget(0, self.katex_input, 1)
            self.katex_input.setPlainText(self.question if self.current_mode == 'question' else self.solution)
            self.katex_input.setVisible(True)

            if self.current_chapter != '':
                self.chapter_button.setStyleSheet(top_chapter_button_style)
            else:
                self.chapter_button.setStyleSheet(unselected_top_chapter_button_style)

            self.chapter_button.setText(self.current_chapter if self.current_chapter != '' else 'Set Chapter')

            self.chapters_scroll_area.setVisible(False)

            print("HIDE CHAPTER PICKER")
            self.show_chapter_picker = False


    def disable_button(self, button):
        button.setStyleSheet(disabled_button_style)
        button.setEnabled(False)


    def enable_button(self, button):
        button.setStyleSheet(button_style)
        button.setEnabled(True)


    def next_problem(self):
        self.save_to_problems()
        
        if self.question == '' or self.current_chapter == '':
            return

        if self.zoomed_image_widget is not None:
            self.zoom_out_image()

        # Increment the current problem index
        self.current_problem_index += 1

        # If there is a next problem, load it
        if self.current_problem_index <= len(self.problems) - 1:
            next_problem = self.problems[self.current_problem_index]
            self.question = next_problem.get('question', '')
            self.solution = next_problem.get('solution', '')
            self.current_chapter = next_problem.get('chapter', '')
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
                self.question_button.setStyleSheet(focused_button_style)
                self.solution_button.setStyleSheet(unfocused_button_style)
            
            self.disable_button(self.next_button)
            self.next_button_enabled = False

        self.update_images()

        if not self.previous_button_enabled:
            self.enable_button(self.previous_button)
            self.previous_button_enabled = True


    def previous_problem(self):
        self.save_to_problems()

        if self.current_problem_index == 0:
            return
        elif self.current_problem_index == 1:
            self.disable_button(self.sender())
            self.previous_button_enabled = False

            if self.zoomed_image_widget is not None:
                self.zoom_out_image()

            if self.next_button_enabled:
                self.disable_button(self.next_button)
                self.next_button_enabled = False

        solution_images = self.problems[self.current_problem_index]['solution_images']
        question_images = self.problems[self.current_problem_index]['question_images']
        if (self.current_problem_index == len(self.problems) - 1) and self.question == '' and solution_images == [] and question_images == []:
            self.problems.pop()
            
        # Decrement the current problem index
        self.current_problem_index -= 1

        # Load the previous problem data
        previous_problem = self.problems[self.current_problem_index]
        self.question = previous_problem.get('question', '')
        self.solution = previous_problem.get('solution', '')
        self.current_chapter = previous_problem.get('chapter', '')
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
            "All Files (*);;Image Files (*.gif *.jpeg *.jpg *.png *.heif)",
            options=options
        )

        if fileName:
            img = Image.open(fileName)
            rgb_img = img.convert('RGB') # Convert image to RGB color space
            uuid_str = str(uuid.uuid4())
            destination = 'images/' + uuid_str + '.jpg'

            current_problem = self.problems[self.current_problem_index]
            current_problem[self.current_mode + '_images'].append(uuid_str)

            for quality in range(100, 0, -10):
                rgb_img.save(destination, 'JPEG', quality=quality)
                if os.path.getsize(destination) <= 128 * 1024:  # Check if file size is less than or equal to 128KB
                    break
            else:
                print("Could not compress the image enough to get under 128KB")


            # Create a QLabel with the image
            if self.images_scroll_area_widget is None:
                self.images_scroll_area_widget = self.images_scroll_area()
                self.right_layout.addWidget(self.images_scroll_area_widget, 3)
            else:
                self.right_layout.removeWidget(self.images_scroll_area_widget)
                self.images_scroll_area_widget.deleteLater()
                self.images_scroll_area_widget = self.images_scroll_area()
                self.right_layout.addWidget(self.images_scroll_area_widget, 3)
        

    def update_math(self):
        # Get KaTeX text from the QTextEdit
        katex_text = self.katex_input.toPlainText()

        if self.current_mode == 'question':
            self.question = katex_text
        else:
            self.solution = katex_text

        # Create HTML string with KaTeX script
        katex_html = katex_html = f"""
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
        </body>
        </html>
        """

        if not self.next_button_enabled: # if button next is disabled
            if self.question != '':
                self.enable_button(self.next_button)
                self.next_button_enabled = True
            
        elif self.question == '':
            self.disable_button(self.next_button)
            self.next_button_enabled = False

        # Set HTML content to the QWebEngineView
        self.webview.setHtml(katex_html)


    def closeEvent(self, event):
        self.save_to_problems()
        event.accept()

# Run the application if this file is executed directly
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyleSheet("""
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    QPushButton {
        background-color: #353535;
        border: 1px solid #474747;
    }
    QPushButton:hover {
        background-color: #3e3e3e;
    }
    QPushButton:pressed {
        background-color: #4a4a4a;
    }
""")
    playground = MathPlayground()
    playground.show()
    sys.exit(app.exec_())
