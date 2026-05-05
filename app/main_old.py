from typing import Optional

from fastapi import FastAPI, HTTPException, status, Response
from psycopg import Cursor
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time



app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published : bool = False
    rate :Optional[int] = None

while True :
    try:
        conn = psycopg.connect(dbname = 'fastapi', user = 'postgres', password = 'munnaa61', row_factory=dict_row)
        cursor:Cursor = conn.cursor()
        print('connected successfully')
        break
    except Exception as error:
        print("connecting to database failed")
        print("Error : ",error)
        time.sleep(2)
       


my_posts = [
    {"id" : 1 , "title" : "Post num 1", "content" :  "Welcome to my first post"},
    {"id" : 2 , "title" : "Post num 2", "content" :  "Welcome to my second post "}
]

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return  post
    return None

def find_post_index(id) -> int:
    for index, post in enumerate (my_posts):
        if post["id"] == id : 
            return index
    return 0
@app.get("/")
def  root():
    return {"message" : "Hello World!"}

@app.get('/posts')
def get_posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data" : posts}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[-1]
    return post

@app.get('/posts/{id}')
def get_post(id:int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id), ))
    post = cursor.fetchone()
    if not post :
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                          detail= f"post with id {id} was not found")

    return {"post detail":post}



@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post :Post):

   cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content, post.published))
   new_post = cursor.fetchone()
   conn.commit()
   return {"new Post": new_post}


# @app.delete('/posts/{id}',status_code=status.HTTP_410_GONE)
# def delete_post(id:int):
#     post = find_post(id)
#     if post:
#         my_posts.remove(post)
#         return {"msg" :f"post with id {id} deleted"}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post is not found")
#

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):

    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id), ))
    deleted_post = cursor.fetchone()

    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post is not found")
    else :
        return {"msg" :f"post with id {id} deleted"}


@app.put('/posts/{id}')
async def update_post(id:int, post : Post):
    cursor.execute("UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post is not found")
    else:
        return {"data" : updated_post}
 