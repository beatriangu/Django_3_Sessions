from django.contrib import admin
from .models import AUser, Tip

@admin.register(AUser)
class AUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'reputation')
    # Puedes añadir más configuraciones aquí según sea necesario

@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'date_created', 'upvotes_count', 'downvotes_count')
    # Puedes añadir más configuraciones aquí según sea necesario

