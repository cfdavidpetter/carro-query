import random

from faker import Faker
from models import Brand, Model, Car, FuelType, TransmissionType
from datetime import datetime
from config import get_db

fake = Faker('pt_BR')

def create_brands(db):
    brands = [
        "Toyota", "Honda", "Volkswagen", "Fiat", "Chevrolet",
        "Ford", "Hyundai", "Renault", "Nissan", "BMW", "Mercedes-Benz", 
        "Audi", "Volvo", "Porsche", "Lamborghini", "Ferrari", "Maserati", 
        "Peugeot", "Citroën", "Jeep", "Kia", "Suzuki", "Mitsubishi", 
        "Subaru", "Chery", "JAC Motors"
    ]
    brand_objects = []
    for brand_name in brands:
        existing_brand = db.query(Brand).filter(Brand.name == brand_name).first()
        if existing_brand:
            brand_objects.append(existing_brand)
        else:
            brand = Brand(
                name=brand_name,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            brand_objects.append(brand)
            db.add(brand)
    
    db.commit()
    return brand_objects

def create_models(db, brands):
    model_data = {
        "Toyota": ["Corolla", "Camry", "RAV4", "Hilux", "Yaris", "Land Cruiser", "Prius"],
        "Honda": ["Civic", "Accord", "CR-V", "HR-V", "Fit", "City", "Pilot"],
        "Volkswagen": ["Golf", "Polo", "Tiguan", "Amarok", "Jetta", "Passat", "T-Cross"],
        "Fiat": ["Uno", "Palio", "Argo", "Toro", "Mobi", "Pulse", "Cronos"],
        "Chevrolet": ["Onix", "Cruze", "Tracker", "S10", "Spin", "Cobalt", "Montana"],
        "Ford": ["Ka", "Focus", "EcoSport", "Ranger", "Fusion", "Fiesta", "Edge"],
        "Hyundai": ["HB20", "Creta", "Santa Fe", "Tucson", "i30", "Azera", "Kona"],
        "Renault": ["Kwid", "Sandero", "Duster", "Captur", "Logan", "Oroch", "Megane"],
        "Nissan": ["March", "Versa", "Kicks", "Frontier", "Sentra", "Altima", "X-Trail"],
        "BMW": ["320i", "X1", "X3", "X5", "X6", "M3", "i8"],
        "Mercedes-Benz": ["A-Class", "C-Class", "E-Class", "S-Class", "GLA", "GLC", "GLE"],
        "Audi": ["A3", "A4", "A5", "A6", "Q3", "Q5", "Q7"],
        "Volvo": ["V40", "V60", "V70", "V90", "XC40", "XC60", "XC90"],
        "Porsche": ["911", "718", "Taycan", "Macan", "Panamera", "Cayenne"],
        "Lamborghini": ["Huracan", "Aventador", "Urus", "Countach", "Gallardo", "Murcielago"],
        "Ferrari": ["488", "812", "F8", "SF90", "Roma", "Portofino", "LaFerrari"],
        "Maserati": ["Ghibli", "Levante", "Quattroporte", "MC20", "GranTurismo", "GranCabrio"],
        "Peugeot": ["208", "2008", "3008", "308", "508", "5008"],
        "Citroën": ["C3", "C4 Cactus", "C5 Aircross", "Berlingo", "DS3"],
        "Jeep": ["Renegade", "Compass", "Wrangler", "Cherokee", "Grand Cherokee", "Gladiator"],
        "Kia": ["Sportage", "Sorento", "Cerato", "Seltos", "Picanto", "Rio", "Stinger"],
        "Suzuki": ["Swift", "Vitara", "Jimny", "SX4", "S-Cross"],
        "Mitsubishi": ["Lancer", "ASX", "Outlander", "Pajero", "Eclipse Cross"],
        "Subaru": ["Impreza", "Forester", "Outback", "XV", "WRX"],
        "Chery": ["Tiggo 2", "Tiggo 5X", "Tiggo 7", "Tiggo 8", "Arrizo 5"],
        "JAC Motors": ["T40", "T50", "T60", "T80", "iEV40"],
    }
    
    model_objects = []
    for brand in brands:
        for model_name in model_data[brand.name]:
            model = Model(
                brand_id=brand.id,
                name=model_name,
                engine_displacement=round(random.uniform(1.0, 3.0), 1),
                fuel_type=random.choice(list(FuelType)),
                consumption=round(random.uniform(8.0, 15.0), 1),
                transmission=random.choice(list(TransmissionType)),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            model_objects.append(model)
    db.add_all(model_objects)
    db.commit()
    return model_objects

def create_cars(db, models):
    colors = ["Preto", "Branco", "Prata", "Vermelho", "Azul", "Cinza", "Verde", "Amarelo", "Roxo", "Laranja"]
    cars = []
    
    for model in models:
        for _ in range(100):
            year = random.randint(2001, 2025)
            doors = random.choice([2, 4])
            accents = 2 if doors == 2 else random.choice([5, 7])
            car = Car(
                model_id=model.id,
                year=year,
                color=random.choice(colors),
                kilometers=random.randint(0, 100000),
                doors=doors,
                accents=accents,
                price=round(random.uniform(30000, 200000), 2),
                description=fake.text(max_nb_chars=200),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            cars.append(car)
    
    db.add_all(cars)
    db.commit()

def main():
    db = get_db()
    try:
        print("Creating brands...")
        brands = create_brands(db)
        
        print("Creating models...")
        models = create_models(db, brands)
        
        print("Creating cars...")
        create_cars(db, models)
        
        print("Seed completed successfully!")
    except Exception as e:
        print(f"Error during seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 
