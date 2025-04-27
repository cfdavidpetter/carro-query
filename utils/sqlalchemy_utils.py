def clean_sqlalchemy_object(obj):
    """
    Clean SQLAlchemy object by removing internal attributes and converting to a clean dictionary.
    
    Args:
        obj: SQLAlchemy model instance
        
    Returns:
        dict: Clean dictionary with only the model's attributes
    """
    if hasattr(obj, '__dict__'):
        return {
            key: value for key, value in obj.__dict__.items()
            if not key.startswith('_')
        }
    return obj 


def add_exact_match_condition(conditions: list, value: any, field: any) -> None:
    if value is not None:
        conditions.append(field == value)

def add_range_condition(conditions: list, min_value: any, max_value: any, field: any) -> None:
    if min_value is not None:
        conditions.append(field >= min_value)
    if max_value is not None:
        conditions.append(field <= max_value)

def add_text_search_condition(conditions: list, value: str, field: any) -> None:
    if value is not None:
        conditions.append(field.ilike(f"%{value}%"))
