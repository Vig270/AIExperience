import pytest
from secondpage import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_submit_issue(client):
    response = client.post('/submit_issue', data={'name': 'Test User', 'email': 'test@example.com', 'item': 'Test Item', 'issue': 'Test Issue'})
    assert response.status_code == 200
    assert b"Issue submitted successfully!" in response.data

def test_view_issues(client):
    response = client.get('/view_issues')
    assert response.status_code == 200
    assert b"No issues have been submitted yet." in response.data
