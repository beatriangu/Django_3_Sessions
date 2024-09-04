from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
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
    tip.upvote(request.user)
    tip.save()
    return redirect('homepage')


@permission_required('ex.can_downvote_tip', raise_exception=True)
def downvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    if request.method == 'POST':
        tip.downvote(request.user)
        return redirect('homepage')



@login_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)

    # Permitir eliminación si el usuario es el autor o tiene el permiso específico
    if request.user == tip.author or request.user.has_perm('app_name.can_delete_tip'):
        if request.method == 'POST':
            tip.delete()
            return redirect('homepage')
    else:
        raise PermissionDenied("No tienes permiso para borrar este tip.")
    
    return redirect('homepage')
