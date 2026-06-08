import pytest

from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    def verify(post):
       return  schemas.PostOut(**post)

    posts_map = map(verify, res.json())

    posts_list = list(posts_map)
    assert posts_list[0].Post.id == test_posts[0].id
    assert res.status_code ==200


def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_existed(authorized_client,test_posts):
    res = authorized_client.get(f'/posts/8888')
    assert res.status_code == 404

def test_get_one_valid_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**res.json())
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published",[
     ("testpost 1", "testpost 1", True),
     ("testpost 2", "testpost 2", False),
     ("testpost 3", "testpost 3", True),
 ])
def test_create_post(authorized_client,test_user, test_posts,title,content,published):
    res = authorized_client.post('/posts/', json={'title' : title, 'content' : content, 'published' : published})
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']

def test_create_post_default_published_false(authorized_client, test_user):
    res = authorized_client.post('/posts/', json={'title' : 'title', 'content' : 'content'})
    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content'
    assert created_post.published == False
    assert created_post.user_id == test_user['id']

def test_unauthorized_user_create_post(client,test_posts):
    res =client.post('/posts/', json={'title': 'title', 'content': 'content'})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_success_delete_post(authorized_client,test_posts,test_user):
    res = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client,test_posts,test_user):
    res = authorized_client.delete(f'/posts/888')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts,test_user2):
    res = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts, test_user):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[0].id
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data["content"]

def test_update_other_user_post(authorized_client,test_posts,test_user):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user,test_posts):
    res = client.put(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client,test_posts,test_user):
    data = {
        "title" : "updated title",
        "content" : "updated content",
        "id" : test_posts[3].id
    }
    res = authorized_client.put(f'/posts/888',json=data)
    assert res.status_code == 404

