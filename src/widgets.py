from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from PySide6.QtGui import QPainter, QPixmap

class BgWidget(QWidget):
    def __init__(self, image_path: str, overlay_alpha: float = 0.45):
        super().__init__()
        self._pix = QPixmap(image_path)
        self._alpha = overlay_alpha

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._pix.isNull():
            painter.fillRect(self.rect(), Qt.black)
            return

        scaled = self._pix.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        painter.drawPixmap(x, y, scaled)

        painter.setOpacity(self._alpha)
        painter.fillRect(self.rect(), Qt.black)
        painter.setOpacity(1.0)

def card(title: str, big: bool = False) -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.StyledPanel)

    # DO NOT override label alignment/colors globall please 
    f.setStyleSheet("""
        QFrame { background: white; border: 1px solid #ddd; border-radius: 12px; }
        QLabel { font-size: 14px; color: #111; }
    """)

    lay = QVBoxLayout(f)
    lay.setContentsMargins(14, 14, 14, 14)
    lay.setSpacing(6)

    # Title
    t = QLabel(title)
    t.setObjectName("title")          
    t.setAlignment(Qt.AlignCenter)   
    lay.addWidget(t)

    # Value
    v = QLabel("—")
    v.setObjectName("value")
    v.setAlignment(Qt.AlignCenter)
    lay.addStretch(1)
    lay.addWidget(v)

    # Size styling 
    if big:
        v.setStyleSheet("font-size: 28px; font-weight: 900;")
    else:
        v.setStyleSheet("font-size: 18px; font-weight: 700;")

    return f