import pytest
from index import create_app, _db_connect

@pytest.fixture()
def app():
    """ @summary A testing initialisation function
        @return our_app - Returns the created app
    """
    our_app = create_app()
    return our_app

app_tester = app()

@app_tester.before_request
def startup():
    _db_connect()
