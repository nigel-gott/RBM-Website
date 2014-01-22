import os
import shutil
import numpy as np
from djcelery import celery
from django.conf import settings
from rbm_website.libs.image_lib import image_processor as imgpr
from rbm_website.libs.image_lib import noise

# The celery task used to train the DBN
# dbn - The DBN object
# label_list - The list of labels used in training
# pre_epoch - The epochs for pre training
# train_epoch - The epochs for label training
# train_loop - The number of loops to execute training
@celery.task
def train_dbn(dbn, label_list, pre_epoch, train_epoch, train_loop):
    print "Processing and training DBN: " + str(dbn.name) + "..."

    # Stored the label values in the DBN
    print "Saving label_values..."
    dbn.label_values = label_list
    dbn.training = True
    dbn.save()
    print dbn.label_values

    # Creates all the required directories
    print "Creating directories..."
    class_path = settings.MEDIA_ROOT + str(dbn.id)
    base_path = class_path + '/base_images'
    train_path = class_path + '/training'
    test_path = class_path + '/testing'
    os.makedirs(train_path)
    os.makedirs(test_path)

    # Creates the noisy images for training
    print "Creating noisy images..."
    noise.create_noisy_images(base_path, train_path, 1000)
    noise.create_noisy_images(base_path, test_path, 200)

    # Retrieves all the images, randomises them and formats them
    print "Retrieving and formatting images..."
    train_tuples  = zip(*retrieve_images(train_path, dbn.height, dbn.width, label_list))
    (test_images, test_labels) = retrieve_images(test_path, dbn.height, dbn.width, label_list)
    train_tuples = np.random.permutation(train_tuples)
    (train_images, train_labels) = zip(*train_tuples)

    # Trains the DBN
    print "Training DBN..."
    training_method(dbn.dbn, train_images, train_labels, test_images, test_labels, pre_epoch, 50, train_epoch, 50, train_loop, 1)

    # Updates the status of the DBN in training
    print "Updating DBN status..."
    dbn.training = False
    dbn.trained = True
    dbn.save()

    # Cleans up all the files used by training
    print "Cleaning up files..."
    shutil.rmtree(train_path)
    shutil.rmtree(test_path)

    # Success message
    print"---------------------------------------------------------------"
    print"------------FINISHED--------------------TRAINING---------------"
    print"---------------------------------------------------------------"

# The training method to be used for DBN training
def training_method(dbn, train_img, train_lbl, test_img, test_lbl, pre_epoch=5,
    pre_batch=50, train_epoch = 50, train_batch = 50, train_loop=20, samples=1 ):
    dbn.pre_train(train_img, pre_epoch, pre_batch)
    for i in xrange(0, train_loop):
        dbn.train_labels(train_img, train_lbl, train_epoch, train_batch)
        test_class = dbn.classify(test_img, samples)
        print 'Iteration {0}: Error over test data: {1}'.format(i, 1 - (test_class*test_lbl).mean() * dbn.number_labels)

# Retreives the images from a given directory
# Returns them as a tuple of Numpy array of images and labels
def retrieve_images(path, height, width, label_list):
    (images, labels) = imgpr.retrieve_all_images(path, height, width)
    trim_labels(labels)
    np_labels = convert_labels(labels, label_list)
    np_images = np.array(images)
    return (np_images, np_labels)

# Trims the white space off the labels
def trim_labels(labels):
    for index, item in enumerate(labels):
        item = item.split(".")[0]
        labels[index] = item

# Converts the labels into an appropriate format
# Of Numpy arrays with a 1 in the correct index and 0 otherwise
def convert_labels(labels, label_list):
    np_labels = np.zeros((len(labels), (len(label_list))))
    for index, item in enumerate(labels):
        i = label_list.index(item)
        label_data = np.zeros(len(label_list))
        label_data[i] = 1
        np_labels[index] = label_data
    return np_labels


