import pytest


@pytest.fixture
def get_text():
    def _get_text(response):
        return response.data.decode("utf-8")

    return _get_text
