from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from cars import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.car_list, name = 'car_list'),
    path('admin/',admin.site.urls),

    path('profile', views.profile, name= 'profile'),
    path('add/', views.add_car, name="add_car"),
    path('car_details/<int:car_id>',views.car_details, name= 'car_details'),

    path('car_edit/<int:car_id>/', views.car_edit, name='car_edit'),
    path('car_delete/<int:car_id>/', views.car_delete, name='car_delete'),

    path("register/", views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name= "cars/login.html"), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('guest-login/', views.guest_login, name='guest_login'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)