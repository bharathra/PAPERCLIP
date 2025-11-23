
class Styles:
    # Colors
    YELLOW_BG = "#fff740"
    YELLOW_HEADER = "#e6de3a"

    BLUE_BG = "#a0cfff"
    BLUE_HEADER = "#90badd"

    GREEN_BG = "#b7ffb7"
    GREEN_HEADER = "#a4e5a4"

    PINK_BG = "#ffcce0"
    PINK_HEADER = "#e5b7c9"

    TEXT_COLOR = "#333333"

    # Fonts
    FONT_FAMILY = "Intel One Mono, Montserrat, Segoe UI, San Francisco, Helvetica, Arial, sans-serif"
    FONT_SIZE = "16px"

    # Stylesheets
    NOTE_WINDOW = """
        QMainWindow {{
            background-color: transparent;
        }}
        QWidget#CentralWidget {{
            background-color: {bg_color};
            border-radius: 10px;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }}
    """

    TITLE_BAR = """
        QFrame#TitleBar {{
            background-color: {header_color};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }}
        QPushButton {{
            background-color: transparent;
            border: none;
            color: #555;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton:hover {{
            color: #000;
            background-color: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }}
    """

    CONTENT_AREA = """
        QTextEdit {{
            background-color: transparent;
            border: none;
            color: {text_color};
            font-family: {font_family};
            font-size: {font_size};
            padding: 15px;
            selection-background-color: rgba(0, 0, 0, 0.1);
        }}
    """

    SCROLLBAR = """
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 8px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: rgba(0, 0, 0, 0.1);
            min-height: 20px;
            border-radius: 4px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """
