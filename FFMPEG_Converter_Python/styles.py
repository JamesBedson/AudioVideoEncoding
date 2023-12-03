from enum import Enum
from PyQt6.QtGui import QFont

class Color(Enum):
    BACKGROUND_COLOR_PRIMARY    = "#18191c"
    BACKGROUND_COLOR_SECONDARY  = "#202124"
    ACCENT_COLOR_PRIMARY        = "#6c387d"
    ACCENT_COLOR_PRIMARY_DARK   = "#353638"
    ACCENT_COLOR_SECONDARY      = "#7c4d8b"
    ACCENT_COLOR_TERCIARY       = "#ba207f"
    ACCENT_COLOR_TERCIARY_LIGHT = "#c4438c"
    FONT_COLOR_PRIMARY          = "#ffffff"
    FONT_COLOR_SECONDARY        = "#dcdcdc"
    FILE_DROP_FRAME_DEFAULT     = "#2c353a"
    FILE_DROP_FRAME_DRAG        = "#2e557c"

class Font(Enum):
    DEFAULT_FONT = "Gill Sans"
    H1_FONT_Q = QFont("Gill Sans", weight = 600, pointSize = 15)
    H2_FONT_Q = QFont("Gill Sans", weight = 400, pointSize = 13)
    H3_FONT_Q = QFont("Gill Sans", weight = 200, pointSize = 10)
    
BORDER_RADIUS   = 6
BORDER_WIDTH    = 1

GLOBAL_STYLE = f"""
MainWindow {{
    background-color: {Color.BACKGROUND_COLOR_PRIMARY.value};
}}

QTabBar#menu {{
    background-color: {Color.BACKGROUND_COLOR_PRIMARY.value};
    color: {Color.FONT_COLOR_PRIMARY.value};
    font-family: "{Font.DEFAULT_FONT.value}";
    font-size: 12px;
}}

QTabBar#menu::tab {{
    background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};
    border: 1px solid {Color.BACKGROUND_COLOR_PRIMARY.value};
    border-radius: {BORDER_RADIUS};
    padding: 6px;
}}

QTabBar#menu::tab:selected {{
    background-color: {Color.BACKGROUND_COLOR_SECONDARY.value};
}}

QTabBar#menu::tab:hover {{
    background-color: {Color.ACCENT_COLOR_TERCIARY_LIGHT.value};
}}

QComboBox {{
    background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};
    color: {Color.FONT_COLOR_PRIMARY.value};
    border: 1px solid {Color.BACKGROUND_COLOR_PRIMARY.value};
    border-radius: 4px;
    padding: 4px;
    selection-background-color: {Color.ACCENT_COLOR_PRIMARY.value};
}}

QComboBox QAbstractItemView {{
    background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};
    width: 40px;
}}


QComboBox::down-arrow {{
    image: url("/Users/james/Documents/Development/University/AudioVideoEncoding/FFMPEG_Converter_Python/assets/down-arrow_white.png");
    width: 10px;
    height: 10px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: center right;
    background-color: {Color.FILE_DROP_FRAME_DEFAULT.value};  /* Add the desired color for the box */
    border-radius: 4px;
}}

QLabel {{
    font-family: "Gill Sans";
}}

QPushButton {{
    padding: 0.8em 1.2em;
    font-size: 9px;
    text-transform: uppercase;
    font-weight: 500;
    color: {Color.FONT_COLOR_PRIMARY.value};
    background-color: {Color.ACCENT_COLOR_PRIMARY.value};
    border-radius: {BORDER_RADIUS};
    outline: 1px;
}}

QPushButton#chooseFile {{
    text-transform: uppercase;
    font-weight: 500;
    color: {Color.FONT_COLOR_PRIMARY.value};
    background-color: {Color.ACCENT_COLOR_PRIMARY.value};
    border-radius: {BORDER_RADIUS};
    outline: 1px;
}}

QPushButton#chooseFile:hover {{
    background-color: {Color.ACCENT_COLOR_SECONDARY.value};
    color: {Color.FONT_COLOR_PRIMARY.value};
}}

QPushButton#convertButton {{
    padding: 1.3em 2em;
    font-size: 9px;
    text-transform: uppercase;
    font-weight: 500;
    color: {Color.FONT_COLOR_PRIMARY.value};
    background-color: {Color.ACCENT_COLOR_TERCIARY.value};
    border-radius: {BORDER_RADIUS};
    outline: 1px;
}}

QPushButton#convertButton:hover {{
    background-color: {Color.ACCENT_COLOR_TERCIARY_LIGHT.value};
    color: {Color.FONT_COLOR_PRIMARY.value};
}}

QVideoWidget {{
    border-radius: 10px;
}}

QPushButton:hover {{
    background-color: {Color.ACCENT_COLOR_SECONDARY.value};
    color: {Color.FONT_COLOR_PRIMARY.value};
}}

QSlider:groove{{
    background: {Color.BACKGROUND_COLOR_SECONDARY.value};
}}

QSlider::groove:horizontal {{
    border: 1px solid {Color.BACKGROUND_COLOR_PRIMARY.value};
    height: 10px;
    background: {Color.ACCENT_COLOR_PRIMARY_DARK.value};
    margin: 0px;
    border-radius: 4px;
}}

QSlider::handle:horizontal {{
    background: {Color.ACCENT_COLOR_PRIMARY.value};
    width: 16px;
    height: 13px;
    border-radius: 4px;
}}

QSlider::sub-page:horizontal {{
    background: {Color.ACCENT_COLOR_SECONDARY.value};
    border: 1px solid {Color.BACKGROUND_COLOR_PRIMARY.value};  /* Add a border */
    border-radius: 4px;
}}

"""
