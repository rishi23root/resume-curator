import pytest
from flaskApi import app
from flask.testing import FlaskClient

@pytest.fixture
def client() -> FlaskClient: # type: ignore
    with app.test_client() as client:
        yield client # type: ignore
