from django.db import models
from django.contrib.auth.models import AbstractUser

class AUser(AbstractUser):
    pass

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(AUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]  # Display the first 50 characters of the tip
