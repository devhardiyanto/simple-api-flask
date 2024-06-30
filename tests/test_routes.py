# tests/test_routes.py

import pytest
from app import create_app, db
from app.models import Item

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_item(client):
    response = client.post('/items', json={'name': 'Test Item', 'description': 'Test Description'})
    assert response.status_code == 201
    assert 'Test Item' in str(response.data)

def test_get_items(client):
    client.post('/items', json={'name': 'Test Item', 'description': 'Test Description'})
    response = client.get('/items')
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_item(client):
    response_create = client.post('/items', json={'name': 'Test Item', 'description': 'Test Description'})
    item_id = response_create.json['item']['id']
    response_get = client.get(f'/items/{item_id}')
    assert response_get.status_code == 200
    assert response_get.json['name'] == 'Test Item'

def test_update_item(client):
    response_create = client.post('/items', json={'name': 'Test Item', 'description': 'Test Description'})
    item_id = response_create.json['item']['id']
    response_update = client.put(f'/items/{item_id}', json={'name': 'Updated Item', 'description': 'Updated Description'})
    assert response_update.status_code == 200
    assert response_update.json['item']['name'] == 'Updated Item'

def test_delete_item(client):
    response_create = client.post('/items', json={'name': 'Test Item', 'description': 'Test Description'})
    item_id = response_create.json['item']['id']
    response_delete = client.delete(f'/items/{item_id}')
    assert response_delete.status_code == 200
    response_get = client.get(f'/items/{item_id}')
    assert response_get.status_code == 404

if __name__ == '__main__':
    pytest.main()