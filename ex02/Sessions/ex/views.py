from django.shortcuts import render, redirect
from django.contrib.auth import  login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Tip
from .forms import TipForm, AUserCreationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'ex/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('homepage') 

def register(request):
    if request.method == 'POST':
        form = AUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = AUserCreationForm()
    return render(request, 'ex/register.html', {'form': form})

def homepage(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = TipForm(request.POST)
            if form.is_valid():
                tip = form.save(commit=False)
                tip.author = request.user
                tip.save()
                return redirect('homepage')
    else:
        form = TipForm()

    tips = Tip.objects.all()
    return render(request, 'ex/homepage.html', {'form': form, 'tips': tips})

