from sqlalchemy import Column , Integer , String , Text
from database import Base 


class LostItem(Base):
    __tablename__ = "lost_items"

    id = Column(Integer , primary_key=True , index=True)
    name = Column(String(100) , nullable=False)
    description= Column(Text , nullable=False)
    location = Column(String(100) , nullable=False)
    category = Column(String(50) , nullable=False)

    status = Column(String , default="lost" , nullable=False)




class User(Base):
    __tablename__ ="Users"

    id = Column(Integer , primary_key=True , index=True)
    username=Column(String(50) , nullable=False , index=True , unique=True)
    password_hash = Column(String , nullable=False)



