from django.db import models
from django.contrib.auth.models import AbstractUser

class AUser(AbstractUser):
    pass

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(AUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(AUser, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(AUser, related_name='downvoted_tips', blank=True)

    class Meta:
        permissions = [
            ("can_delete_tip", "Can delete tip"),
        ]

    def upvote(self, user):
        if self.downvotes.filter(id=user.id).exists():
            self.downvotes.remove(user)
        if not self.upvotes.filter(id=user.id).exists():
            self.upvotes.add(user)

    def downvote(self, user):
        if self.upvotes.filter(id=user.id).exists():
            self.upvotes.remove(user)
        if not self.downvotes.filter(id=user.id).exists():
            self.downvotes.add(user)

    def upvotes_count(self):
        return self.upvotes.count()

    def downvotes_count(self):
        return self.downvotes.count()

