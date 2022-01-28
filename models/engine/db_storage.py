#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from os import getenv
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import sessionmaker


class DBStorage:
    """This class manages storage of hbnb models in MySQL Database."""

    __engine = None
    __session = None

    def __init__(self):
        """init method holding startup content of instance.

        Args:
            self (object): <class 'main.DBStorage'> type object

        Returns:
            None
        """
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:{}/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                3306,
                getenv("HBNB_MYSQL_DB")
            ), pool_pre_ping=True
        )
        if getenv("HBNB_ENV") == "test":
            from models.amenity import Amenity
            from models.city import City
            from models.place import Place
            from models.review import Review
            from models.state import State
            from models.user import User
            from models.base_model import Base

            Base.metadata.drop_all(bind=self.__engine)
        return None

    def all(self, cls=None):
        """Query on current session.

        Query using `self.__session` all objects depending on the class name
        i.e. cls

        Args:
            self (object): <class 'main.DBStorage'> type object
            cls (class, optional): Mapped class to query from

        Returns:
            None
        """
        dictionary = {}
        if cls:
            for obj in self.__session.query(cls).all():
                dictionary[type(obj).__name__ + '.' + obj.id] = obj
        else:
            from models.amenity import Amenity
            from models.city import City
            from models.place import Place
            from models.review import Review
            from models.state import State
            from models.user import User
            for clss in [City, State, Place, User]:
                for obj in self.__session.query(clss).all():
                    dictionary[type(obj).__name__ + '.' + obj.id] = obj
        return dictionary

    def new(self, obj):
        """Add the object to the current database session.

        Args:
            self (object): <class 'main.DBStorage'> type object
            obj (object): An object to add to self.__session

        Returns:
            None
        """
        self.__session.add(obj)
        return None

    def save(self):
        """Commit all changes of the current database session.

        Args:
            self (object): <class 'main.DBStorage'> type object

        Returns:
            None
        """
        self.__session.commit()
        return None

    def delete(self, obj=None):
        """Delete from current database session.

        Args:
            self (object): <class 'main.DBStorage'> type object
            obj (object): object to delete from session if not `None`

        Returns:
            None
        """
        if obj:
            self.__session.delete(obj)
        return None

    def reload(self):
        """Create all tables and current database session.

        Args:
            self (object): <class 'main.DBStorage'> type object

        Returns:
            None
        """
        from models.amenity import Amenity
        from models.base_model import Base
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine)
        Session = scoped_session(session_factory)
        self.__session = Session()
