from sqlalchemy import and_
from utils.sqlalchemy_utils import clean_sqlalchemy_object, add_exact_match_condition, add_range_condition, add_text_search_condition
from database.config import get_db
from database.models import Car, Model, Brand
from .models import CarFilter

db = get_db()

async def filter_cars(filters: CarFilter):
    """
    Filter cars based on various criteria.
    
    Args:
        filters (CarFilter): Filter criteria with the following attributes:
            - year (Optional[int]): Year of the car
            - color (Optional[str]): Color of the car
            - min_kilometers (Optional[int]): Minimum kilometers
            - max_kilometers (Optional[int]): Maximum kilometers
            - doors (Optional[int]): Number of doors
            - accents (Optional[int]): Number of accents
            - min_price (Optional[float]): Minimum price
            - max_price (Optional[float]): Maximum price
            - description (Optional[str]): Description text to search for
            - model_name (Optional[str]): Name of the model to search for
            - brand_name (Optional[str]): Name of the brand to search for
            - min_engine_displacement (Optional[float]): Minimum engine displacement
            - max_engine_displacement (Optional[float]): Maximum engine displacement
            - fuel_type (Optional[gasoline, ethanol, diesel, flex, hybrid, electric]): Type of fuel
            - min_consumption (Optional[float]): Minimum fuel consumption
            - max_consumption (Optional[float]): Maximum fuel consumption
            - transmission (Optional[manual, automatic, semi_automatic, cvt]): Type of transmission
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with filtered cars or error message
            - int: HTTP status code (200 for success, 400 for bad request, 500 for server error)
    """
    try:
        if all(param is None for param in [
            filters.year, filters.color, filters.min_kilometers, 
            filters.max_kilometers, filters.doors, filters.accents, 
            filters.min_price, filters.max_price, filters.description,
            filters.model_name, filters.brand_name, filters.min_engine_displacement, 
            filters.max_engine_displacement, filters.fuel_type, filters.min_consumption, 
            filters.max_consumption, filters.transmission
        ]):
            return {"error": "At least one filter parameter must be provided"}, 400

        query = db.query(Car).join(Model).join(Brand)
        conditions = []
        
        add_exact_match_condition(conditions, filters.year, Car.year)
        add_text_search_condition(conditions, filters.color, Car.color)
        add_range_condition(conditions, filters.min_kilometers, filters.max_kilometers, Car.kilometers)
        add_exact_match_condition(conditions, filters.doors, Car.doors)
        add_exact_match_condition(conditions, filters.accents, Car.accents)
        add_range_condition(conditions, filters.min_price, filters.max_price, Car.price)
        add_text_search_condition(conditions, filters.description, Car.description)
        add_text_search_condition(conditions, filters.model_name, Model.name)
        add_text_search_condition(conditions, filters.brand_name, Brand.name)
        add_range_condition(conditions, filters.min_engine_displacement, filters.max_engine_displacement, Model.engine_displacement)
        add_exact_match_condition(conditions, filters.fuel_type, Model.fuel_type)
        add_range_condition(conditions, filters.min_consumption, filters.max_consumption, Model.consumption)
        add_exact_match_condition(conditions, filters.transmission, Model.transmission)
        
        if conditions:
            query = query.filter(and_(*conditions))
        
        cars = query.all()
        
        results = [{
            **clean_sqlalchemy_object(car),
            "model": {
                **clean_sqlalchemy_object(car.model),
                "brand": clean_sqlalchemy_object(car.model.brand)
            }
        } for car in cars]
        
        return {"cars": results}, 200
    
    except Exception as e:
        return {"error": str(e)}, 500
