from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from .models import Tip
from .forms import TipForm, AUserCreationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                print(f"User {user} authenticated")
                login(request, user)
                return redirect('homepage')
            else:
                print("Authentication failed")
    else:
        form = AuthenticationForm()
    return render(request, 'ex/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('homepage')  # Redirige a la página de inicio

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
    if request.method == 'POST' and request.user.is_authenticated:
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
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user in tip.downvotes.all():
        tip.downvotes.remove(request.user)  # Evita conflictos con downvotes
    if request.user not in tip.upvotes.all():
        tip.upvotes.add(request.user)
        tip.author.update_reputation()  # Actualiza reputación del autor
    return redirect('homepage')

@login_required
def downvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.user.can_downvote:
        if request.user in tip.upvotes.all():
            tip.upvotes.remove(request.user)  # Evita conflictos con upvotes
        if request.user not in tip.downvotes.all():
            tip.downvotes.add(request.user)
            tip.author.update_reputation()  # Actualiza reputación del autor
    else:
        raise PermissionDenied("No tienes permiso para downvote este tip.")
    return redirect('homepage')

@login_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)

    # Permitir eliminación si el usuario es el autor o tiene el permiso específico basado en reputación
    if request.user == tip.author or request.user.can_delete_tips:
        if request.method == 'POST':
            tip.delete()
            return redirect('homepage')
        return render(request, 'ex/confirm_delete.html', {'tip': tip})
    else:
        raise PermissionDenied("No tienes permiso para borrar este tip.")

