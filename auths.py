from jose import jwt
from datetime import timedelta , timezone , datetime
from fastapi import APIRouter , HTTPException , Depends 
from sqlalchemy.orm import Session
import models , schemas 
from pwdlib import PasswordHash
from database import get_db





router = APIRouter(prefix="/auth" , tags=["Authentication"])

password_hash = PasswordHash.recommended()





SECRET_KEY = "omprasadd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = 30



def create_token_access(username : str):

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)


    payload = {
        "sub" : username,
        "exp" : expire
    }

    return jwt.encode(payload , SECRET_KEY , algorithm=ALGORITHM )

@router.post("/register" , response_model=schemas.UserResponse  , status_code=201)
def register (user : schemas.UserCreate , db: Session =Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user :
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = models.User(
        username = user.username,
        password_hash = password_hash.hash(user.password)

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user : schemas.UserLogin, db : Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user is None :
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    if not password_hash.verify(user.password , existing_user.password_hash):

        raise HTTPException(
            status_code=401,
            detail="invalid username or password"
        )


    token = create_token_access(existing_user.username)

    return {
        "access_token" : token,
        "token_type" : "bearer"
    }




