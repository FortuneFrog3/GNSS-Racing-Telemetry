from src.state import SessionInfo

# Shows that state.py is storing values correctly when new session is made
def test_session_creation():
    session = SessionInfo(
        role = "Driver",
        driver_name = "Bob",
        vehicle_name = "Miata",
        track_name = "Daytona",
        session_number = "1",
        date_time = "2026-03-08",
        tire_compound = "Soft",
        weather = "Sunny",
        notes = "Test..."
    )

    assert session.role == "Driver"
    assert session.driver_name == "Bob"
    assert session.vehicle_name == "Miata"
    assert session.track_name == "Daytona"
    assert session.session_number == "1"
    assert session.date_time == "2026-03-08"
    assert session.tire_compound == "Soft"
    assert session.weather == "Sunny"
    assert session.notes == "Test..."

# Shows that session gives a safe empty string if data isnt provided
def test_default_values():
    session = SessionInfo()

    assert session.role == ""
    assert session.driver_name == ""
    assert session.vehicle_name == ""
    assert session.track_name == ""
    assert session.session_number == ""
    assert session.date_time == ""
    assert session.tire_compound == ""
    assert session.weather == ""
    assert session.notes == ""


# Shows that data fields can be updated during runtime
def test_session_update():
    session = SessionInfo()

    session.driver_name = "Bob"
    session.notes = "Updated notes..."

    assert session.driver_name == "Bob"
    assert session.notes == "Updated notes..."