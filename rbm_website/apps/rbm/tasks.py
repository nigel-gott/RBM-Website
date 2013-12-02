import os
import numpy as np
from djcelery import celery
from django.conf import settings
from rbm_website.apps.rbm.models import DBNModel
from rbm_website.libs.image_lib import image_processor as imgpr
from rbm_website.libs.image_lib import noise
from rbm_website.libs.rbm_lib import dbn as dbnlib

@celery.task
def train_dbn(dbn, label_list):
    DBN = dbn.dbn

    class_path = settings.MEDIA_ROOT + str(dbn.id)
    base_path = class_path + '/base_images'
    result_path = class_path + '/results'
    os.makedirs(result_path)

    noise.create_noisy_images(base_path, result_path, 20)

    (images, labels) = imgpr.retrieve_all_images(result_path, dbn.height, dbn.width)
    trim_labels(labels)
    np_labels = convert_labels(labels, label_list)
    np_images = np.array(images)

def trim_labels(labels):
    for index, item in enumerate(labels):
        item = item.split(".")[0]
        labels[index] = item

def convert_labels(labels, label_list):
    np_labels = np.zeros((len(labels), (len(label_list))))
    for index, item in enumerate(labels):
        i = label_list.index(item)
        label_data = np.zeros(len(label_list))
        label_data[i] = 1
        np_labels[index] = label_data
    return np_labels


