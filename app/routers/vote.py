

from fastapi import HTTPException, status, APIRouter,Depends

from .. import schemas,oauth2, models
from ..database import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db : Session = Depends(get_db) , current_user : models.User = Depends(oauth2.get_current_user)):
    # check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {vote.post_id} does not exist")


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user with id : {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id , user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message" : "Successfully voted"}
    # dir == 0
        # not found vote -> raise exception
    else :
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message" : "Successfully devoted"}