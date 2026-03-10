import math
import serial
import pynmea2


class GNSSReader:
    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.ref_lat = None
        self.ref_lon = None
        self.sim_t = 0.0
        self.sim_mode = False

    def connect(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=0)
            self.sim_mode = False
            return True
        except Exception:
            self.serial_conn = None
            self.sim_mode = True
            return False

    def close(self):
        if self.serial_conn is not None:
            try:
                self.serial_conn.close()
            except Exception:
                pass
            self.serial_conn = None

    def reset_reference(self):
        self.ref_lat = None
        self.ref_lon = None
        self.sim_t = 0.0

    def latlon_to_xy(self, lat: float, lon: float):
        if self.ref_lat is None or self.ref_lon is None:
            self.ref_lat = lat
            self.ref_lon = lon

        R = 6371000.0  # Earth radius in meters

        lat0 = math.radians(self.ref_lat)
        lon0 = math.radians(self.ref_lon)
        lat1 = math.radians(lat)
        lon1 = math.radians(lon)

        x = (lon1 - lon0) * math.cos(lat0) * R
        y = (lat1 - lat0) * R

        return x, y

    def read_point(self):
        if self.sim_mode:
            self.sim_t += 0.08
            x = 18 * math.cos(self.sim_t)
            y = 18 * math.sin(self.sim_t)
            return x, y

        if self.serial_conn is None:
            return None

        try:
            while self.serial_conn.in_waiting:
                line = self.serial_conn.readline().decode("ascii", errors="ignore").strip()

                if not line:
                    continue

                if line.startswith("$GNRMC") or line.startswith("$GPRMC"):
                    msg = pynmea2.parse(line)

                    if msg.status != "A":
                        continue

                    lat = msg.latitude
                    lon = msg.longitude
                    return self.latlon_to_xy(lat, lon)

        except Exception:
            return None

        return None