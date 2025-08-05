def test_home_route():
    from app import app
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
