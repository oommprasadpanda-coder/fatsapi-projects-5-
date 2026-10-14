from pydantic import BaseModel 
from typing import Literal

#find item in database 
# ItemStatus =Literal["lost" , "claimed" , "returned"]
ItemStatus = Literal["lost" , "claimed" , "returned"]

class LostItemCreate(BaseModel):
    name  : str 
    description : str 
    location : str 
    category : str 
    status : ItemStatus = "lost"


class LostItemResponse(LostItemCreate):
    id : int

    model_config = {"from_attributes" : True}

#lost items in database 
class ItemStatusUpdate(BaseModel):
    status : ItemStatus



class UserCreate(BaseModel):
    username : str 
    password : str

class UserLogin(BaseModel):
    username : str 
    password : str 

class UserResponse(BaseModel):
    id  : int 
    username : str

    model_config = {"from_attributes" : True}

    