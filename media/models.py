from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Media(models.Model):
  description = models.CharField(max_length=100)
  image = models.ImageField(upload_to='image')
  created = models.DateTimeField(auto_now_add = True)