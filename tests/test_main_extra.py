from tests.conftest import client


def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200


def test_docs():

    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi():

    response = client.get("/openapi.json")

    assert response.status_code == 200