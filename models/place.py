#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Float, Integer, String
from models.base_model import Base, BaseModel


place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id",
           String(60),
           ForeignKey("places.id"),
           primary_key=True
           ),
    Column("amenity_id",
           String(60),
           ForeignKey("amenities.id"),
           primary_key=True
           )
)


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    amenity_ids = []
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(String(1024))
    name = Column(String(128), nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False,)

    reviews = relationship(
        "Review",
        backref="place",
        cascade="all, delete, delete-orphan"
    )

    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        viewonly=False,
        back_populates="place_amenities"
    )

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
