
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
import pytest
from app.database import Base
from fastapi.testclient import TestClient
from app.oauth2 import create_token
from app import models

SQLALCHEMY_DB_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_tests'

engine = create_engine(SQLALCHEMY_DB_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)




@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)



@pytest.fixture
def test_user(client):
    user_data = {
        'email': 'momos@gmail.com',
        'password': '123456'
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {
        'email': 'momoss@gmail.com',
        'password': '123456'
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    token = create_token(data= {"user_id" :test_user['id']})
    return token


@pytest.fixture()
def authorized_client(token,client,session):
    client.headers ={
        **client.headers,
        'Authorization' : f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user,test_user2,session):
    posts_data = [
        {"title" : "1st post","content" : "1st post", "user_id" :test_user['id']},
        {"title" : "2st post","content" : "2st post", "user_id" :test_user['id']},
        {"title" : "3st post","content" : "3st post", "user_id" :test_user['id']},
        {"title" : "4st post","content" : "4st post", "user_id" :test_user2['id']},
    ]
    def create_user_model(post):
       return  models.Post(**post)

    posts_map = map(create_user_model, posts_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
