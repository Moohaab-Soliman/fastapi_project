import jwt
import pytest

from app import schemas

from app.config import settings



def test_create_user(client):
    res = client.post('/users/', json ={
        'email' : 'momos123@gmail.com',
        'password' : '123456'
    })
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'momos123@gmail.com'
    assert res.status_code == 201

def test_login(client, test_user):
    res = client.post('auth/login', data = {
        'username': test_user['email'],
        'password': test_user['password'],
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200
@pytest.mark.parametrize("email, password, status_code" , [
    ('momos@gmail.com', '123', 403),
    ('momoss@gmail.com', '123456', 403),
    ('momossss@gmail.com', '123', 403),
])
def test_incorrect_login(client,test_user, email,password,status_code):
    res = client.post('auth/login', data ={
        'username' : email,
        'password' : password
    })
    assert res.json().get('detail') == 'invalid credentials'
    assert res.status_code == status_code



