from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class AUser(AbstractUser):
    reputation = models.IntegerField(default=0)  # Campo para la reputación

    def update_reputation(self):
        # Recalcula la reputación basada en los votos de los tips del usuario
        upvotes = sum(tip.upvotes.count() for tip in self.tips.all())
        downvotes = sum(tip.downvotes.count() for tip in self.tips.all())
        self.reputation = upvotes * 5 - downvotes * 2
        self.save()

    @property
    def can_downvote(self):
        return self.reputation >= 15

    @property
    def can_delete_tips(self):
        return self.reputation >= 30

    def __str__(self):
        return f"{self.username} ({self.reputation} rep)"



class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tips')
    date_created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    class Meta:
        permissions = [
            ("can_delete_tip", "Can delete tip"),
            ("can_downvote_tip", "Can downvote a tip"),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.author.update_reputation()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.author.update_reputation()

    def upvote(self, user):
        if self.downvotes.filter(id=user.id).exists():
            self.downvotes.remove(user)
        if not self.upvotes.filter(id=user.id).exists():
            self.upvotes.add(user)
            self.author.update_reputation()

    def downvote(self, user):
        if self.upvotes.filter(id=user.id).exists():
            self.upvotes.remove(user)
        if not self.downvotes.filter(id=user.id).exists():
            self.downvotes.add(user)
            self.author.update_reputation()

    def upvotes_count(self):
        return self.upvotes.count()

    def downvotes_count(self):
        return self.downvotes.count()