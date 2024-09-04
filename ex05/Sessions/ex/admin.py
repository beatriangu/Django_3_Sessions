# ex/admin.py
from django.contrib import admin
from .models import AUser, Tip

admin.site.register(AUser)
admin.site.register(Tip)
