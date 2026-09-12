from sqlmodel import Session, create_engine, SQLModel
from dotenv import load_dotenv
from os import getenv
from typing import Annotated
from fastapi import Depends

load_dotenv()

__connection_string = getenv('DB_HOST')

if (not __connection_string):
    raise ValueError("A string de conexão com o banco de dados é nula.")
_engine = create_engine(__connection_string, pool_pre_ping=True)

def __db_connect():
    with Session(_engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(__db_connect)]