from database.config import get_db
from database.models import Car, Model, Brand
from utils.sqlalchemy_utils import clean_sqlalchemy_object

db = get_db()

async def get_all_cars():
    """
    Retrieve all cars from the database with their associated model and brand information.
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with all cars or error message
                - cars (list): List of car objects, each containing:
                    - car details (from clean_sqlalchemy_object)
                    - model (dict): Model information including:
                        - model details (from clean_sqlalchemy_object)
                        - brand (dict): Brand information (from clean_sqlalchemy_object)
            - int: HTTP status code (200 for success, 500 for server error)
    """
    try:
        cars = db.query(Car).join(Model).join(Brand).all()
        
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
