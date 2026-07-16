def test_should_reject_request_without_credentials(client):
    response = client.get("/documents")

    assert response.status_code == 401


def test_should_reject_invalid_credentials(client):
    response = client.get(
        "/documents",
        auth=("admin", "senha_errada"),
    )

    assert response.status_code == 401


def test_should_accept_valid_credentials(
    client,
    authentication,
):
    response = client.get(
        "/documents",
        auth=authentication,
    )

    assert response.status_code == 200