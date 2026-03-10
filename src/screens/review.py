from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel

class ReviewScreen(QWidget):
    def __init__(self, join_live, go_back):
        super().__init__()
        self.setObjectName("AppPage")
        self.join_live = join_live
        self.go_back = go_back

        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(12)

        top = QHBoxLayout()
        back_btn = QPushButton("Back to Login")
        back_btn.clicked.connect(self.go_back)
        top.addWidget(back_btn)
        top.addStretch(1)

        join_btn = QPushButton("Join Current Session")
        join_btn.clicked.connect(self.join_live)
        top.addWidget(join_btn)

        root.addLayout(top)

        panel = QFrame()
        panel.setObjectName("Panel")
        p = QVBoxLayout(panel)
        p.setContentsMargins(18, 18, 18, 18)
        p.addWidget(QLabel("(Review Past Sessions screen)"))

        root.addWidget(panel, 1)