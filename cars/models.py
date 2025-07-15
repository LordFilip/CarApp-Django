from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Car(models.Model):

    FUEL_CHOICES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
        ('LPG', 'LPG'),
    ]

    CAR_TYPE_CHOICES = [
        ('COUPE', 'Kupe'),
        ('SEDAN', 'Limuzina'),
        ('HATCHBACK', 'Hečbek'),
        ('SUV', 'SUV'),
        ('CONVERTIBLE', 'Kabriolet'),
        ('WAGON', 'Karavan'),
        ('PICKUP', 'Pickup'),
    ]

    owner = models.ForeignKey(User, on_delete = models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    image = models.ImageField(upload_to='car_images/', blank=False,null=False )
    mileage = models.PositiveIntegerField(help_text='Kilometraza')
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    car_type = models.CharField(max_length=15, choices=CAR_TYPE_CHOICES)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"





