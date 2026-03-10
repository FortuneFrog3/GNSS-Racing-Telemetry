from dataclasses import dataclass

@dataclass
class SessionInfo:
    role: str = ""
    driver_name: str = ""
    vehicle_name: str = ""
    track_name: str = ""
    session_number: str = ""
    date_time: str = ""

    tire_compound: str = ""
    weather: str = ""
    notes: str = ""