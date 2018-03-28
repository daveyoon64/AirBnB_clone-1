#!/usr/bin/python3
'''
    describe DBstorage
'''
from models.base_model import Base
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
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
        if os.environ['HBNB_ENV'] == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            query current database session for all objects depending on cls.
        '''
        match = {}
        if not cls:
            result = self.__session.query(State, City).all()
            for element in result:
                for obj in element:
                    key = "{}.{}".format(type(obj), obj.id)
                    match[key] = obj
        else:
            if cls == 'State':
                result = self.__session.query(State).all()
            elif cls == 'City':
                result = self.__ession.query(City).all()
            elif cls == 'User':
                result = self.__session.query(User).all()
            elif cls == 'Place':
                result = self.__session.query(Place).all()
            for element in result:
                key = "{}.{}".format(type(element), element.id)
                match[key] = element
        return match

    def new(self, obj):
        '''
            add object to current session.
        '''
        self.__session.add(obj)

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

    def reload(self):
        '''
          reload stuff
        '''
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
