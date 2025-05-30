# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class Dealer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=10)
    state = models.CharField(max_length=2)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True)
    founded_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(now().year)],
        null=True,
        blank=True
    )
    website = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SEDAN = 'SEDAN'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TRUCK = 'TRUCK'
    VAN = 'VAN'
    SPORTS = 'SPORTS'
    LUXURY = 'LUXURY'
    HYBRID = 'HYBRID'
    ELECTRIC = 'ELECTRIC'
    
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (TRUCK, 'Truck'),
        (VAN, 'Van'),
        (SPORTS, 'Sports'),
        (LUXURY, 'Luxury'),
        (HYBRID, 'Hybrid'),
        (ELECTRIC, 'Electric'),
    ]
    
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=CAR_TYPES, default=SUV)
    year = models.IntegerField(
        validators=[MinValueValidator(2015), MaxValueValidator(2023)]
    )
    color = models.CharField(max_length=50, blank=True)
    engine = models.CharField(max_length=100, blank=True)
    transmission = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.car_make.name} {self.name}"

class CarDealerReview(models.Model):
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    review = models.TextField()
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.IntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"Review by {self.name} for {self.dealership.full_name}"
