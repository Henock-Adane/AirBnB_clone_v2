#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String
from models.base_model import Base, BaseModel


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False,)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    reviews = relationship("Review",
                           backref="place",
                           cascade="all, delete, delete-orphan")

    @property
    def reviews(self):
        """Getter attribute that returns list of Review instances.

        Returns review instances with `place_id` equal to the current
        `Place.id`

        Args:
            self (object): <class 'main.Place'> type object

        Returns:
            List of review instances where `place_id` = Place.id
        """
        req_reviews = []
        from models import storage
        for *_, v in storage.all():
            if v.__class__.__name__ == "Review" and v.place_id == self.id:
                req_reviews.append(v)
        return req_reviews
