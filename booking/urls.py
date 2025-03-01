from django.urls import path
from . import views
from . views import *

urlpatterns = [
    path('', views.home, name='home'),  # This is your index/home page
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='registration'),
    path('profile/', views.user_profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('send_message/', views.sendMessage, name='send_message'),
    path('adminDashboard/', views.custom_admin, name='custom_admin'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('process-payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('booking-success/', views.booking_success, name='booking_success'),
    
]