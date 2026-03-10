from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QMessageBox, QComboBox
)

class InfoScreen(QWidget):
    def __init__(self, go_race, go_back):
        super().__init__()
        self.setObjectName("AppPage")
        self.go_race = go_race
        self.go_back = go_back

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 24, 30, 24)
        root.setSpacing(18)

        header = QLabel("Session Information")
        header.setStyleSheet("font-size: 35px; font-weight: 700;")
        header.setAlignment(Qt.AlignCenter)
        header_row = QHBoxLayout()
        header_row.addStretch()
        header_row.addWidget(header)
        header_row.addStretch()

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        back_btn.setObjectName("SoftButton")
        header_row.addWidget(back_btn)

        root.addLayout(header_row)

        # Top row
        top_grid = QGridLayout()
        top_grid.setHorizontalSpacing(40)
        top_grid.setVerticalSpacing(18)

        self.driver = self._box("Driver Name")
        self.vehicle = self._box("Vehicle")
        self.tire = self._dropdown_box("Tire Compound", ["Soft", "Medium", "Hard"])
        self.track = self._box("Track Name")

        top_grid.addLayout(self.driver["layout"], 0, 0)
        top_grid.addLayout(self.vehicle["layout"], 0, 1)
        top_grid.addLayout(self.tire["layout"],    0, 2)
        top_grid.addLayout(self.track["layout"],   0, 3)

        root.addLayout(top_grid)

        # Bottom row
        bottom_grid = QGridLayout()
        bottom_grid.setHorizontalSpacing(40)
        bottom_grid.setVerticalSpacing(18)

        self.weather = self._dropdown_box("Track Conditions", ["Dry", "Wet", "Mixed"])
        self.dt = self._box("Date/Time")
        self.notes = self._box("Additional Notes")
        
        # Date/Time
        self.dt["edit"].setText(datetime.now().strftime("%m/%d/%Y %I:%M %p"))
        self.dt["edit"].setReadOnly(True)

        bottom_grid.addLayout(self.weather["layout"], 0, 1)
        bottom_grid.addLayout(self.dt["layout"],      0, 2)
        bottom_grid.addLayout(self.notes["layout"],   0, 0)

        root.addLayout(bottom_grid)

        # READY button
        ready_row = QHBoxLayout()
        ready_row.addStretch(1)

        self.ready_btn = QPushButton("READY")
        self.ready_btn.setObjectName("ReadyButton")
        self.ready_btn.setMinimumSize(160, 160)
        self.ready_btn.setMaximumSize(160, 160)
        self.ready_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.ready_btn.clicked.connect(self.handle_continue)

        ready_row.addWidget(self.ready_btn, 0, Qt.AlignCenter)
        ready_row.addStretch(1)
        root.addLayout(ready_row)

    def _box(self, label_text: str):
        lay = QVBoxLayout()
        lay.setSpacing(8)

        # labels
        lbl = QLabel(label_text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: rgba(255,255,255,0.85);")

        edit = QLineEdit()
        edit.setPlaceholderText(label_text)
        edit.setMinimumWidth(260)
        edit.setMinimumHeight(56)
        edit.setAlignment(Qt.AlignCenter)
        edit.setObjectName("WireBox")

        lay.addWidget(lbl)
        lay.addWidget(edit)

        return {"layout": lay, "label": lbl, "edit": edit}
    
    def _dropdown_box(self, label_text: str, items: list[str]):
        lay = QVBoxLayout()
        lay.setSpacing(8)

        lbl = QLabel(label_text)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px; font-weight: 800; color: rgba(255,255,255,0.85);")

        combo = QComboBox()
        combo.addItems(items)
        combo.setMinimumWidth(260)
        combo.setMinimumHeight(56)
        combo.setObjectName("WireDropDown")
        combo.setEditable(False)

        lay.addWidget(lbl)
        lay.addWidget(combo)

        return {"layout": lay, "label": lbl, "combo": combo}

    def handle_continue(self):
        driver = self.driver["edit"].text().strip()
        track = self.track["edit"].text().strip()
        vehicle = self.vehicle["edit"].text().strip()
        session = "1"  # change later (we can add incrementing session numbers)

        if not driver or not track or not vehicle:
            QMessageBox.warning(self, "Missing Info", "Please fill out Driver Name, Track Name, and Vehicle.")
            return

        self.go_race(
            driver=driver,
            track=track,
            vehicle=vehicle,
            session=session
        )