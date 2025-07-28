from django.db import models

# Create your models here.
from django.db import models

class Todo(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.TextField()
    status = models.BooleanField(default=False)
    seq = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)