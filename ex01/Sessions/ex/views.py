from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import AUserCreationForm, AUserAuthenticationForm

def homepage(request):
    # Render the home page template with the username
    return render(request, 'ex/homepage.html')

def register(request):
    if request.method == 'POST':
        form = AUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Crea el nuevo usuario
            login(request, user)  # Inicia sesión automáticamente
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('login')  # Redirige a la página de inicio de sesión
        else:
            # Agrega un mensaje de error solo si hay errores en el formulario
            messages.error(request, "Please correct the errors below.")
    else:
        form = AUserCreationForm()
    
    return render(request, 'ex/register.html', {'form': form})
    
def user_login(request):
    if request.method == 'POST':
        form = AUserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            print("User logged in successfully")  # Añadir para depurar
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AUserAuthenticationForm()
    return render(request, 'ex/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('homepage')
