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
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine)
        session = Session()

        if os.environ['HBNB_ENV'] == 'test':
            # DROP ALL tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            query current database session for all objects depending on cls.
        '''
        Session = sessionmaker(bind=self.__engine)
        session = Session()
        if cls is None:
            result = session.query(User, State, City, Amentiy,
                                   Place, Review).all()
        else:
            if cls == 'State':
                result = session.query(State).all()
            elif cls == 'City':
                result = session.query(City).all()
        match = {}
        for element in result:
            key = "{}.{}".format(type(element), element.id)
            match[key] = element
        return match

    def new(self, obj):
        '''
            add object to current session.
        '''
        Session = sessionmaker(bind=self.__engine)
        session = Session()
        session.add(obj)
        session.commit()

    def save(self):
        '''
            commit all changes to current session.
        '''
        Session = sessionmaker(bind=self.__engine)
        session = Session()
        session.commit()

    def delete(self, obj=None):
        '''
            delete from current sesssion
        '''
        Session = sessionmaker(bind=self.__engine)
        session = Session()
        session.delete(obj)
        session.commit()

    def reload(self):
        '''
          reload stuff
        '''
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format
                                      (os.environ['HBNB_MYSQL_USER'],
                                       os.environ['HBNB_MYSQL_PWD'],
                                       os.environ['HBNB_MYSQL_HOST'],
                                       os.environ['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session())
