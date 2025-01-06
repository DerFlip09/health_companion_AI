import dotenv
import models 
from fastapi import Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine

# get the database URL from '.env' file
DATABASE_URL = dotenv.get_key(".env", "DATABASE_URL")

# create a database engine
engine = create_engine(DATABASE_URL)

# initialize the database
SQLModel.metadata.create_all(bind=engine)

# function to get a session from the engine
def get_session():
    with Session(bind=engine) as session:
        yield session
 
# dependency for database session and to use in the API endpoints
db_depend = Annotated[Session, Depends(get_session)]

