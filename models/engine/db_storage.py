#!/usr/bin/python3
'''
    describe DBstorage
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


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
                                      (os.env['HBNB_MYSQL_USER'],
                                          os.env['HBNB_MYSQL_PWD'],
                                          os.env['HBNB_MYSQL_HOST'],
                                          os.env['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        if os.env['HBNB_ENV'] == 'test':
            # DROP ALL tables
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
            query current database session for all objects depending on cls.
        '''
        Session = sessionmaker(bind=engine)
        session = Session()
        if cls is None:
            result = session.query(User, State, City, Amentiy,
                                   Place, Review).all()
        else:
            result = session.query(cls).all()
        match = {}
        for element in result:
            key = "{}.{}".format(type(element), element.id)
            match[key] = element
        return match

    def new(self, obj):
        '''
            add object to current session.
        '''
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(obj)
        session.commit()

    def save(self):
        '''
            commit all changes to current session.
        '''
        session.commit()

    def delete(self, obj=None):
        '''
            delete from current sesssion
        '''
        session.delete(obj)
        session.commit()

    def reload(self):
        '''
          reload stuff
        '''
        from models.city import City
        from models.state import State

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format
                                      (os.env['HBNB_MYSQL_USER'],
                                       os.env['HBNB_MYSQL_PWD'],
                                       os.env['HBNB_MYSQL_HOST'],
                                       os.env['HBNB_MYSQL_DB']),
                                      pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

        Session = sessionmaker(bind=engine, expire_on_commit=False)
        session = scoped_session(Session())
