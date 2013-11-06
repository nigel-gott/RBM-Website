# Create your views here.
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView

from rbm_website.libs.rbm import rbm
from rbm_website.apps.rbm.models import RBM 

class RBMList(ListView):
    model = RBM

def create(request):
    training_data = request.POST['matrix']
    training_array = [map(int, x.split(',')) for x in training_data.split(';')]

    visible = int(request.POST['visible'])
    hidden = int(request.POST['hidden'])
    learning_rate = float(request.POST['learning_rate'])
    trainer = rbm.RBM(visible, hidden, learning_rate)
    trainer.train(training_array)
    matrix = trainer.weights.tolist() 

    new_rbm = RBM(name=request.POST['name'], matrix=matrix, visible=visible, hidden=hidden, learning_rate=learning_rate)
    new_rbm.save()
    return redirect('index')

def view(request, rbm_id):
    stored_rbm = get_object_or_404(RBM , pk=rbm_id)
    matrix = str(stored_rbm.matrix)
    return render(request, 'rbm/view.html', {'rbm': stored_rbm, 'matrix': matrix})

def regenerate(request, rbm_id):
    stored_rbm = get_object_or_404(RBM , pk=rbm_id)
    trainer = rbm.RBM(stored_rbm.visible, stored_rbm.hidden, stored_rbm.learning_rate)
    trainer.weights = np.array([map(int, x) for x in stored_rbm.matrix])
    data = [map(int, request.POST['data'].split(','))]
    (visible_state, hidden_state) = trainer.regenerate(data)
    visible_state = np.array_str(visible_state)
    hidden_state = np.array_str(hidden_state)
    return render(request, 'rbm/regenerate.html', {'old_data': request.POST['data'], 'rbm': stored_rbm, 'visible_state': visible_state, 'hidden_state': hidden_state})

