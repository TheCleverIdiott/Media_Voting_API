from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.orm import Session
import models
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION = settings.access_token_expire_minutes

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHIM)
    return encoded_jwt

def verify_acces_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHIM)
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)   
    except JWTError:
        raise credentials_exception    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={'WWW-Authenticate':'Bearer'})
    token = verify_acces_token(token,credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
