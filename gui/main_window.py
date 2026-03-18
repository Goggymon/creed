from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QLabel,
    QScrollArea,
)
from PySide6.QtCore import Qt
from worker import ChatWorker


class ChatBubble(QFrame):
    def __init__(self, text, is_user=False):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        self.label = QLabel(text)
        self.label.setWordWrap(True)

        bubble = QFrame()
        bubble_layout = QVBoxLayout(bubble)
        bubble_layout.addWidget(self.label)

        if is_user:
            bubble.setStyleSheet(
                """
                background:#00c8ff;
                color:black;
                border-radius:12px;
                padding:8px;
            """
            )
            layout.addStretch()
            layout.addWidget(bubble)
        else:
            bubble.setStyleSheet(
                """
                background:#2a2f3a;
                color:white;
                border-radius:12px;
                padding:8px;
            """
            )
            layout.addWidget(bubble)
            layout.addStretch()

        self.bubble = bubble

    def append_text(self, text):
        self.label.setText(self.label.text() + text)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(1200, 750)
        self.setMinimumSize(1000, 650)

        self._old_pos = None

        self.init_ui()
        self.apply_styles()
        self.set_status("Idle")

    # ----------------------------
    # UI BUILD
    # ----------------------------
    def init_ui(self):

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll = self.setObjectName("chat_area")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        # ----------------------------
        # Title Bar
        # ----------------------------
        self.title_bar = QFrame()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setObjectName("title_bar")

        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 0, 10, 0)

        self.title_label = QLabel("CREED")

        self.min_btn = QPushButton("—")
        self.max_btn = QPushButton("▢")
        self.close_btn = QPushButton("✕")

        for btn in [self.min_btn, self.max_btn, self.close_btn]:
            btn.setFixedSize(30, 24)

        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.min_btn)
        title_layout.addWidget(self.max_btn)
        title_layout.addWidget(self.close_btn)

        # ----------------------------
        # Central Widget
        # ----------------------------
        self.central = QWidget()
        self.central.setObjectName("central_widget")
        self.setCentralWidget(self.central)

        root_layout = QVBoxLayout(self.central)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(6)

        root_layout.addWidget(self.title_bar)

        main_layout = QHBoxLayout()
        root_layout.addLayout(main_layout)

        # ----------------------------
        # Sidebar
        # ----------------------------
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(80)
        self.sidebar.setObjectName("sidebar")

        # ----------------------------
        # Conversation Panel
        # ----------------------------
        self.conversation_panel = QFrame()
        self.conversation_panel.setObjectName("conversation_panel")

        conv_layout = QVBoxLayout(self.conversation_panel)
        conv_layout.setContentsMargins(15, 15, 15, 10)
        conv_layout.setSpacing(6)

        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setObjectName("chat_area")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(10)
        self.chat_layout.addStretch()

        self.chat_scroll.setWidget(self.chat_container)

        self.bottom_bar = QWidget()
        bottom_layout = QHBoxLayout(self.bottom_bar)
        bottom_layout.setContentsMargins(0, 8, 0, 0)
        bottom_layout.setSpacing(8)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Speak or type a command...")

        self.voice_btn = QPushButton("🎙")
        self.stop_btn = QPushButton("⏹")
        self.send_btn = QPushButton("▶")

        bottom_layout.addWidget(self.input_field)
        bottom_layout.addWidget(self.voice_btn)
        bottom_layout.addWidget(self.stop_btn)
        bottom_layout.addWidget(self.send_btn)

        conv_layout.addWidget(self.chat_scroll)
        conv_layout.addWidget(self.bottom_bar)

        # ----------------------------
        # Right Panel
        # ----------------------------
        self.right_panel = QFrame()
        self.right_panel.setFixedWidth(350)
        self.right_panel.setObjectName("right_panel")

        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.setSpacing(10)

        # ----------------------------
        # Systems Panel
        # ----------------------------
        self.systems_panel = QFrame()
        self.systems_panel.setObjectName("systems_panel")

        systems_layout = QVBoxLayout(self.systems_panel)
        systems_layout.setContentsMargins(15, 15, 15, 15)
        systems_layout.setSpacing(6)

        self.systems_label = QLabel("SYSTEM STATUS")

        status_row = QHBoxLayout()
        status_row.setSpacing(8)

        self.status_dot = QLabel()
        self.status_dot.setFixedSize(10, 10)

        self.system_state = QLabel("Idle")

        status_row.addWidget(self.status_dot)
        status_row.addWidget(self.system_state)
        status_row.addStretch()

        systems_layout.addWidget(self.systems_label)
        systems_layout.addLayout(status_row)
        systems_layout.addStretch()

        # ----------------------------
        # Memory Panel
        # ----------------------------
        self.memory_panel = QFrame()
        self.memory_panel.setObjectName("memory_panel")

        memory_layout = QVBoxLayout(self.memory_panel)
        memory_layout.setContentsMargins(15, 15, 15, 15)
        memory_layout.setSpacing(6)

        self.memory_label = QLabel("MEMORY")
        self.memory_content = QLabel("No persistent memory yet.")
        self.memory_content.setWordWrap(True)

        memory_layout.addWidget(self.memory_label)
        memory_layout.addWidget(self.memory_content)
        memory_layout.addStretch()

        right_layout.addWidget(self.systems_panel, 1)
        right_layout.addWidget(self.memory_panel, 2)

        # ----------------------------
        # Add Panels
        # ----------------------------
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.conversation_panel)
        main_layout.addWidget(self.right_panel)

        # ----------------------------
        # Signals
        # ----------------------------
        self.send_btn.clicked.connect(self.handle_send)
        self.input_field.returnPressed.connect(self.handle_send)
        self.stop_btn.clicked.connect(self.stop_generation)

        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)
        self.max_btn.clicked.connect(self.toggle_fullscreen)

        self.chat_scroll.setWidget(self.chat_container)

    # ----------------------------
    # Styling
    # ----------------------------
    def apply_styles(self):

        self.setStyleSheet(
            """
        QWidget#central_widget {
            background-color: #0f1117;
            border-radius: 18px;
        }

        QFrame#title_bar {
            background-color: #12151f;
            border-radius: 10px;
            border: 1px solid #242938;
        }

        QFrame#sidebar {
            background-color: #161a24;
            border-radius: 16px;
            border: 1px solid #242938;
        }

        QFrame#conversation_panel {
            background-color: #151821;
            border-radius: 16px;
            border: 1px solid #242938;
        }

        QFrame#systems_panel,
        QFrame#memory_panel {
            background-color: #1a1f29;
            border-radius: 16px;
            border: 1px solid #242938;
        }

        QTextEdit#chat_area {
            background-color: transparent;
            border: none;
            color: #e6e6e6;
            font-size: 14px;
        }

        QLineEdit {
            background-color: #1c212b;
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
            color: black;
            font-weight: bold;
            border-radius: 8px;
            padding: 6px 12px;
        }

        QPushButton:hover {
            background-color: #00a8d8;
        }

        QLabel {
            color: #d1d5db;
            font-size: 12px;
        }
        """
        )

    # ----------------------------
    # Window Drag
    # ----------------------------
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

    # ----------------------------
    # Chat Logic
    # ----------------------------
    def handle_send(self):

        text = self.input_field.text().strip()
        if not text:
            return

        # USER bubble
        user_bubble = ChatBubble(text, True)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, user_bubble)

        self.input_field.clear()

        # ✅ CREATE + STORE AI bubble
        self.current_ai_bubble = ChatBubble("", False)
        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1, self.current_ai_bubble
        )

        self.set_status("Processing")

        # START worker AFTER bubble exists
        self.worker = ChatWorker(text)
        self.worker.new_token.connect(self.append_token)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.error_signal.connect(self.on_error)

        self.worker.start()

    def stop_generation(self):
        if hasattr(self, "worker"):
            self.worker.stop()
            self.set_status("Stopped")

    def append_token(self, token):

        if not hasattr(self, "current_ai_bubble"):
            print("No bubble yet")
            return
        # force UI refresh
        self.current_ai_bubble.label.repaint()

        # auto scroll
        scrollbar = self.chat_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_finished(self):
        self.set_status("Idle")

    def on_error(self, error):

        error_bubble = ChatBubble(f"Error: {error}", False)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, error_bubble)

        self.set_status("Error")

    # ----------------------------
    # Status Indicator
    # ----------------------------
    def set_status(self, state):

        self.system_state.setText(state)

        color_map = {
            "Idle": "#555a66",
            "Listening": "#00c8ff",
            "Recording": "#ffb020",
            "Processing": "#3b82f6",
            "Speaking": "#22c55e",
            "Error": "#ef4444",
        }

        color = color_map.get(state, "#555a66")

        self.status_dot.setStyleSheet(
            f"""
            background-color: {color};
            border-radius: 5px;
        """
        )

    # ----------------------------
    # Fullscreen Toggle
    # ----------------------------
    def toggle_fullscreen(self):

        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
