from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    last_logout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class PollChoice(models.Model):
    choice_title = models.TextField()
    votes = models.IntegerField(default=0)
    users_who_voted = models.ManyToManyField(CustomUser, related_name='selected_choices')
    poll_creation_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Poll(models.Model):
    title = models.CharField(max_length=100)
    options = models.ManyToManyField(PollChoice)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title
