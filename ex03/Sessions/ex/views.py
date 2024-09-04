from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import  login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
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


@login_required
def upvote_tip(request, tip_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to upvote.")

    tip = get_object_or_404(Tip, id=tip_id)
    tip.upvote(request.user)
    return redirect('homepage')
@login_required
def downvote_tip(request, tip_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to downvote.")

    tip = get_object_or_404(Tip, id=tip_id)
    tip.downvote(request.user)
    return redirect('homepage')
@login_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    # Check if the user is the author of the tip
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You are not authorized to delete this tip.")

    tip.delete()
    return redirect('homepage')