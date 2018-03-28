#!/usr/bin/python3
'''
    Implementation of the State class
'''
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.city import City
import os


class State(BaseModel, Base):
    '''
        Implementation for the State.
    '''
    __tablename__ = 'states'

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="delete")
    else:
        name = ""

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
