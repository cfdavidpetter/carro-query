from pydantic import BaseModel, Field
from typing import Optional
from database.models import FuelType, TransmissionType

class CarFilter(BaseModel):
    year: Optional[int] = Field(None, description="Year of the car")
    color: Optional[str] = Field(None, description="Color of the car")
    min_kilometers: Optional[int] = Field(None, description="Minimum kilometers")
    max_kilometers: Optional[int] = Field(None, description="Maximum kilometers")
    doors: Optional[int] = Field(None, description="Number of doors")
    accents: Optional[int] = Field(None, description="Number of accents")
    min_price: Optional[float] = Field(None, description="Minimum price")
    max_price: Optional[float] = Field(None, description="Maximum price")
    description: Optional[str] = Field(None, description="Description text to search for")
    model_name: Optional[str] = Field(None, description="Name of the model to search for")
    brand_name: Optional[str] = Field(None, description="Name of the brand to search for")
    min_engine_displacement: Optional[float] = Field(None, description="Minimum engine displacement")
    max_engine_displacement: Optional[float] = Field(None, description="Maximum engine displacement")
    fuel_type: Optional[FuelType] = Field(None, description="Type of fuel")
    min_consumption: Optional[float] = Field(None, description="Minimum fuel consumption")
    max_consumption: Optional[float] = Field(None, description="Maximum fuel consumption")
    transmission: Optional[TransmissionType] = Field(None, description="Type of transmission")
