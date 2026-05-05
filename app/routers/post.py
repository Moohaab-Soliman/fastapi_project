from fastapi import Depends,status, HTTPException, APIRouter
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session
from app import schemas, models
from ..database import  get_db
from .. import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts( db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user), limit : int = 10, skip : int = 0,search : Optional[str]  = ""):
        # posts = (db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip)).all()

        result = db.query(models.Post, func.count(models.Post.id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Posts are not found")
        else:
            return result





@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id:int,db :Session = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    result = db.query(models.Post, func.count(models.Post.id).label("votes")).filter(models.Post.id == id).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    print(result)

    if result is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Posts with id {id} is not found")
    # if post.user_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform action")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db :Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)) :
    print(current_user)

    new_post = models.Post(user_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return  post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Authorized to perform action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return  post_query.first()

