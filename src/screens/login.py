import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame

from ..widgets import BgWidget

class LoginScreen(QWidget):
    def __init__(self, go_next):
        super().__init__()
        self.go_next = go_next

        base_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(base_dir)
        img_path = os.path.join(root_dir, "loginwallpaper", "wallpaper.jpg")

        bg = BgWidget(img_path, overlay_alpha=0.45)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(bg)

        layout = QVBoxLayout(bg)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(12)

        title = QLabel("ChronoBox")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 60px; font-weight: 700; color: white; background: transparent;")

        subtitle = QLabel("Choose role to continue")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255,255,255,0.7); background: transparent;")

        driver_btn = QPushButton("Driver Login")
        team_btn = QPushButton("Team Login")
        driver_btn.clicked.connect(lambda: self.go_next("driver"))
        team_btn.clicked.connect(lambda: self.go_next("team"))

        driver_btn.setMinimumHeight(48)
        team_btn.setMinimumHeight(48)
        driver_btn.setMaximumWidth(420)
        team_btn.setMaximumWidth(420)

        form = QFrame()
        form.setObjectName("Panel")
        form.setMaximumWidth(700)

        f = QVBoxLayout(form)
        f.setContentsMargins(24, 24, 24, 24)
        f.setSpacing(12)
        f.addWidget(driver_btn)
        f.setSpacing(20)
        f.addWidget(team_btn)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addWidget(form)