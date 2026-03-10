from backend.services import firebase_services as fbs
import backend.config as con
from unittest.mock import patch, MagicMock


@patch('backend.config.firebase_admin')
def test_firebase_initialize(mock_firebase_admin):
    """Test that Firebase initializes correctly"""
    mock_firebase_admin._apps = {}
    
    with patch.dict('os.environ', {
        'FIREBASE_CRED_PATH': 'credentials/serviceAccountKey.json',
        'FIREBASE_DB_URL': 'https://test.firebaseio.com'
    }):
        with patch('backend.config.credentials.Certificate'):
            try:
                con.initialize_firebase()
            except Exception as e:
                assert False, f"Firebase initialization failed: {e}"


@patch('backend.services.firebase_services.db')
def test_get_database_reference(mock_db):
    """Test that we can obtain a database reference"""
    mock_ref = MagicMock()
    mock_db.reference.return_value = mock_ref
    
    try:
        ref = fbs.get_ref()
        assert ref is not None
    except Exception as e:
        assert False, f"Failed to get database reference: {e}"


@patch('backend.services.firebase_services.db')
def test_firebase_write(mock_db):
    """Test writing data to Firebase"""
    mock_ref = MagicMock()
    mock_db.reference.return_value = mock_ref
    
    try:
        fbs.write_data("card11_test", {"status": "write_success"})
        mock_ref.set.assert_called_once_with({"status": "write_success"})
    except Exception as e:
        assert False, f"Firebase write failed: {e}"


@patch('backend.services.firebase_services.db')
def test_firebase_read(mock_db):
    """Test reading data from Firebase"""
    mock_ref = MagicMock()
    mock_db.reference.return_value = mock_ref
    mock_ref.get.return_value = {"status": "test_data"}
    
    try:
        data = fbs.read_data("card11_test")
        assert data is not None
        assert data == {"status": "test_data"}
    except Exception as e:
        assert False, f"Firebase read failed: {e}"