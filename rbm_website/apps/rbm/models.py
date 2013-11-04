from django.db import models
from jsonfield import JSONField

# Create your models here.
class RBM(models.Model):
    name = models.CharField(max_length=200)
    matrix = JSONField()
    
