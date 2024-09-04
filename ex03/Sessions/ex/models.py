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

    def upvote(self, user):
        # Cancel any downvote by this user
        if self.downvotes.filter(id=user.id).exists():
            self.downvotes.remove(user)
        # Add the upvote if not already upvoted
        if not self.upvotes.filter(id=user.id).exists():
            self.upvotes.add(user)

    def downvote(self, user):
        # Cancel any upvote by this user
        if self.upvotes.filter(id=user.id).exists():
            self.upvotes.remove(user)
        # Add the downvote if not already downvoted
        if not self.downvotes.filter(id=user.id).exists():
            self.downvotes.add(user)

    def cancel_vote(self, user):
        # Remove both upvotes and downvotes by this user
        self.upvotes.remove(user)
        self.downvotes.remove(user)

    def upvotes_count(self):
        return self.upvotes.count()

    def downvotes_count(self):
        return self.downvotes.count()
