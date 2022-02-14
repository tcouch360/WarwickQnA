import pytest
from app import app as application

@pytest.fixture()
def app_fixture():
    application.run(host='127.0.0.1', port=8080, debug=True)
    yield application

    # clean up / reset resources here


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()


@pytest.fixture()
def runner(app_fixture):
    return app_fixture.test_cli_runner()

def test_request_example(client):
    response = client.get("/index")
    assert b"<title>Welcome | Warwick Q&A</title>" in response.data