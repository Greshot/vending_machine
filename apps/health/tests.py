def test_health_check_ok(client):
    response = client.get("/healthcheck/")
    assert response.status_code == 200
    assert response.content == b"OK"
