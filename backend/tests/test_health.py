def test_health_root_and_api(client):
    assert client.get("/health").get_json()["status"] == "ok"
    payload = client.get("/api/v1/health").get_json()
    assert payload["service"] == "python-ai-assistant"
