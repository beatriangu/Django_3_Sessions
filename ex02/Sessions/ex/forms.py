
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tip, AUser

class AUserCreationForm(UserCreationForm):
    class Meta:
        model = AUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(AUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['content']  # Only the 'content' field is visible in the form

    def __init__(self, *args, **kwargs):
        super(TipForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
