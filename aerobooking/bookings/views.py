from django.shortcuts import render

# Create your views here.

def home(request):
    context = {
        'user': request.user,
    }
    return render(request, 'home.html', context)

def about(request):
    context = {
        'user': request.user,
    }
    return render(request, 'about.html', context)
