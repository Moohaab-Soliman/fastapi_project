import jwt
from datetime import datetime, timedelta

from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, Depends,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import  settings

from . import  schemas,database,models
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token (token : str, credentials_exception : HTTPException) :
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')
        if id is None:
            raise credentials_exception
        toked_data = schemas.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception


    return  toked_data



def get_current_user(token : str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    verify_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == verify_token.id).first()
    return user

