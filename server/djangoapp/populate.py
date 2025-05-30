from djangoapp.models import CarMake, CarModel, Dealer


def initiate():
    car_make_data = [
        {"name": "NISSAN", "description": "Great cars. Japanese technology"},
        {"name": "Mercedes", "description": "Great cars. German luxury"},
        {"name": "Audi", "description": "Great cars. German technology"},
        {"name": "Kia", "description": "Great cars. Korean technology"},
        {"name": "Toyota", "description": "Great cars. Japanese technology"},
    ]

    car_make_instances = []
    for data in car_make_data:
        car_make_instances.append(
            CarMake.objects.create(
                name=data['name'],
                description=data['description']
            )
        )

    # Create CarModel instances with the corresponding CarMake instances
    car_model_data = [
        {"name": "Pathfinder", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[0]},
        {"name": "Qashqai", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[0]},
        {"name": "XTRAIL", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[0]},
        {"name": "A-Class", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[1]},
        {"name": "C-Class", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[1]},
        {"name": "E-Class", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[1]},
        {"name": "A4", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[2]},
        {"name": "A5", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[2]},
        {"name": "A6", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[2]},
        {"name": "Sorrento", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[3]},
        {"name": "Carnival", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[3]},
        {"name": "Cerato", "type": "Sedan", "year": 2023,
         "car_make": car_make_instances[3]},
        {"name": "Corolla", "type": "Sedan", "year": 2023,
         "car_make": car_make_instances[4]},
        {"name": "Camry", "type": "Sedan", "year": 2023,
         "car_make": car_make_instances[4]},
        {"name": "Kluger", "type": "SUV", "year": 2023,
         "car_make": car_make_instances[4]},
    ]

    for data in car_model_data:
        CarModel.objects.create(
            name=data['name'],
            car_make=data['car_make'],
            car_type=data['type'],
            year=data['year']
        )

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
