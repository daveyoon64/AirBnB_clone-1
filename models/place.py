#!/usr/bin/python3
'''
    Define the class Place.
'''
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from models.city import City
from models.user import User
import os


class Place(BaseModel, Base):
    '''
        Define the class Place that inherits from BaseModel.
    '''
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.environ['HBNB_TYPE_STORAGE'] == 'db':
        reviews = relationship('Review', backref='place',
                               cascade="delete")
    else:
        @property
        def reviews(self):
            '''
                returns the list of Review instances with
                place_id equals to the current Place.id
            '''
            match = []
            all_reviews = models.storage.all(Review)
            for k, v in all_reviews.items():
                if v.place_id == self.id:
                    match.append(v)
            return
