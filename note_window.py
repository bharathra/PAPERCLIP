import sys
import os

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QFrame, QSizeGrip, QApplication, QMenu, QLabel)
from PyQt6.QtCore import Qt, QPoint, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QCursor, QAction, QTextBlockFormat, QShortcut, QKeySequence, QPixmap, QIcon

from styles import Styles


class TitleBar(QFrame):
    def __init__(self, parent=None, color_key="YELLOW"):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(42)
        self.parent_window = parent
        self.setCursor(Qt.CursorShape.OpenHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        # App Icon
        self.icon_label = QLabel()
        self.icon_label.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), "icons/paper_clip.png")
                                          ).scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        layout.addWidget(self.icon_label)

        layout.addSpacing(5)

        # Spacer to align everything to the right
        layout.addStretch()

        # Thin Separator
        self.add_separator(layout, thickness=1)

        # Add Button
        self.add_btn = QPushButton()
        self.add_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/add.png")))
        self.add_btn.setIconSize(QSize(16, 16))
        self.add_btn.setFixedSize(20, 20)
        self.add_btn.setCursor(Qt.CursorShape.ArrowCursor)
        self.add_btn.setToolTip("New Note")
        self.add_btn.clicked.connect(self.parent_window.spawn_new_note)
        layout.addWidget(self.add_btn)

        # Thin Separator
        self.add_separator(layout, thickness=1)

        # Color Button
        self.color_btn = QPushButton()
        self.color_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/color_palette.png")))
        self.color_btn.setIconSize(QSize(16, 16))
        self.color_btn.setFixedSize(20, 20)
        self.color_btn.setCursor(Qt.CursorShape.ArrowCursor)
        self.color_btn.setToolTip("Change Color")
        self.color_btn.clicked.connect(self.show_color_menu)
        layout.addWidget(self.color_btn)

        # Thin Separator
        self.add_separator(layout, thickness=1)

        # Checkbox Button
        self.checkbox_btn = QPushButton()
        self.checkbox_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/check_box.png")))
        self.checkbox_btn.setIconSize(QSize(16, 16))
        self.checkbox_btn.setFixedSize(20, 20)
        self.checkbox_btn.setCursor(Qt.CursorShape.ArrowCursor)
        self.checkbox_btn.setToolTip("Toggle Checkboxes")
        self.checkbox_btn.clicked.connect(self.toggle_checkboxes)
        layout.addWidget(self.checkbox_btn)

        # Thin Separator
        self.add_separator(layout, thickness=1)

        # Delete Button
        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "icons/delete.png")))
        self.delete_btn.setIconSize(QSize(16, 16))
        self.delete_btn.setFixedSize(20, 20)
        self.delete_btn.setCursor(Qt.CursorShape.ArrowCursor)
        self.delete_btn.setToolTip("Delete Note")
        self.delete_btn.clicked.connect(self.parent_window.delete_note)
        layout.addWidget(self.delete_btn)

        # Thick Separator
        self.add_separator(layout, thickness=4)

        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(20, 20)
        self.close_btn.setCursor(Qt.CursorShape.ArrowCursor)
        self.close_btn.setToolTip("Close Window")
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        self.start_pos = None

    def add_separator(self, layout, thickness=1):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setFixedWidth(thickness)
        line.setStyleSheet(f"background-color: rgba(0, 0, 0, 0.2); border: none;")
        layout.addWidget(line)

    def toggle_checkboxes(self):
        self.parent_window.content.toggle_checklist_mode()

    def show_color_menu(self):
        menu = QMenu(self)

        # Define colors and their display names/values
        color_map = {
            "Yellow": Styles.YELLOW_BG,
            "Blue": Styles.BLUE_BG,
            "Green": Styles.GREEN_BG,
            "Pink": Styles.PINK_BG
        }

        for name, hex_color in color_map.items():
            # Create a pixmap for the color
            pixmap = QPixmap(20, 20)
            pixmap.fill(QColor(hex_color))

            # Create icon from pixmap
            icon = QIcon(pixmap)

            # Create action with icon and no text (or name as tooltip if needed, but request said replace text)
            # Using a space as text to ensure the icon shows up nicely without label
            action = QAction(icon, "   " + name, self)

            action.triggered.connect(lambda checked, c=name: self.parent_window.change_color(c))
            menu.addAction(action)

        menu.exec(self.color_btn.mapToGlobal(QPoint(0, self.color_btn.height())))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            self.start_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()

            # Try system move first (better for Wayland/modern WMs)
            window_handle = self.parent_window.windowHandle()
            if window_handle and window_handle.startSystemMove():
                event.accept()
                return

            event.accept()

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.start_pos = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.start_pos:
            self.parent_window.move(event.globalPosition().toPoint() - self.start_pos)
            event.accept()


class NoteContent(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.checklist_mode = False

        # Set line spacing
        block_fmt = QTextBlockFormat()
        block_fmt.setLineHeight(150, 1)  # 150% line height (1 = ProportionalHeight)
        self.document().setDefaultTextOption(self.document().defaultTextOption())
        cursor = self.textCursor()
        cursor.select(cursor.SelectionType.Document)
        cursor.mergeBlockFormat(block_fmt)

        # Apply to future blocks
        self.document().setDefaultTextOption(self.document().defaultTextOption())

    def show_context_menu(self, pos):
        menu = self.createStandardContextMenu()
        menu.addSeparator()

        toggle_action = QAction("Toggle Checklist Mode", self)
        toggle_action.setCheckable(True)
        toggle_action.setChecked(self.checklist_mode)
        toggle_action.triggered.connect(self.toggle_checklist_mode)
        menu.addAction(toggle_action)

        menu.exec(self.mapToGlobal(pos))

    def toggle_checklist_mode(self):
        self.checklist_mode = not self.checklist_mode
        if self.checklist_mode:
            self.convert_to_checklist()
        else:
            self.remove_checklist()

    def convert_to_checklist(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        doc = self.document()
        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            text = block.text()
            if not text.startswith("☐ ") and not text.startswith("☑ "):
                cursor.setPosition(block.position())
                cursor.insertText("☐ ")

        cursor.endEditBlock()

    def remove_checklist(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()

        doc = self.document()
        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            text = block.text()
            if text.startswith("☐ ") or text.startswith("☑ "):
                cursor.setPosition(block.position())
                cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 2)
                cursor.removeSelectedText()

                # Reset formatting
                cursor.select(cursor.SelectionType.BlockUnderCursor)
                fmt = cursor.charFormat()
                fmt.setForeground(QColor(Styles.TEXT_COLOR))
                fmt.setFontStrikeOut(False)
                cursor.setCharFormat(fmt)

        cursor.endEditBlock()

    def keyPressEvent(self, event):
        if self.checklist_mode and event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            cursor.insertText("\n☐ ")
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if self.checklist_mode and event.button() == Qt.MouseButton.LeftButton:
            cursor = self.cursorForPosition(event.pos())
            block = cursor.block()
            text = block.text()

            # Check if click is near the start of the block (where checkbox is)
            # This is a rough approximation. A better way is to check the cursor position relative to block start.
            block_pos = cursor.positionInBlock()

            if block_pos <= 2:  # Clicked on the checkbox characters
                if text.startswith("☐ "):
                    self.toggle_checkbox(block, True)
                    return
                elif text.startswith("☑ "):
                    self.toggle_checkbox(block, False)
                    return

        super().mousePressEvent(event)

    def toggle_checkbox(self, block, checked):
        cursor = self.textCursor()
        cursor.setPosition(block.position())
        cursor.movePosition(cursor.MoveOperation.Right, cursor.MoveMode.KeepAnchor, 2)

        cursor.beginEditBlock()
        cursor.insertText("☑ " if checked else "☐ ")

        # Apply styling to the rest of the line
        cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
        fmt = cursor.charFormat()
        if checked:
            fmt.setForeground(QColor("#888888"))
            fmt.setFontStrikeOut(True)
        else:
            fmt.setForeground(QColor(Styles.TEXT_COLOR))
            fmt.setFontStrikeOut(False)
        cursor.setCharFormat(fmt)

        cursor.endEditBlock()


class NoteWindow(QMainWindow):
    note_changed = pyqtSignal(dict)
    spawn_requested = pyqtSignal(int, int)  # x, y
    delete_requested = pyqtSignal(str)  # note_id
    closed = pyqtSignal(str)  # note_id

    def __init__(self, note_data):
        super().__init__()
        self.note_data = note_data
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.color_key = note_data.get("color", "yellow").upper()
        self.setup_ui()
        self.load_data()

        # Auto-save timer
        self.save_timer = QTimer()
        self.save_timer.setInterval(2000)  # 2 seconds debounce
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_note)

        self.content.textChanged.connect(self.on_text_changed)

        # Restore position after window is shown (fixes WM centering issues)
        # Increased delay and using windowHandle for Wayland support
        QTimer.singleShot(100, self.restore_position)

        # Keyboard Shortcuts
        self.new_note_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.new_note_shortcut.activated.connect(self.spawn_new_note)

    def restore_position(self):
        x = self.note_data.get("x", 100)
        y = self.note_data.get("y", 100)
        self.move(x, y)

        # Try setting position directly on window handle (for Wayland)
        if self.windowHandle():
            self.windowHandle().setPosition(x, y)

    def setup_ui(self):
        # Main Container
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title Bar
        self.title_bar = TitleBar(self, self.color_key)
        layout.addWidget(self.title_bar)

        # Content
        self.content = NoteContent()
        layout.addWidget(self.content)

        # Resize Grip (Bottom Right)
        grip_layout = QHBoxLayout()
        grip_layout.setContentsMargins(0, 0, 0, 0)
        grip_layout.addStretch()
        self.size_grip = QSizeGrip(self.central_widget)
        self.size_grip.setFixedSize(15, 15)
        grip_layout.addWidget(self.size_grip)
        layout.addLayout(grip_layout)

        self.apply_styles()

    def apply_styles(self):
        bg_color = getattr(Styles, f"{self.color_key}_BG", Styles.YELLOW_BG)
        header_color = getattr(Styles, f"{self.color_key}_HEADER", Styles.YELLOW_HEADER)

        # Get system font and increase size
        font = QApplication.font()
        font_family = font.family()
        font_size = f"{font.pointSize() + 2}pt"

        self.central_widget.setStyleSheet(Styles.NOTE_WINDOW.format(bg_color=bg_color))
        self.title_bar.setStyleSheet(Styles.TITLE_BAR.format(header_color=header_color))
        self.content.setStyleSheet(Styles.CONTENT_AREA.format(
            text_color=Styles.TEXT_COLOR,
            font_family=font_family,
            font_weight="bold",
            font_size=font_size
        ) + Styles.SCROLLBAR)

    def load_data(self):
        self.content.setPlainText(self.note_data.get("content", ""))
        self.content.checklist_mode = self.note_data.get("checklist_mode", False)

        # If in checklist mode, ensure content is formatted correctly
        if self.content.checklist_mode:
            self.content.convert_to_checklist()
            self.restore_checklist_styles()

        self.setGeometry(
            self.note_data.get("x", 100),
            self.note_data.get("y", 100),
            self.note_data.get("width", 300),
            self.note_data.get("height", 300)
        )

    def restore_checklist_styles(self):
        # Iterate blocks and apply style if checked
        doc = self.content.document()
        cursor = self.content.textCursor()

        for i in range(doc.blockCount()):
            block = doc.findBlockByNumber(i)
            text = block.text()
            if text.startswith("☑ "):
                cursor.setPosition(block.position())
                cursor.movePosition(cursor.MoveOperation.EndOfBlock, cursor.MoveMode.KeepAnchor)
                fmt = cursor.charFormat()
                fmt.setForeground(QColor("#888888"))
                fmt.setFontStrikeOut(True)
                cursor.setCharFormat(fmt)

    def on_text_changed(self):
        self.save_timer.start()

    def save_note(self):
        self.note_data["content"] = self.content.toPlainText()
        self.note_data["checklist_mode"] = self.content.checklist_mode
        self.note_data["x"] = self.pos().x()
        self.note_data["y"] = self.pos().y()
        self.note_data["width"] = self.width()
        self.note_data["height"] = self.height()
        self.note_changed.emit(self.note_data)

    def moveEvent(self, event):
        self.save_timer.start()
        super().moveEvent(event)

    def resizeEvent(self, event):
        self.save_timer.start()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.save_note()
        self.closed.emit(self.note_data["id"])
        super().closeEvent(event)

    def spawn_new_note(self):
        self.spawn_requested.emit(self.x() + 20, self.y() + 20)

    def change_color(self, color_name):
        self.color_key = color_name.upper()
        self.note_data["color"] = color_name.lower()
        self.apply_styles()
        self.save_note()

    def delete_note(self):
        self.delete_requested.emit(self.note_data["id"])
        self.close()
