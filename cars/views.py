from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Car
from .forms import CarForm, RegisterForm
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

def car_list(request):
    fuel_filter = request.GET.get('fuel_type')
    car_type_filter = request.GET.get('car_type')
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    displacement_min = request.GET.get('displacement_min')
    displacement_max = request.GET.get('displacement_max')

    cars = Car.objects.all().order_by('-created_at')


    if fuel_filter:
        cars = cars.filter(fuel_type=fuel_filter)
    if car_type_filter:
        cars = cars.filter(car_type=car_type_filter)
    if year_min:
        cars = cars.filter(year__gte=year_min)
    if year_max:
        cars = cars.filter(year__lte=year_max)
    if displacement_min:
        cars = cars.filter(engine_displacement__gte=displacement_min)
    if displacement_max:
        cars = cars.filter(engine_displacement__lte=displacement_max)

    fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct()
    car_types = Car.objects.values_list('car_type', flat=True).distinct()

    return render(request, 'cars/car_list.html', {
        'cars': cars,
        'fuel_types': fuel_types,
        'car_types': car_types,
        'selected_fuel': fuel_filter,
        'selected_car_type': car_type_filter,
        'year_min': year_min,
        'year_max': year_max,
        'displacement_min': displacement_min,
        'displacement_max': displacement_max,
    })




@login_required
def profile(request):
    cars = Car.objects.filter(owner= request.user)
    return render (request, 'cars/profile.html', {'cars': cars})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@require_POST
def guest_login(request):
    
    guest_user, created = User.objects.get_or_create(username='guest')

    
    if created:
        guest_user.set_unusable_password() 
        guest_user.save()

   
    login(request, guest_user)

    
    return redirect('car_list')




def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    same_owner_cars = Car.objects.filter(owner=car.owner).exclude(id=car.id)[:4]
    related_cars = list(same_owner_cars)
    count = len(related_cars)

    if count < 4:
        needed = 4 - count
        same_type_cars = Car.objects.filter(car_type=car.car_type).exclude(
            Q(id=car.id) | Q(id__in=[c.id for c in related_cars])
        )[:needed]
        related_cars.extend(same_type_cars)
        count = len(related_cars)

    if count < 4:
        needed = 4 - count
        other_cars = Car.objects.exclude(
            Q(id=car.id) | Q(id__in=[c.id for c in related_cars])
        )[:needed]
        related_cars.extend(other_cars)

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