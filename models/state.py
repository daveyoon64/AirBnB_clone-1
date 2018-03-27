#!/usr/bin/python3
'''
    Implementation of the State class
'''
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import os


class State(BaseModel, Base):
    '''
        Implementation for the State.
    '''
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        cities = relationship("City", backref='state',
                              cascade="all, delete, delete-orphan")
    else:
        @property
        def cities(self):
            '''
            Code for FileStorage & returns list of cities
            '''
            match = []
            all_cities = models.storage.all(City)
            for k, v in all_cities.items():
                if v.state_id == self.id:
                    match.append(v)
            return match
