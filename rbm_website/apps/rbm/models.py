from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

from rbm_website.libs.rbm_lib.dbn import DBN

# Create your models here.
class DBNModel(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='dbns')
    created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    height = models.IntegerField(max_length=10)
    width = models.IntegerField(max_length=10)
    labels = models.IntegerField(max_length=10)
    private = models.BooleanField()
    training = models.BooleanField()
    trained = models.BooleanField()
    dbn = PickledObjectField()
    label_values = PickledObjectField()

    def __unicode__(self):
        return (self.name + " - " + self.creator.username)

    def get_topology(self):
        return self.dbn.get_topology()

    def classify_image(self, image_data, samples):
        return self.dbn.classify(image_data, samples)

    @staticmethod
    def build_dbn(name, creator, description, height, width, config, labels, private, learning_rate):
        dbn = DBN(config, labels, learning_rate)
        return DBNModel(name=name, creator=creator, description=description, height=height,
            width=width, labels=labels, private=private, training=False, trained=False, dbn=dbn)