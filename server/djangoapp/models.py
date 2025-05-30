# Uncomment the following imports before adding the Model code

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=1000)

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
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    SPORT = 'sport'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (SPORT, 'Sport'),
    ]
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField()
    car_type = models.CharField(max_length=20, choices=CAR_TYPES, default=SEDAN)
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2024)])

    def __str__(self):
        return self.name


class CarDealer(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    id = models.IntegerField(primary_key=True)
    lat = models.FloatField()
    long = models.FloatField()
    short_name = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.full_name

    def to_dict(self):
        return {
            'address': self.address,
            'city': self.city,
            'full_name': self.full_name,
            'id': self.id,
            'lat': self.lat,
            'long': self.long,
            'short_name': self.short_name,
            'st': self.st,
            'zip': self.zip
        }


class DealerReview(models.Model):
    dealership = models.IntegerField()
    name = models.CharField(max_length=100)
    purchase = models.BooleanField()
    review = models.CharField(max_length=1000)
    purchase_date = models.DateField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=100, default='neutral')

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'dealership': self.dealership,
            'name': self.name,
            'purchase': self.purchase,
            'review': self.review,
            'purchase_date': self.purchase_date.isoformat(),
            'car_make': self.car_make,
            'car_model': self.car_model,
            'car_year': self.car_year,
            'sentiment': self.sentiment
        }
