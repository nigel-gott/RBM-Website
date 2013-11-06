# Create your views here.
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView

from rbm_website.libs.rbm_lib.rbm import RBM 
from rbm_website.apps.rbm.models import RBMModel

class RBMListView(ListView):
    model = RBMModel

class RBMDetailView(DetailView):
    model = RBMModel

def create(request):
    training_data = request.POST['weights']
    training_array = [map(int, x.split(',')) for x in training_data.split(';')]

    visible = int(request.POST['visible'])
    hidden = int(request.POST['hidden'])
    learning_rate = float(request.POST['learning_rate'])
    trainer = RBM(visible, hidden, learning_rate)
    trainer.train(training_array)
    weights = trainer.weights.tolist() 

    new_rbm = RBMModel(name=request.POST['name'], weights=weights, visible=visible, hidden=hidden, learning_rate=learning_rate)
    new_rbm.save()
    return redirect('index')

def regenerate(request, rbm_id):
    stored_rbm = get_object_or_404(RBMModel , pk=rbm_id)
    trainer = RBM(stored_rbm.visible, stored_rbm.hidden, stored_rbm.learning_rate)
    trainer.weights = np.array([map(int, x) for x in stored_rbm.weights])
    data = [map(int, request.POST['data'].split(','))]
    (visible_state, hidden_state) = trainer.regenerate(data)
    visible_state = np.array_str(visible_state)
    hidden_state = np.array_str(hidden_state)
    return render(request, 'rbm/regenerate.html', {'old_data': request.POST['data'], 'rbm': stored_rbm, 'visible_state': visible_state, 'hidden_state': hidden_state})

