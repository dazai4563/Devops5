from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

existing_users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    email = existing_users[0]['email']
    response = client.get("/api/v1/user", params={'email': email})
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == existing_users[0]['id']
    assert data['name'] == existing_users[0]['name']
    assert data['email'] == existing_users[0]['email']

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'Test User',
        'email': 'test_unique@example.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    user_id = response.json()
    assert isinstance(user_id, int)

    get_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert get_response.status_code == 200
    user_data = get_response.json()
    assert user_data['name'] == new_user['name']
    assert user_data['email'] == new_user['email']
    assert user_data['id'] == user_id

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую уже использует другой пользователь'''
    duplicate_user = {
        'name': 'Duplicate',
        'email': existing_users[0]['email']
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    temp_user = {
        'name': 'Temp User',
        'email': 'temp@example.com'
    }
    create_response = client.post("/api/v1/user", json=temp_user)
    assert create_response.status_code == 201
    temp_user_id = create_response.json()

    delete_response = client.delete("/api/v1/user", params={'email': temp_user['email']})
    assert delete_response.status_code == 204
    assert delete_response.text == ""

    get_response = client.get("/api/v1/user", params={'email': temp_user['email']})
    assert get_response.status_code == 404