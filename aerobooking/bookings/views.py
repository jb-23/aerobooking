from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    context = {
        'user': request.user,
    }
    return render(request, 'home.html', context)

@login_required(redirect_field_name='')
def bookings_list(request):
    data = []
    requested_data = []
    context = {
        'bookings': data,
        'requested_bookings': requested_data,
        'user': request.user,
    }
    return render(request, 'bookings-list.html', context)

def about(request):
    context = {
        'user': request.user,
    }
    return render(request, 'about.html', context)
