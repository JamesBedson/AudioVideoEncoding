from enum import Enum

class Color(Enum):
    BACKGROUND_COLOR_PRIMARY    = "#181b1d"
    BACKGROUND_COLOR_SECONDARY  = "#123456"
    FONT_COLOR_PRIMARY          = "#ffffff"
    FONT_COLOR_SECONDARY        = "#dcdcdc"
    FILE_DROP_FRAME_DEFAULT     = "#2c353a"
    FILE_DROP_FRAME_DRAG        = "#2e557c"


class FontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    # Add more font sizes as needed

BUTTON_STYLE = """
#QPushButton {
    padding: 1.3em 3em;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 500;
    color: #000;
    background-color: #fff;
    border: none;
    border-radius: 45px;
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease 0s;
    cursor: pointer;
    outline: none;
}

#QPushButton:hover {
    background-color: #23c483;
    box-shadow: 0px 15px 20px rgba(46, 229, 157, 0.4);
    color: #fff;
    transform: translateY(-7px);
}

#QPushButton:pressed {
    transform: translateY(-1px);
}
"""
    