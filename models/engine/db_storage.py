#!/usr/bin/python3
'''
    describe DBstorage
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
import os


class DBStorage:
    '''
        Define DBStorage
    '''
    __engine = None
    __session = None

    def __init__(self):
        '''
            initialize DBStorage instance
        '''
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format
                                      (os.environ['HBNB_MYSQL_USER'],
                                          os.environ['HBNB_MYSQL_PWD'],
                                          os.environ['HBNB_MYSQL_HOST'],
                                          os.environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            query current database session for all objects depending on cls.
        '''
        match = {}
        if not cls:
            result = self.__session.query(State, City,
                                          Place, User, Review).all()
            for element in result:
                for obj in element:
                    key = "{}.{}".format(type(obj), obj.id)
                    match[key] = obj
        else:
            if cls == 'State':
                result = self.__session.query(State).all()
            elif cls == 'City':
                result = self.__session.query(City).all()
            elif cls == 'User':
                result = self.__session.query(User).all()
            elif cls == 'Place':
                result = self.__session.query(Place).all()
            elif cls == 'Review':
                result = self.__session.query(Review).all()
            for element in result:
                key = "{}.{}".format(type(element), element.id)
                match[key] = element
        return match

    def new(self, obj):
        '''
            add object to current session.
        '''
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        '''
            commit all changes to current session.
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
            delete from current sesssion
        '''
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        '''
          reload stuff
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
