from django.db import models
from picklefield.fields import PickledObjectField

from rbm_website.libs.rbm_lib.dbn import DBN

# Create your models here.
class DBNModel(models.Model):
    name = models.CharField(max_length=200)
    creator = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    dbn = PickledObjectField()

    @staticmethod
    def build_dbn(name, creator, description, config, labels, learning_rate):
        dbn = DBN(config, labels, learning_rate)
        return DBNModel(name=name, creator=creator, description=description, dbn=dbn)

    #def train(self, training_data):
    #    self.dbn.train(training_data)

    #def regenerate(self, data):
    #    return self.dbn.regenerate(data)

