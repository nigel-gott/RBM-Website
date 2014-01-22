import pickle
import rbm_website.libs.rbm_lib.rbm as rbm 
import rbm_website.libs.rbm_lib.dbn as dbn 
import rbm_website.settings
import sys, os
import shutil

if __name__ == '__main__':
    os.environ["DJANGO_SETTINGS_MODULE"] = "rbm_website.settings"
    sys.path.append("rbm_website/")
    from rbm_website.apps.rbm.models import DBNModel
    sys.modules["rbm"] = rbm 
    sys.modules["dbn"] = dbn 
    dbn_file = open("dbn.pob", "rb")
    dbn = pickle.load(dbn_file)
    model = DBNModel()

    dbn.number_inputs = 784

    model.name = "Handwritten Digits DBN"
    model.dbn = dbn
    model.creator_id = 1
    model.description = "Handwritten Digits DBN, please google the MNIST handwritten digits database and look at the pictures to see in what style the digits have been written. Also please make sure you centre your digits as the MNIST training set is also centred. "
    model.trained = True
    model.height = 28
    model.width = 28
    model.labels = 10
    model.private = False
    model.training = False
    model.label_values = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    model.save()

    shutil.copytree('rbm_website/example_handwritten_base_images/', 'rbm_website/media/' + str(model.id))

