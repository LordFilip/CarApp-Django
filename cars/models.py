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
    description = models.TextField(
        max_length=1000,
        blank=True,
        help_text='Kratak opis automobila (opciono)'
    )
    engine_displacement = models.PositiveIntegerField(
        help_text="Engine displacement in cubic centimeters (e.g. 1600)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True,blank=True, help_text='Unesite svoje godine')
    location = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def number_of_cars(self):
        return self.user.car_set.count()

    def cars(self):
        return self.user.car_set.all()

    def __str__(self):
        return f"{self.user.username} - {self.age} god."



