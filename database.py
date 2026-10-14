from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker , declarative_base

DATABASE_URL = "postgresql+psycopg2://omm@localhost/findit_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
    
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



