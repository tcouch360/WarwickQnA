import pytest
import pytest_flask_sqlalchemy
from app import app as application
from app import db
@pytest.fixture()
def app_fixture():
    application.run(host='127.0.0.1', port=8080, debug=True)

    yield application

@pytest.fixture(scope='session')
def _db():
    return db

@pytest.fixture()
def client(app_fixture):
    yield app_fixture.test_client()

@pytest.fixture()
def runner(app_fixture):
    yield app_fixture.test_cli_runner()

def test_request_example(_db,client):
    response = client.get("/index")
    assert b"<title>Welcome | Warwick Q&A</title>" in response.data

def test_logout_redirect(_db,client):
    response = client.get("/logout")
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == "/index"

