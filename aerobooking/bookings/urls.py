from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('bookings', views.bookings, name='main'),
    #path('bookings-list', views.bookings_list, name='bookings_list'),
    #path('bookings/create', views.bookings_edit, name='bookings_create'),
    #path('bookings/<slug>', views.bookings_edit, name='bookings_edit'),
    path('about', views.about, name='about'),
]
