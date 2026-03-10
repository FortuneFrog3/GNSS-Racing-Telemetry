import time
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import Qt, QTimer
from datetime import datetime

from ..widgets import card
from ..gnss.reader import GNSSReader


class RaceScreen(QWidget):
    def __init__(self, logout):
        super().__init__()
        self.setObjectName("AppPage")
        self.logout = logout

        root = QVBoxLayout(self)
        root.setSpacing(10)

        top = QFrame()
        top.setObjectName("Panel")
        top_lay = QHBoxLayout(top)
        top_lay.setContentsMargins(14, 10, 14, 10)
        top_lay.setSpacing(28)

        self.track_lbl = QLabel("Track: —")
        self.driver_lbl = QLabel("Driver: —")
        self.vehicle_lbl = QLabel("Vehicle: —")
        self.time_lbl = QLabel("Date/Time: —")
        self.sess_lbl = QLabel("Session: —")

        for lbl in (
            self.track_lbl,
            self.driver_lbl,
            self.vehicle_lbl,
            self.time_lbl,
            self.sess_lbl,
        ):
            lbl.setObjectName("HeaderField")

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._tick_time)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)

        top_lay.addWidget(self.track_lbl, 1)
        top_lay.addWidget(self.driver_lbl, 1)
        top_lay.addWidget(self.vehicle_lbl, 1)
        top_lay.addWidget(self.time_lbl, 1)
        top_lay.addWidget(self.sess_lbl, 1)
        top_lay.addWidget(logout_btn, 1)

        content = QHBoxLayout()
        content.setSpacing(10)

        map_box = QFrame()
        map_box.setObjectName("Panel")
        map_box.setMinimumWidth(280)
        map_lay = QVBoxLayout(map_box)
        map_lay.setContentsMargins(12, 12, 12, 12)

        map_title = QLabel("Live GNSS Track View")
        map_title.setObjectName("SectionTitle")

        self.plot = pg.PlotWidget()
        self.plot.setBackground("w")
        self.plot.showGrid(x=True, y=True)
        self.plot.setLabel("left", "Y (m)")
        self.plot.setLabel("bottom", "X (m)")
        self.plot.setMinimumHeight(260)
        self.plot.setAspectLocked(True)

        self.track_curve = self.plot.plot([], [], pen=pg.mkPen("b", width=2))
        self.current_dot = pg.ScatterPlotItem(size=10, brush=pg.mkBrush("r"))
        self.plot.addItem(self.current_dot)

        map_lay.addWidget(map_title)
        map_lay.addWidget(self.plot)

        right = QFrame()
        right.setObjectName("TelemetryPanel")
        grid = QGridLayout(right)
        grid.setSpacing(10)

        self.lap_time = card("Lap Time", big=True)
        self.best_lap = card("Best Lap Time")
        self.delta_lap = card("Δ Last Lap (+ / -)")
        self.sector = card("Sector # + Sector Time")
        self.delta_sector = card("Δ Last Sector (+ / -)")
        self.projected = card("Projected Fastest Lap")

        self.lap_time_value = self.lap_time.findChild(QLabel, "value")
        self.lap_time_value.setObjectName("LapTimeValue")
        self.lap_time_value.setAlignment(Qt.AlignCenter)

        # Lap timer state
        self._lap_start = None
        self._lap_elapsed_before = 0.0
        self._set_lap_elapsed(0.0)

        self.session_time = card("Total Session Time:")
        title_lbl = self.session_time.findChild(QLabel, "title")
        if title_lbl is None:
            labels = self.session_time.findChildren(QLabel)
            title_lbl = next((l for l in labels if l.objectName() != "value"), None)

        if title_lbl:
            title_lbl.setText("Total Session Time:")
            title_lbl.setObjectName("SessionTimeTitle")
            title_lbl.setAlignment(Qt.AlignCenter)

        self.session_time_value = self.session_time.findChild(QLabel, "value")
        self.session_time_value.setObjectName("SessionTimeValue")
        self.session_time_value.setAlignment(Qt.AlignCenter)

        self.start_stop = QPushButton("Start Session")
        self.start_stop.clicked.connect(self.toggle_session)
        self.start_stop.setMinimumHeight(48)
        self.start_stop.setObjectName("StartSessionButton")

        self._session_ui_timer = QTimer(self)
        self._session_ui_timer.setInterval(100)
        self._session_ui_timer.timeout.connect(self._tick_session_elapsed)

        self._session_start = None
        self._elapsed_before = 0.0
        self._set_session_elapsed(0.0)

        grid.addWidget(self.lap_time, 0, 0, 1, 2)
        grid.addWidget(self.delta_lap, 1, 0)
        grid.addWidget(self.best_lap, 1, 1)
        grid.addWidget(self.sector, 2, 0)
        grid.addWidget(self.delta_sector, 2, 1)
        grid.addWidget(self.projected, 3, 0)
        grid.addWidget(self.session_time, 3, 1)
        grid.addWidget(self.start_stop, 4, 0, 1, 2)

        content.addWidget(map_box, 1)
        content.addWidget(right, 2)

        bottom = QFrame()
        b_lay = QHBoxLayout(bottom)
        b_lay.setContentsMargins(14, 10, 14, 10)

        self.session_status = QLabel("Status: Idle")

        b_lay.addStretch(1)
        b_lay.addWidget(self.session_status)

        root.addWidget(top)
        root.addLayout(content)
        root.addWidget(bottom)

        self._running = False
        self._session_number = 1

        # GNSS / plot state
        self._gnss = GNSSReader()
        self._track_x = []
        self._track_y = []
        self._plot_initialized = False

        self._gps_timer = QTimer(self)
        self._gps_timer.setInterval(100)  # 10 Hz
        self._gps_timer.timeout.connect(self._poll_gps)

        connected = self._gnss.connect()
        if connected:
            self.session_status.setText("Status: GNSS connected")
        else:
            self.session_status.setText("Status: GNSS not detected (simulation mode)")

        self._gps_timer.start()

    def set_header(self, track: str, driver: str, vehicle: str, session: str, dt: str):
        self.track_lbl.setText(f"Track: {track}")
        self.driver_lbl.setText(f"Driver: {driver}")
        self.vehicle_lbl.setText(f"Vehicle: {vehicle}")
        self._session_number = int(session)
        self.sess_lbl.setText(f"Session: {self._session_number}")
        self.time_lbl.setText(f"Date/Time: {dt}")

    def toggle_session(self):
        self._running = not self._running

        if self._running:
            self.start_stop.setText("Stop Session")
            self.session_status.setText("Status: Recording")

            # Reset track for new session
            self._track_x = []
            self._track_y = []
            self.track_curve.setData([], [])
            self.current_dot.setData([], [])
            self._gnss.reset_reference()

            # Reset plot initialization so range can be set again if needed
            self._plot_initialized = False

            # Start elapsed timing
            self._session_start = time.perf_counter()
            self._session_ui_timer.start()

            self._lap_start = time.perf_counter()
            self._lap_elapsed_before = 0.0
            self._set_lap_elapsed(0.0)

            self._timer.start()

        else:
            self.start_stop.setText("Start Session")
            self.session_status.setText("Status: Idle")

            # Stop timers
            self._session_ui_timer.stop()
            self._timer.stop()

            # Increment session number
            self._session_number += 1
            self.sess_lbl.setText(f"Session: {self._session_number}")

            # Reset session timer
            self._session_start = None
            self._elapsed_before = 0.0
            self._set_session_elapsed(0.0)

            # Reset lap timer
            self._lap_start = None
            self._lap_elapsed_before = 0.0
            self._set_lap_elapsed(0.0)

    def _tick_time(self):
        now = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        self.time_lbl.setText(f"Date/Time: {now}")

    def _set_session_elapsed(self, seconds: float):
        if seconds < 0:
            seconds = 0.0
        total_tenths = int(seconds * 10)
        mm = (total_tenths // 10) // 60
        ss = (total_tenths // 10) % 60
        t = total_tenths % 10
        text = f"{mm:02d}  :  {ss:02d}  .  {t}"
        self.session_time_value.setText(text)

    def _set_lap_elapsed(self, seconds: float):
        if seconds < 0:
            seconds = 0.0
        total_tenths = int(seconds * 10)
        mm = (total_tenths // 10) // 60
        ss = (total_tenths // 10) % 60
        t = total_tenths % 10
        text = f"{mm:02d}  :  {ss:02d}  .  {t}"
        self.lap_time_value.setText(text)

    def reset_lap_timer(self):
        self._lap_elapsed_before = 0.0
        self._lap_start = time.perf_counter() if self._running else None
        self._set_lap_elapsed(0.0)

    def _tick_session_elapsed(self):
        now = time.perf_counter()

        # Total session time
        if self._session_start is not None:
            elapsed = self._elapsed_before + (now - self._session_start)
            self._set_session_elapsed(elapsed)

        # Current lap time
        if self._lap_start is not None:
            lap_elapsed = self._lap_elapsed_before + (now - self._lap_start)
            self._set_lap_elapsed(lap_elapsed)

    def _poll_gps(self):
        point = self._gnss.read_point()
        if point is None:
            return

        x, y = point

        # Set an initial visible range the first time points appear
        if not self._plot_initialized:
            self.plot.setXRange(-25, 25)
            self.plot.setYRange(-25, 25)
            self._plot_initialized = True

        self._track_x.append(x)
        self._track_y.append(y)

        self.track_curve.setData(self._track_x, self._track_y)
        self.current_dot.setData([x], [y])