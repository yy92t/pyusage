import pytest

@pytest.fixture
def sample_fixture():
    return "sample data" 

def pytest_configure():
    pytest.sample_data = "sample data"