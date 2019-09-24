import pytest
from flask import url_for
from index import main


@pytest.fixture()
def test_app_main(client):
    """ @summary A testing function to test that the app is working
    """
    assert client.get(url_for('main')).status_code == 200