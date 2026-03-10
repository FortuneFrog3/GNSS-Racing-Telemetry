from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel

class TeamScreen(QWidget):
    def __init__(self, go_back):
        super().__init__()
        self.setObjectName("AppPage")
        self.go_back = go_back

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        top = QHBoxLayout()
        back_btn = QPushButton("Back to Login")
        back_btn.clicked.connect(self.go_back)
        top.addWidget(back_btn)
        top.addStretch(1)
        root.addLayout(top)

        placeholder = QFrame()
        placeholder.setObjectName("Panel")
        ph = QVBoxLayout(placeholder)
        ph.setContentsMargins(18, 18, 18, 18)

        self.wait_overlay = QLabel("Waiting for driver to start session…")
        self.wait_overlay.setAlignment(Qt.AlignCenter)
        self.wait_overlay.setStyleSheet("""
            background-color: rgba(0,0,0,0.60);
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 16px;
            font-size: 26px;
            font-weight: 900;
            padding: 26px;
        """)
        root.addWidget(self.wait_overlay)

        self.set_waiting(True)

    def set_waiting(self, waiting: bool):
        self.wait_overlay.setVisible(waiting)