import sys
sys.path.append("../")
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models
from database import get_db
from schemas import Register,UserRegisterResponse
from utils import hash_password


router = APIRouter()


### Registering a user
@router.post('/register',status_code=status.HTTP_201_CREATED,response_model=UserRegisterResponse)
def create_user(payload:Register, db: Session = Depends(get_db)):
    
    
    #hashing the password
    hashed_password = hash_password(payload.password)
    payload.password = hashed_password
    registered_user = models.Users(**payload.dict())
    db.add(registered_user)
    db.commit()
    db.refresh(registered_user)

    return registered_user

### Get a single user
@router.get('/user/{id}',response_model=UserRegisterResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} does not exist")
    
    return user
