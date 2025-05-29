from .models import CarMake, CarModel, Dealer

def initiate():
    car_make_data = [
        {"name": "Toyota", "description": "Japanese automotive manufacturer", "country": "Japan", "founded_year": 1937},
        {"name": "BMW", "description": "German luxury vehicle manufacturer", "country": "Germany", "founded_year": 1916},
        {"name": "Tesla", "description": "American electric vehicle manufacturer", "country": "USA", "founded_year": 2003},
        {"name": "Ford", "description": "American multinational automaker", "country": "USA", "founded_year": 1903},
        {"name": "Honda", "description": "Japanese multinational conglomerate", "country": "Japan", "founded_year": 1948}
    ]

    car_model_data = [
        # Toyota Models
        {"name": "Camry", "car_make": "Toyota", "type": "SEDAN", "year": 2023},
        {"name": "RAV4", "car_make": "Toyota", "type": "SUV", "year": 2023},
        {"name": "Prius", "car_make": "Toyota", "type": "HYBRID", "year": 2023},
        
        # BMW Models
        {"name": "3 Series", "car_make": "BMW", "type": "SEDAN", "year": 2023},
        {"name": "X5", "car_make": "BMW", "type": "SUV", "year": 2023},
        {"name": "M4", "car_make": "BMW", "type": "SPORTS", "year": 2023},
        
        # Tesla Models
        {"name": "Model 3", "car_make": "Tesla", "type": "ELECTRIC", "year": 2023},
        {"name": "Model Y", "car_make": "Tesla", "type": "ELECTRIC", "year": 2023},
        {"name": "Model S", "car_make": "Tesla", "type": "ELECTRIC", "year": 2023},
        
        # Ford Models
        {"name": "Mustang", "car_make": "Ford", "type": "SPORTS", "year": 2023},
        {"name": "F-150", "car_make": "Ford", "type": "TRUCK", "year": 2023},
        {"name": "Explorer", "car_make": "Ford", "type": "SUV", "year": 2023},
        
        # Honda Models
        {"name": "Civic", "car_make": "Honda", "type": "SEDAN", "year": 2023},
        {"name": "CR-V", "car_make": "Honda", "type": "SUV", "year": 2023},
        {"name": "Accord", "car_make": "Honda", "type": "SEDAN", "year": 2023}
    ]

    dealer_data = [
        {
            "id": 1,
            "name": "Best Cars",
            "city": "New York",
            "address": "123 Main St",
            "zip": "10001",
            "state": "NY",
            "lat": 40.7128,
            "long": -74.0060,
            "short_name": "BestCars NY",
            "full_name": "Best Cars New York"
        },
        {
            "id": 2,
            "name": "Premium Motors",
            "city": "Los Angeles",
            "address": "456 Hollywood Blvd",
            "zip": "90028",
            "state": "CA",
            "lat": 34.0522,
            "long": -118.2437,
            "short_name": "Premium LA",
            "full_name": "Premium Motors Los Angeles"
        },
        {
            "id": 3,
            "name": "Elite Autos",
            "city": "Chicago",
            "address": "789 Michigan Ave",
            "zip": "60601",
            "state": "IL",
            "lat": 41.8781,
            "long": -87.6298,
            "short_name": "Elite CHI",
            "full_name": "Elite Autos Chicago"
        },
        {
            "id": 4,
            "name": "Luxury Cars",
            "city": "Miami",
            "address": "321 Ocean Dr",
            "zip": "33139",
            "state": "FL",
            "lat": 25.7617,
            "long": -80.1918,
            "short_name": "Luxury MIA",
            "full_name": "Luxury Cars Miami"
        },
        {
            "id": 5,
            "name": "Classic Motors",
            "city": "Houston",
            "address": "654 Texas Ave",
            "zip": "77001",
            "state": "TX",
            "lat": 29.7604,
            "long": -95.3698,
            "short_name": "Classic HOU",
            "full_name": "Classic Motors Houston"
        }
    ]

    # Create car makes
    for make_data in car_make_data:
        CarMake.objects.get_or_create(
            name=make_data["name"],
            defaults={
                "description": make_data["description"],
                "country": make_data["country"],
                "founded_year": make_data["founded_year"]
            }
        )

    # Create car models
    for model_data in car_model_data:
        car_make = CarMake.objects.get(name=model_data["car_make"])
        CarModel.objects.get_or_create(
            name=model_data["name"],
            car_make=car_make,
            defaults={
                "type": model_data["type"],
                "year": model_data["year"]
            }
        )

    # Create dealers
    for dealer_data in dealer_data:
        Dealer.objects.get_or_create(
            id=dealer_data["id"],
            defaults={
                "name": dealer_data["name"],
                "city": dealer_data["city"],
                "address": dealer_data["address"],
                "zip": dealer_data["zip"],
                "state": dealer_data["state"],
                "lat": dealer_data["lat"],
                "long": dealer_data["long"],
                "short_name": dealer_data["short_name"],
                "full_name": dealer_data["full_name"]
            }
        )
