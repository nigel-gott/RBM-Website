from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
from rbm_website.libs.rbm_lib.dbn import DBN

# The DBN model object
# Contains the name and other key details
# Contains a pickled object of the dbn
# Contains the list of labels
# Provides some methods for manipulation
class DBNModel(models.Model):
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, related_name='dbns')
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    height = models.IntegerField(max_length=10)
    width = models.IntegerField(max_length=10)
    labels = models.IntegerField(max_length=10)
    private = models.BooleanField()
    training = models.BooleanField()
    trained = models.BooleanField()
    dbn = PickledObjectField()
    label_values = PickledObjectField()

    # The string representation of the DBN
    def __unicode__(self):
        return (self.name + " - " + self.creator.username)

    # Gets the DBN topology
    def get_topology(self):
        return self.dbn.get_topology()

    # Classifies an image using the DBN
    def classify_image(self, image_data, samples):
        return self.dbn.classify(image_data, samples)

    # Creates a DBN with given parameters
    @staticmethod
    def build_dbn(name, creator, description, height, width, config, labels, private, learning_rate):
        dbn = DBN(config, labels, learning_rate)
        return DBNModel(name=name, creator=creator, description=description, height=height,
            width=width, labels=labels, private=private, training=False, trained=False, dbn=dbn)