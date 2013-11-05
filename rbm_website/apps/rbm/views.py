# Create your views here.
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from rbm_website.libs.rbm import rbm
from rbm_website.apps.rbm.models import RBM 

def index(request):
    rbm_list = RBM.objects.all()
    return render(request, 'rbm/index.html', {'rbm_list': rbm_list})

def create(request):
    training_data = request.POST['matrix']
    training_array = [map(int, x.split(',')) for x in training_data.split(';')]

    trainer = rbm.RBM(
            int(request.POST['visible']), 
            int(request.POST['hidden']), 
            float(request.POST['learning_rate']),
            )
    trainer.train(training_array)
    matrix = list(np.array(trainer.weights).reshape(-1,))

    new_rbm = RBM(name=request.POST['name'], matrix=matrix)
    new_rbm.save()
    return redirect('index')

def view(request, rbm_id):
    stored_rbm = get_object_or_404(RBM , pk=rbm_id)
    matrix = str(stored_rbm.matrix)
    return render(request, 'rbm/view.html', {'name': stored_rbm.name, 'matrix': matrix})

