import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from .state import SessionInfo
from .screens.login import LoginScreen
from .screens.info import InfoScreen
from .screens.race import RaceScreen
from .screens.review import ReviewScreen
from .screens.team import TeamScreen

APP_STYLESHEET = """
    /* Background color for all pages */
    QWidget#AppPage {
        background-color: #171b24;
    }

    /* Center all telemetry labels */
    QFrame#TelemetryPanel QLabel {
        qproperty-alignment: AlignCenter;
    }

    /* READY Racing Button */
   QPushButton#ReadyButton {
        background-color: #dc2626;
        border: 5px solid rgba(255,255,255,0.20);
        border-radius: 80px;   /* half of 160 */
        min-width: 160px;
        min-height: 160px;
        max-width: 160px;
        max-height: 160px;
        color: white;
        font-size: 22px;
        font-weight: 1000;
        letter-spacing: 2px;
    }

/* Start Session button */
QPushButton#StartSessionButton {
    background-color: #ffffff;
    color: #0b0f18;
    font-weight: 900;
    font-size: 16px;

    border-style: solid;
    border-width: 2px;
    border-top-color: #f7f7f7;  
    border-left-color: #f7f7f7;
    border-right-color: #111827; 
    border-bottom-color: #111827;

    border-radius: 10px;
    padding: 12px 14px;
}

QPushButton#StartSessionButton:hover {
    background-color: #f2f2f2;
}

QPushButton#StartSessionButton:pressed {
    background-color: #e9e9e9;

    /* invert bevel to feel "pressed in" */
    border-top-color: #111827;
    border-left-color: #111827;
    border-right-color: #f7f7f7;
    border-bottom-color: #f7f7f7;
}

    QPushButton#ReadyButton:hover { background-color: #ef4444; }
    QPushButton#ReadyButton:pressed { background-color: #991b1b;}
    
    QFrame#Panel {
    background-color: rgba(17, 24, 39, 0.72);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    }

    QLabel {
        color: rgba(255,255,255,0.90);
    }

    /* Top header fields (Track/Driver/Vehicle/Date/Session) */
    QLabel#HeaderField {
    color: rgba(255,255,255,0.92);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

    QPushButton {
        background-color: rgba(148, 163, 184, 0.22);
        border: 1px solid rgba(255,255,255,0.12);
        color: white;
        border-radius: 10px;
        padding: 10px 14px;
        font-weight: 700;
    }
    QPushButton:hover { background-color: rgba(148, 163, 184, 0.32); }
    QPushButton:pressed { background-color: rgba(148, 163, 184, 0.18); }

    QPushButton#SoftButton {
        background-color: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.16);
    }

    /* Top bar text */
    QLabel#TopBarLabel {
        font-weight: 700;
    }

    /* Section title */
    QLabel#SectionTitle {
        font-weight: 800;
        color: rgba(255,255,255,0.85);
    }

    /* Map placeholder */
    QLabel#MapArea {
        color: rgba(255,255,255,0.55);
        border: 1px dashed rgba(255,255,255,0.25);
        border-radius: 10px;
    }

    /* Subtle text */
    QLabel#SubtleText {
        color: rgba(255,255,255,0.65);
        font-weight: 600;
    }

    /* Session time title */
    QLabel#SessionTimeTitle {
        font-size: 14px;
        font-weight: 700;
        color: rgba(255,255,255,0.75);
        margin-bottom: 4px;
    }

    /* Large centered session time */
    QLabel#SessionTimeValue {
        font-size: 32px;
        font-weight: 900;
        color: #ffffff;
}

    """

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChronoBox - Dev Test")
        self.resize(1100, 650)

        self.state = SessionInfo()
        self.stack = QStackedWidget()
        self.stack.setObjectName("AppPage")
        self.setCentralWidget(self.stack)

        self.login = LoginScreen(go_next=self.on_login_success)
        self.info = InfoScreen(go_race=self.on_info_done, go_back=self.go_login)
        self.race = RaceScreen(logout=self.go_login)
        self.review = ReviewScreen(join_live=self.go_team_live, go_back=self.go_login)
        self.team = TeamScreen(go_back=self.go_login)

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.info)
        self.stack.addWidget(self.race)
        self.stack.addWidget(self.review)
        self.stack.addWidget(self.team)

        self.go_login()

    def go_login(self):
        self.stack.setCurrentWidget(self.login)

    def on_login_success(self, role: str):
        self.state.role = role
        if role == "driver":
            self.stack.setCurrentWidget(self.info)
        else:
            self.stack.setCurrentWidget(self.review)

    def go_team_live(self):
        self.team.set_waiting(True)
        self.stack.setCurrentWidget(self.team)

    def on_info_done(self, driver: str, track: str, vehicle: str, session: str):
        self.state.driver_name = driver
        self.state.track_name = track
        self.state.vehicle_name = vehicle
        self.state.session_number = session
        self.state.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.race.set_header(track, driver, vehicle, session, self.state.date_time)
        self.stack.setCurrentWidget(self.race)

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLESHEET)
    win = MainWindow()
    win.showFullScreen()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())

