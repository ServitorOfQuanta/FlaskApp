import pytest
from app import create_app
from models import db, Contact  # Import your app and models


# This will create a Flask test client with a test database for each test
@pytest.fixture
def client():
    app = create_app()
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",  # In-memory database for testing
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_create_contact(client):
    """Test creating a contact with valid data."""
    contact_data = {
        "name": "Some Person",
        "description": "A description.",
        "phoneNumber": "+123456789012",
    }

    response = client.post("/Contacts/api", json=contact_data)
    assert response.status_code == 201  # Expect a successful creation (201 Created)

    # Check that the contact is added to the database
    contact = Contact.query.first()
    assert contact.name == "Some Person"
    assert contact.phone_number == "+123456789012"


def test_invalid_phone_number(client):
    """Test phone number validation with an invalid phone number."""
    invalid_phone_number = "12345"  # Invalid phone number format

    # We simulate the phone number validation method here
    is_valid = Contact.validate_phone_number(invalid_phone_number)
    assert not is_valid


def test_valid_phone_number(client):
    """Test phone number validation with a valid phone number."""
    valid_phone_number = "+123456789012"  # Valid phone number format

    # We simulate the phone number validation method here
    is_valid = Contact.validate_phone_number(valid_phone_number)
    assert is_valid


def test_create_contact_invalid_phone_number(client):
    """Test creating a contact with an invalid phone number."""
    contact_data = {
        "name": "Some Person",
        "description": "A description.",
        "phone_number": "12345",  # Invalid phone number
    }

    response = client.post("/Contacts/api", json=contact_data)
    assert response.status_code == 400  # Expect a Bad Request (400) error

    data = response.get_json()
    assert "error" in data  # Expect an error message


def test_create_contact_missing_phone_number(client):
    """Test creating a contact with a missing phone number."""
    contact_data = {
        "name": "Some Person",
        "description": "A description.",
        "phone_number": "",  # Missing phone number
    }

    response = client.post("/Contacts/api", json=contact_data)
    assert response.status_code == 400  # Expect a Bad Request (400) error
    data = response.get_json()
    assert "error" in data  # Expect an error message
