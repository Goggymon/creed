from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QScrollArea,
    QPushButton,
    QTextEdit,
    QLineEdit,
)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPainter, QBrush, QPen, QTextCursor
from worker import ChatWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(1100, 720)
        self.setMinimumSize(900, 600)

        self._old_pos = None

        self.init_ui()

    def init_ui(self):
        self.central = QWidget()
        self.central.setObjectName("central_widget")

        layout = QVBoxLayout(self.central)
        layout.setContentsMargins(10, 10, 10, 10)

        # Top Bar
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(50)
        top_layout = QHBoxLayout(self.top_bar)
        top_layout.setContentsMargins(10, 0, 10, 0)

        self.title = QLabel("CREED")
        self.version = QLabel("v0.4.0")
        self.close_btn = QPushButton("✕")
        self.min_btn = QPushButton("─")

        self.close_btn.clicked.connect(self.close)
        self.min_btn.clicked.connect(self.showMinimized)

        top_layout.addWidget(self.title)
        top_layout.addStretch()
        top_layout.addWidget(self.version)
        top_layout.addWidget(self.min_btn)
        top_layout.addWidget(self.close_btn)

        layout.addWidget(self.top_bar)
        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setObjectName("chat_area")

        layout.addWidget(self.chat_area)

        # Bottom Input Bar
        bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(bottom_bar)
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message...")

        self.send_btn = QPushButton("▶")
        self.stop_btn = QPushButton("⏹")
        self.voice_btn = QPushButton("🔊")

        bottom_layout.addWidget(self.input_field)
        bottom_layout.addWidget(self.voice_btn)
        bottom_layout.addWidget(self.stop_btn)
        bottom_layout.addWidget(self.send_btn)

        layout.addWidget(bottom_bar)

        # Placeholder content
        content = QLabel("Chat Interface Coming Next...")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)

        self.setCentralWidget(self.central)

        self.apply_styles()
        self.send_btn.clicked.connect(self.handle_send)
        self.input_field.returnPressed.connect(self.handle_send)
        self.send_btn.setObjectName("send_button")

    def apply_styles(self):
        self.setStyleSheet(
            """
        QWidget#central_widget {
            background-color: #0f1117;
            border-radius: 16px;
        }
        QLabel {
            color: #e6e6e6;
            font-size: 14px;
        }
        QPushButton {
            background: transparent;
            color: #e6e6e6;
            border: none;
            font-size: 14px;
        }
        QPushButton:hover {
            color: #00c8ff;
        }
        QTextEdit#chat_area {
            background-color: #151821;
            border-radius: 12px;
            padding: 12px;
            font-size: 14px;
        }

        QLineEdit {
            background-color: #151821;
            border-radius: 10px;
            padding: 8px;
            color: #e6e6e6;
            border: 1px solid #22262f;
        }

        QLineEdit:focus {
            border: 1px solid #00c8ff;
        }

        QPushButton {
        background-color: #00c8ff;
            color:black;
            font-weight: bold;
            border-radius: 8px;
            padding: 6px 12px;
        }

        QPushButton:hover {
            background-color: #00a8d8;
        }
    
        """
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._old_pos:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._old_pos = None

    def handle_send(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.chat_area.append(f"<b>You:</b> {text}")
        self.input_field.clear()

        self.chat_area.append("<b>CREED:</b> ")
        self.worker = ChatWorker(text)

        self.worker.new_token.connect(self.append_token)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def append_token(self, token):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(token)
        self.chat_area.setTextCursor(cursor)
        self.chat_area.ensureCursorVisible()

    def on_finished(self):
        self.chat_area.append("\n")

    def on_error(self, error):
        self.chat_area.append(f"\nError: {error}")
