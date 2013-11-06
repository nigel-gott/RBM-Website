from django.db import models
from picklefield.fields import PickledObjectField

# Create your models here.
class RBMModel(models.Model):
    name = models.CharField(max_length=200)
    weights = PickledObjectField()
    visible = models.IntegerField()
    hidden = models.IntegerField()
    learning_rate = models.FloatField()
    
