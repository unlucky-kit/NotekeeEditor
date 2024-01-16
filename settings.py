import json
from PyQt5.QtWidgets import QApplication
import appdirs
import os

class Settings:
    settings_dict = {}
    
    def __init__(self):
        try:
            # This is the name of your application
            app_name = 'NotekeeEditor'

            # This is the path to the application data directory
            app_dir = appdirs.user_data_dir(app_name)

            # Load settings from json file in the application data directory
            with open(os.path.join(app_dir, 'settings.json'), 'r') as f:
                Settings.settings_dict = json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            self.default_settings()
            self.save_settings()


    def default_settings(self):
        Settings.settings_dict = {
            'window_position': [120, 120],
            'window_size': [800, 600],
            'color_scheme': 'dark',
            'export_index': 1,
            'current_problem_index': 0
        }

    def increment_export_index(self):
        Settings.settings_dict['export_index'] += 1
        self.save_settings()

    def get_export_index(self):
        return Settings.settings_dict['export_index']

    def get_window_position(self):
        return Settings.settings_dict['window_position']
    
    def get_window_size(self):
        return Settings.settings_dict['window_size']
    
    def get_color_scheme(self):
        return Settings.settings_dict['color_scheme']
    
    def get_current_problem_index(self):
        return Settings.settings_dict['current_problem_index']
    
    
    def save_window_position_and_size(self, window):
        screen = QApplication.desktop().screenGeometry()

        # Get the window position and size
        pos = window.pos()
        size = window.size()

        # Get the height of the title bar
        title_bar_height = window.frameGeometry().height() - window.geometry().height()

        # Adjust the y-coordinate of the position
        pos.setY(pos.y() + title_bar_height)

        # Check if the window is outside the screen and adjust if necessary
        if pos.x() < 0:
            pos.setX(0)
        if pos.y() < 0:
            pos.setY(0)
        if pos.x() + size.width() > screen.width():
            pos.setX(screen.width() - size.width())
        if pos.y() + size.height() > screen.height():
            pos.setY(screen.height() - size.height())

        # Save the position and size to the settings
        Settings.settings_dict['window_position'] = [pos.x(), pos.y()]
        Settings.settings_dict['window_size'] = [size.width(), size.height()]

        self.save_settings()

    
    def save_current_problem_index(self, index):
        Settings.settings_dict['current_problem_index'] = index
        self.save_settings()

    def toggle_color_scheme(self):
        if Settings.settings_dict['color_scheme'] == 'dark':
            Settings.settings_dict['color_scheme'] = 'light'
        else:
            Settings.settings_dict['color_scheme'] = 'dark'

        self.save_settings()


    def save_settings(self):
        # This is the name of your application
        app_name = 'NotekeeEditor'

        # This is the path to the application data directory
        app_dir = appdirs.user_data_dir(app_name)

        # Check if the directory exists and create it if it doesn't
        os.makedirs(app_dir, exist_ok=True)

        # Save changes to json file in the application data directory
        with open(os.path.join(app_dir, 'settings.json'), 'w') as f:
            json.dump(Settings.settings_dict, f, indent=4)

