#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey


class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))

    places = relationship("Place", backref="user",
                          cascade="all, delete, delete-orphan")

    reviews = relationship("Review", backref="user",
                           cascade="delete")
