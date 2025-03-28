import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Get my History" in response.data

def test_login_redirect(client):
    response = client.get('/login', follow_redirects=False)
    assert response.status_code == 302  # Redirect to Spotify auth

def test_history_without_token(client):
    response = client.get('/history', follow_redirects=False)
    assert response.status_code == 302
    assert response.location == '/login'