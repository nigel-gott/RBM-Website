import os
import numpy as np
from djcelery import celery
from django.conf import settings
from rbm_website.apps.rbm.models import DBNModel
from rbm_website.libs.image_lib import image_processor as imgpr
from rbm_website.libs.image_lib import noise
from rbm_website.libs.rbm_lib import dbn as dbnlib

# ADD CHECKING AND ERROR OUTPUTTING AFTER TRAINING

@celery.task
def train_dbn(dbn, label_list):
    print "Processing and training DBN: " + str(dbn.name) + "..."
    print "Saving label_values..."
    dbn.label_values = label_list
    dbn.save()
    print dbn.label_values
    print "Creating directories..."
    class_path = settings.MEDIA_ROOT + str(dbn.id)
    base_path = class_path + '/base_images'
    train_path = class_path + '/training'
    test_path = class_path + '/testing'
    os.makedirs(train_path)
    os.makedirs(test_path)

    print "Creating noisy images..."
    noise.create_noisy_images(base_path, train_path, 1000)
    noise.create_noisy_images(base_path, test_path, 200)

    print "Retrieving and formatting images..."
    (train_images, train_labels) = retrieve_images(train_path, dbn.height, dbn.width, label_list)
    (test_images, test_labels) = retrieve_images(test_path, dbn.height, dbn.width, label_list)

    print "Training DBN..."
    #training_method(dbn.dbn, train_images, train_labels, test_images, test_labels)
    training_method(dbn.dbn, train_images, train_labels, test_images, test_labels, 1, 50, 1, 50, 1, 1)

    print"---------------------------------------------------------------"
    print"---------FINISHED--------------------TRAINING------------------"
    print"---------------------------------------------------------------"

def training_method(dbn, train_img, train_lbl, test_img, test_lbl, pre_epoch=5,
    pre_batch=50, train_epoch = 50, train_batch = 50, train_loop=20, samples=1 ):
    dbn.pre_train(train_img, pre_epoch, pre_batch)
    for i in xrange(0, train_loop):
        dbn.train_labels(train_img, train_lbl, train_epoch, train_batch)
        test_class = dbn.classify(test_img, samples)
        print 'Iteration {0}: Error over test data: {1}'.format(i, 1 - (test_class*test_lbl).mean() * 10)

def retrieve_images(path, height, width, label_list):
    (images, labels) = imgpr.retrieve_all_images(path, height, width)
    trim_labels(labels)
    np_labels = convert_labels(labels, label_list)
    np_images = np.array(images)
    return (np_images, np_labels)

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


