#!/usr/bin/python3
""" State Module for HBNB project """
from models.place import place_amenity
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String
from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """ Amenity class """

    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)

    place_amenities = relationship(
        "Place",
        secondary=place_amenity,
        back_populates="amenities"
    )
