from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def login(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        auth_login(request, user)
        return redirect('main')
    else:
        return redirect('home')

def logout(request):
    auth_logout(request)
    return redirect('home')
