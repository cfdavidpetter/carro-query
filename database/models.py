from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from database.config import Base

class FuelType(enum.Enum):
    GASOLINE = "gasoline"
    ETHANOL = "ethanol"
    DIESEL = "diesel"
    FLEX = "flex"
    HYBRID = "hybrid"
    ELECTRIC = "electric"

class TransmissionType(enum.Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    SEMI_AUTOMATIC = "semi_automatic"
    CVT = "cvt"

class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    models = relationship("Model", back_populates="brand")

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    name = Column(String(100), nullable=False)
    engine_displacement = Column(Float, nullable=False)
    fuel_type = Column(Enum(FuelType), nullable=False)
    consumption = Column(Float, nullable=False)
    transmission = Column(Enum(TransmissionType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    brand = relationship("Brand", back_populates="models")
    cars = relationship("Car", back_populates="model")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String(50), nullable=False)
    kilometers = Column(Integer, nullable=False)
    doors = Column(Integer, nullable=False)
    accents = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    model = relationship("Model", back_populates="cars") 
