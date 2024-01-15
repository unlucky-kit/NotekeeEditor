# from settings import Settings


app_style_light = """
    QWidget {
        background-color: #F0F0F0;
        color: #000000;
    }
"""

app_style_dark = """
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff; 
    }  
"""


button_style_light = """
    QPushButton {
        background-color: #c0c0c0;
        border: none;
        color: black;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 0px 10px;
        height: 35px;
        margin: 0px 0px 0px 0px;
    }
    QPushButton:hover {
        background-color: #d0d0d0;
    }
    QPushButton:pressed {
        background-color: #b0b0b0;
    }
"""

button_style_dark = """
    QPushButton {
        background-color: #707070;
        border: none;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 0px 10px;
        height: 35px;
        margin: 0px 0px 0px 0px;
    }
    QPushButton:hover {
        background-color: #808080;
    }
    QPushButton:pressed {
        background-color: #707070;
    }
"""


focused_button_style_light = """
    QPushButton {
        font-size: 18px;
        color: rgba(0, 0, 0, 1);
        background-color: transparent;
        border: none;
    }
"""

focused_button_style_dark = """
    QPushButton {
        font-size: 18px;
        color: rgba(255, 255, 255, 1);
        background-color: transparent;
        border: none;
    }
"""


unfocused_button_style_light = """
    QPushButton {
        font-size: 16px;
        color: rgba(0, 0, 0, 0.5);
        background-color: transparent;
        border: none;
    }
"""

unfocused_button_style_dark = """
    QPushButton {
        font-size: 16px;
        color: rgba(255, 255, 255, 0.5);
        background-color: transparent;
        border: none;
    }
"""


disabled_button_style_light = """
    QPushButton {
        background-color: #d0d0d0;
        border: none;
        color: rgba(0, 0, 0, 0.5);
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 0px 10px;
        height: 35px;
        margin: 0px 0px 0px 0px;
    }
"""

disabled_button_style_dark = """
    QPushButton {
        background-color: #808080;
        border: none;
        color: rgba(255, 255, 255, 0.5);
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 0px 10px;
        height: 35px;
        margin: 0px 0px 0px 0px;
    }
"""


top_chapter_button_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #000000;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        padding: 0px;
        margin: 0px;
        width: 120px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: black;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#191919";
    }
"""

top_chapter_button_dark = """
    QPushButton {  
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        padding: 0px;
        margin: 0px;
        width: 120px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: white;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#FFFFFF";
    }
"""


unselected_top_chapter_button_style = """
        QPushButton {  
        background-color: transparent;
        border: none;
        color: #FF0000;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        padding: 0px;
        margin: 0px;
        width: 120px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: #FF0000;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: #FF1010
    }
"""


chapter_button_style_selected = """
    QPushButton {
        background-color: #202020;
        border: 1px solid #202020;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-size: 12px;
        margin: 0px;
        padding: 0px 5px;
        height: 30px;
        width: 100%;
    }

"""


chapter_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: 1px solid #AAAAAA;
        color: #000000;
        text-align: left;
        text-decoration: none;
        font-size: 12px;
        margin: 0px;
        padding: 0px 5px;
        height: 30px;
        width: 100%;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    }
    QPushButton:pressed {
        background-color: #C0C0C0;
    }
"""

chapter_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: 1px solid #101010;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-size: 12px;
        margin: 0px;
        padding: 0px 5px;
        height: 30px;
        width: 100%;
    }
    QPushButton:hover {
        background-color: #303030;
    }
    QPushButton:pressed {
        background-color: #202020;
    }
"""


link_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #0066CC;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
    }
    QPushButton:pressed {
        color: #0077fc;
    }

"""

link_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #0077CC;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
    }
    QPushButton:pressed {
        color: #0088fc;
    }
"""


checkmark_button_style_light = """
    QPushButton {
        font-size: 30px;
        background-color: transparent;
        border: 1px solid #AAAAAA;
        color: #000000;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        margin: 0px;
        height: 30px;
        width: 30px;
    }
    QPushButton:hover {
        background-color: #D0D0D0;
    }
    QPushButton:pressed {
        background-color: #C0C0C0;
    }
"""

checkmark_button_style_dark = """
    QPushButton {
        font-size: 30px;
        background-color: transparent;
        border: 1px solid #101010;
        color: #FFFFFF;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        margin: 0px;
        height: 30px;
        width: 30px;
    }
    QPushButton:hover {
        background-color: #303030;
    }
    QPushButton:pressed {
        background-color: #202020;
    }
"""


zoom_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #000000;
        text-align: right;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: #0077fc;
    }
    QPushButton:pressed {
        color: #0088fc;
    }
"""

zoom_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        text-align: right;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: #0077fc;
    }
    QPushButton:pressed {
        color: #0088fc;
    }
"""


delete_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #000000;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: #FF0000;
    }
    QPushButton:pressed {
        color: #FFAAAA;
    }
"""

delete_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        margin: 0px;
    }
    QPushButton:hover {
        text-decoration: underline;
        color: #FF0000;
    }
    QPushButton:pressed {
        color: #FF5555;
    }
"""


plain_chapter_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #000000;
        text-align: left;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        padding: 0px;
        margin: 0px;
        height: 15px;
        width: 100%;
    }
    QPushButton:hover {
        color: #101010;
    }
    QPushButton:pressed {
        color: #191919;
    }
"""

plain_chapter_button_style_dark = """
    QPushButton {  
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        padding: 0px;
        margin: 0px;
        height: 15px;
        width: 100%;
    }
    QPushButton:hover {
        color: #F0F0F0;
    }
    QPushButton:pressed {
        color: #CACACA;
    }
"""


plain_problem_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #000000;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""

plain_problem_button_style_dark = """
    QPushButton {  
        background-color: transparent;
        border: none;
        color: #FFFFFF;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""


current_problem_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #5038D0;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""

current_problem_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #7070C0;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""


error_with_problem_button_style_light = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #C02020;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""

error_with_problem_button_style_dark = """
    QPushButton {
        background-color: transparent;
        border: none;
        color: #B73030;
        text-align: left;
        text-decoration: none;
        font-size: 14px;
        height: 15px;
        margin-left: 20px;
        padding: 0px;
        width: 100%;
    }
"""

class Styles:
# Choose the styles based on the lightness
    def __init__(self, settings = None):
        self.settings_dict = settings.settings_dict

        if self.settings_dict['color_scheme'] == 'light':
            # Light mode
            self.button_style = button_style_light
            self.focused_button_style = focused_button_style_light
            self.unfocused_button_style = unfocused_button_style_light
            self.disabled_button_style = disabled_button_style_light
            self.top_chapter_button_style = top_chapter_button_light
            self.link_button_style = link_button_style_light
            self.checkmark_button_style = checkmark_button_style_light
            self.zoom_button_style = zoom_button_style_light
            self.delete_button_style = delete_button_style_light
            self.plain_chapter_button_style = plain_chapter_button_style_light
            self.plain_problem_button_style = plain_problem_button_style_light
            self.app_style = app_style_light
            self.chapter_button_style = chapter_button_style_light
            self.current_problem_button_style = current_problem_button_style_light
            self.error_with_problem_button_style = error_with_problem_button_style_light
        else:
            # Dark mode
            self.button_style = button_style_dark
            self.focused_button_style = focused_button_style_dark
            self.unfocused_button_style = unfocused_button_style_dark
            self.disabled_button_style = disabled_button_style_dark
            self.top_chapter_button_style = top_chapter_button_dark
            self.link_button_style = link_button_style_dark
            self.checkmark_button_style = checkmark_button_style_dark
            self.zoom_button_style = zoom_button_style_dark
            self.delete_button_style = delete_button_style_dark
            self.plain_chapter_button_style = plain_chapter_button_style_dark
            self.plain_problem_button_style = plain_problem_button_style_dark
            self.app_style = app_style_dark
            self.chapter_button_style = chapter_button_style_dark
            self.current_problem_button_style = current_problem_button_style_dark
            self.error_with_problem_button_style = error_with_problem_button_style_dark