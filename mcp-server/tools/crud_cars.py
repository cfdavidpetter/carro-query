from database.config import get_db
from database.models import Car, Model, Brand, FuelType, TransmissionType
from utils.sqlalchemy_utils import clean_sqlalchemy_object
from typing import Dict, Any, Tuple
from sqlalchemy import or_

db = get_db()

async def create_car(car_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """
    Create a new car in the database.
    
    Args:
        car_data (dict): Dictionary containing car information including:
            - brand_name (str): Name of the car brand
            - model_name (str): Name of the car model
            - year (int): Year of the car
            - color (str): Color of the car
            - kilometers (int): Kilometers of the car
            - doors (int): Number of doors
            - accents (int): Number of accents
            - price (float): Price of the car
            - description (str, optional): Description of the car
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with created car or error message
            - int: HTTP status code (201 for success, 400 for bad request, 500 for server error)
    """
    try:
        required_fields = ['brand_name', 'model_name', 'year', 'color', 'kilometers', 'doors', 'accents', 'price']
        for field in required_fields:
            if field not in car_data:
                return {"error": f"Missing required field: {field}"}, 400

        brand = db.query(Brand).filter(Brand.name.ilike(car_data['brand_name'])).first()
        if not brand:
            return {"error": f"Brand '{car_data['brand_name']}' not found, you can add it to the database first"}, 404

        model = db.query(Model).filter(
            Model.brand_id == brand.id,
            Model.name.ilike(car_data['model_name'])
        ).first()
        if not model:
            return {"error": f"Model '{car_data['model_name']}' not found for brand '{brand.name}', you can add it to the database first"}, 404

        car_create_data = {
            'model_id': model.id,
            'year': car_data['year'],
            'color': car_data['color'],
            'kilometers': car_data['kilometers'],
            'doors': car_data['doors'],
            'accents': car_data['accents'],
            'price': car_data['price'],
            'description': car_data.get('description')
        }

        new_car = Car(**car_create_data)
        db.add(new_car)
        db.commit()
        db.refresh(new_car)

        result = {
            **clean_sqlalchemy_object(new_car),
            "model": {
                **clean_sqlalchemy_object(new_car.model),
                "brand": clean_sqlalchemy_object(new_car.model.brand)
            }
        }

        return {"car": result}, 201

    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500

async def get_car(car_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Retrieve a specific car by ID.
    
    Args:
        car_id (int): ID of the car to retrieve
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with car details or error message
            - int: HTTP status code (200 for success, 404 for not found, 500 for server error)
    """
    try:
        car = db.query(Car).join(Model).join(Brand).filter(Car.id == car_id).first()
        
        if not car:
            return {"error": "Car not found"}, 404

        result = {
            **clean_sqlalchemy_object(car),
            "model": {
                **clean_sqlalchemy_object(car.model),
                "brand": clean_sqlalchemy_object(car.model.brand)
            }
        }
        
        return {"car": result}, 200

    except Exception as e:
        return {"error": str(e)}, 500

async def update_car(car_id: int, car_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """
    Update an existing car in the database.
    
    Args:
        car_id (int): ID of the car to update
        car_data (dict): Dictionary containing car information to update including:
            - year (int, optional): Year of the car
            - color (str, optional): Color of the car
            - kilometers (int, optional): Kilometers of the car
            - doors (int, optional): Number of doors
            - accents (int, optional): Number of accents
            - price (float, optional): Price of the car
            - description (str, optional): Description of the car
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with updated car or error message
            - int: HTTP status code (200 for success, 404 for not found, 500 for server error)
    """
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        
        if not car:
            return {"error": "Car not found, you can add it to the database first"}, 404

        updateable_fields = ['year', 'color', 'kilometers', 'doors', 'accents', 'price', 'description']
        for field in updateable_fields:
            if field in car_data:
                setattr(car, field, car_data[field])

        db.commit()
        db.refresh(car)

        result = {
            **clean_sqlalchemy_object(car),
            "model": {
                **clean_sqlalchemy_object(car.model),
                "brand": clean_sqlalchemy_object(car.model.brand)
            }
        }

        return {"car": result}, 200

    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500

async def delete_car(car_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Delete a car from the database.
    
    Args:
        car_id (int): ID of the car to delete
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with success message or error
            - int: HTTP status code (200 for success, 404 for not found, 500 for server error)
    """
    try:
        car = db.query(Car).filter(Car.id == car_id).first()
        
        if not car:
            return {"error": "Car not found"}, 404

        db.delete(car)
        db.commit()

        return {"message": "Car successfully deleted"}, 200

    except Exception as e:
        db.rollback()
        return {"error": str(e)}, 500
