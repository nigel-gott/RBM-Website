from django.db import models
from picklefield.fields import PickledObjectField

from rbm_website.libs.rbm_lib.rbm import RBM

# Create your models here.
class RBMModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    rbm = PickledObjectField()

    @staticmethod
    def build_rbm(name, description, visible, hidden, learning_rate):
        rbm = RBM(visible, hidden, learning_rate)
        return RBMModel(name=name, description=description, rbm=rbm)

    def train(self, training_data):
        self.rbm.train(training_data)

    def regenerate(self, data):
        return self.rbm.regenerate(data)

