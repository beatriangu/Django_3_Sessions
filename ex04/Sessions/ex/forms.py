
from .models import Tip, AUser
from django import forms
from django.contrib.auth.forms import UserCreationForm


class AUserCreationForm(UserCreationForm):
    class Meta:
        model = AUser
        fields = ('username', 'email', 'password1', 'password2')

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']  
