from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import AUser

class AUserCreationForm(UserCreationForm):
    class Meta:
        model = AUser
        fields = ['username', 'email']

class AUserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(AUserAuthenticationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Añade la clase CSS 'form-control' a todos los campos

