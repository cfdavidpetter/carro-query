from database.config import get_db
from database.models import Car, Model, Brand
from sqlalchemy import func
from typing import Dict, Any, Tuple

db = get_db()

async def count_cars_by_attribute(attribute: str) -> Tuple[Dict[str, Any], int]:
    """
    Count cars grouped by a specific attribute.
    
    Args:
        attribute (str): The attribute to group by. Can be any field from Car, Model, or Brand.
            Examples:
            - Car attributes: year, color, kilometers, doors, accents, price
            - Model attributes: name, engine_displacement, fuel_type, consumption, transmission
            - Brand attributes: name
    
    Returns:
        tuple: A tuple containing:
            - dict: Response with counts grouped by attribute or error message
            - int: HTTP status code (200 for success, 400 for bad request, 500 for server error)
    """
    try:
        attribute_map = {
            'year': (Car, Car.year),
            'color': (Car, Car.color),
            'kilometers': (Car, Car.kilometers),
            'doors': (Car, Car.doors),
            'accents': (Car, Car.accents),
            'price': (Car, Car.price),
            'model_name': (Model, Model.name),
            'engine_displacement': (Model, Model.engine_displacement),
            'fuel_type': (Model, Model.fuel_type),
            'consumption': (Model, Model.consumption),
            'transmission': (Model, Model.transmission),
            'brand_name': (Brand, Brand.name)
        }

        if attribute not in attribute_map:
            return {
                "error": f"Invalid attribute. Must be one of: {', '.join(attribute_map.keys())}"
            }, 400

        model, column = attribute_map[attribute]
        
        if model == Car:
            query = db.query(column, func.count(Car.id)).group_by(column)
        elif model == Model:
            query = db.query(column, func.count(Car.id)).join(Car).group_by(column)
        elif model == Brand:
            query = db.query(column, func.count(Car.id)).join(Model).join(Car).group_by(column)
        else:
            return {"error": "Invalid model. Must be one of: Car, Model, Brand"}, 400

        results = query.all()
        formatted_results = [
            {
                "attribute_value": str(value) if value is not None else "null",
                "count": count
            }
            for value, count in results
        ]

        return {
            "attribute": attribute,
            "counts": formatted_results
        }, 200

    except Exception as e:
        return {"error": str(e)}, 500 
