import sys
sys.path.append("../")
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import Token, Login_details
from utils import password_verify
from oauth2 import create_acces_token
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post('/login',response_model=Token)
def login(user_credentials: Login_details, db: Session = Depends(get_db)):
    print(user_credentials.username)
    user = db.query(models.Users).filter(
        models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not password_verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = create_acces_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
