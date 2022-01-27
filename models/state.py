#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship('City',
                          backref="cities",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """Returns the list of City instances linked to a state.

        Args:
            self (object): <class 'main.State'> type object

        Returns:
            List of all cities linked to a state
        """
        req_cities = []
        from models import storage
        for *_, v in storage.all():
            if v.__class__.__name__ == "City" and v.state_id == self.id:
                req_cities.append(v)
        return req_cities
