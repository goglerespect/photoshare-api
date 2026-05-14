from tests.conftest import client


def test_root():

    response = client.get("/")

    assert response.status_code == 200


def test_healthcheck():

    response = client.get("/health")

    assert response.status_code in [200, 404]