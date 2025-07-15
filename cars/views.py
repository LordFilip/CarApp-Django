from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import CarForm, RegisterForm
from django.contrib.auth import logout as auth_logout
from django.db.models import Q

# Create your views here.

def car_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})


@login_required
def profile(request):
    cars = Car.objects.filter(owner= request.user)
    return render (request, 'cars/profile.html', {'cars': cars})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


#@login_required
#def add_car(request):
#   return redirect('add_car')

def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    

    same_owner_cars = Car.objects.filter(owner = car.owner).exclude(id=car.id)[:4]

    if same_owner_cars.count()<4:
        needed = 4- same_owner_cars.count()
        other_cars = Car.objects.exclude(
            Q(id=car.id) | Q(id__in=same_owner_cars.values_list('id',flat=True))
        )[:needed]
        related_cars = list(same_owner_cars) + list(other_cars)
    else:
        related_cars = same_owner_cars

    return render(request, 'cars/car_details.html', {'car': car, 'related_cars': related_cars})



@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('profile')
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})

@login_required
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    
    if car.owner != request.user:
        return redirect('car_details', car_id=car.id)

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_details', car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_edit.html', {'form': form, 'car': car})


@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return redirect('car_details', car_id=car.id)

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'cars/car_delete_confirm.html', {'car': car})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            owner = form.save()
            login(request,owner)
            return redirect('car_list')
    else:
        form = RegisterForm()
    return render(request, 'cars/register.html', {'form': form})