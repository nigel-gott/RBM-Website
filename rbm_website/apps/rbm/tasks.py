from djcelery import celery
from django.conf import settings
from rbm_website.apps.rbm.models import DBNModel
from rbm_website.libs.image_lib import image_processor as imgpr
from rbm_website.libs.rbm_lib import dbn as dbnlib

@celery.task
def train_dbn(dbn):
    print dbn.id
    print dbn.height
    print dbn.width
    print dbn.labels

    DBN = dbn.dbn
    
    class_path = settings.MEDIA_ROOT + str(dbn.id)
    print class_path
    ( images, labels ) = imgpr.retrieve_image_class(class_path, dbn.height, dbn.width)
    print images
    print labels
