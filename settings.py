import json
from PyQt5.QtWidgets import QApplication
# from styles import Styles

class Settings:
    settings_dict = {}
    
    def __init__(self):
        try:
            # Load settings from json file
            with open('settings.json', 'r') as f:
                Settings.settings_dict = json.load(f)

        except json.JSONDecodeError or FileNotFoundError:
            self.default_settings()
            self.save_settings()


    def default_settings(self):
        Settings.settings_dict = {
            'window_position': [120, 120],
            'window_size': [800, 600],
            'color_scheme': 'dark',
            'export_index': 0,
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

        # Check if the window is outside the screen and adjust if necessary
        if pos.x() < 0:
            pos.setX(0)
        if pos.y() < 0:
            pos.setY(0)
        if pos.x() + size.width() > screen.width():
            pos.setX(screen.width() - size.width())
        if pos.y() + size.height() > screen.height():
            pos.setY(screen.height() - size.height())

        pos = [pos.x(), pos.y()]
        size = [size.width(), size.height()]
        

        Settings.settings_dict['window_position'] = pos
        Settings.settings_dict['window_size'] = size
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
        # Save changes to json file
        with open('settings.json', 'w') as f:
            json.dump(Settings.settings_dict, f, indent=4)



