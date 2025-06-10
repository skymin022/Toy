from django.db import models
from django.contrib.auth.models import User

class Stat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    study = models.IntegerField(default=0)
    exercise = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
    appearance = models.IntegerField(default=0)
    wealth = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    achieved = models.BooleanField(default=False)
    date_achieved = models.DateTimeField(null=True, blank=True)
