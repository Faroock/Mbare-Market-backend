import os
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

from rimdev_lib.database import RIMDB

load_dotenv()
db = RIMDB(
    usr_db=os.getenv('DB_USER'), 
    pass_db=os.getenv('DB_PASSWORD'), 
    host_db=os.getenv('DB_HOSTNAME'), 
    database=os.getenv('DB_DATABASE'), 
    driver=os.getenv('DB_DRIVER'), 
    base = 'DB', 
    port=os.getenv('DB_PORT'))
session = db.session
engine = db.engine
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vekn_id = Column(Integer, unique=True)
    nick_name = Column(String(20), nullable=False, unique=True)
    name = Column(String(80), nullable=False)
    country = Column(Integer, ForeignKey('countries.id'), nullable=False)
    state = Column(Integer)
    city = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(20), nullable=False)
    llave = Column(String(50))
    rol = Column(Integer, ForeignKey('roles.id'), default=3)

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(3), nullable=False, unique=True)
    country = Column(String(30), nullable=False, unique=True)

class State(Base):
    __tablename__ = 'states'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(3), nullable=False)
    state = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False, unique=True)
    __table_args__ = (UniqueConstraint('country_id', 'code'), )

class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False)
    id_country = Column(Integer, ForeignKey('countries.id'), nullable=False)
    __table_args__ = (UniqueConstraint('id_country', 'city'),)

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    location = Column(String(100), nullable=False)
    __table_args__ = (UniqueConstraint('id_user', 'location'),)

class Inventario(Base):
    __tablename__ = 'inventarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_carta = Column(Integer, nullable=False)
    id_location = Column(Integer, ForeignKey('locations.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    offer = Column(Integer, nullable=False)
    __table_args__ = (UniqueConstraint('id_user', 'id_location', 'id_carta'),)

class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rol = Column(String(20))
    permiso = Column(String(10))

Base.metadata.create_all(engine)

class UserInput(BaseModel):
    username: str
    password: str

class NewUser(BaseModel):
    email: str
    password: str
    nick_name: str
    country: str
    city: str
    name: Optional[str] = None
    vekn_id: Optional[int] = None
    state: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None