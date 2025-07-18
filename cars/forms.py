from django import forms
from .models import Car, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'image', 'mileage', 'fuel_type', 'car_type','engine_displacement','description',]
        widgets = {
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'car_type': forms.Select(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'engine_displacement': forms.NumberInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Unesite kratak opis automobila...'
            }),
           
        }
        


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'age', 'location']
        widgets = {
            'age': forms.NumberInput(attrs={'min': 0}),
            'location': forms.TextInput(attrs={'placeholder': 'Unesite lokaciju'}),
            'number_of_cars': forms.NumberInput(attrs={'min': 0}),
        }