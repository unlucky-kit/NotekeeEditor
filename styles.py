from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QApplication

# Get the lightness of the background color
lightness = QApplication.palette().color(QPalette.Window).lightness()

# Define styles for light mode
button_style_light = """
    QPushButton {
        background-color: #c0c0c0;
        border: none;
        color: black;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 10px 10px;
        margin: 0px;
    }
    QPushButton:hover {
        background-color: #d0d0d0;
    }
    QPushButton:pressed {
        background-color: #b0b0b0;
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

unfocused_button_style_light = """
    QPushButton {
        font-size: 16px;
        color: rgba(0, 0, 0, 0.5);
        background-color: transparent;
        border: none;
    }
"""

# Define styles for dark mode
button_style_dark = """
    QPushButton {
        background-color: #707070;
        border: none;
        color: white;
        text-align: center;
        text-decoration: none;
        font-size: 12px;
        padding: 10px 10px;
        margin: 0px;
    }
    QPushButton:hover {
        background-color: #808080;
    }
    QPushButton:pressed {
        background-color: #707070;
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
        padding: 10px 10px;
        margin: 0px;
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
        padding: 10px 10px;
        margin: 0px;
    }
"""

# Accepts an integer and returns a string
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

chapter_button_style = """
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
    }
    QPushButton:pressed {
        color: #111111;
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
        text-decoration: underline;
        color: black;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#191919";
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
        text-decoration: underline;
        color: white;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#FFFFFF";
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
    QPushButton:hover {
        text-decoration: underline;
        color: black;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#191919";
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
    QPushButton:hover {
        text-decoration: underline;
        color: white;
    }
    QPushButton:pressed {
        text-decoration: underline;
        color: "#FFFFFF";
    }
"""

# Choose the styles based on the lightness
if False:
    print(lightness)
    # Light mode
    button_style = button_style_light
    focused_button_style = focused_button_style_light
    unfocused_button_style = unfocused_button_style_light
    disabled_button_style = disabled_button_style_light
    top_chapter_button_style = top_chapter_button_light
    link_button_style = link_button_style_light
    checkmark_button_style = checkmark_button_style_light
    zoom_button_style = zoom_button_style_light
    delete_button_style = delete_button_style_light
    plain_chaspter_button_style = plain_chapter_button_style_light
    plain_problem_button_style = plain_problem_button_style_light
else:
    print(lightness)
    # Dark mode
    button_style = button_style_dark
    focused_button_style = focused_button_style_dark
    unfocused_button_style = unfocused_button_style_dark
    disabled_button_style = disabled_button_style_dark
    top_chapter_button_style = top_chapter_button_dark
    link_button_style = link_button_style_dark
    checkmark_button_style = checkmark_button_style_dark
    zoom_button_style = zoom_button_style_dark
    delete_button_style = delete_button_style_dark
    plain_chapter_button_style = plain_chapter_button_style_dark
    plain_problem_button_style = plain_problem_button_style_dark