# Create your views here.
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView

from rbm_website.apps.rbm.models import RBMModel

class RBMListView(ListView):
    model = RBMModel

class RBMDetailView(DetailView):
    model = RBMModel

def create(request):
    training_data_string = request.POST['weights']
    # training_data_string is a list of comma seperated values seperated by 
    # semi-colons.
    training_data = [map(int, x.split(',')) for x in training_data_string.split(';')]

    visible = int(request.POST['visible'])
    hidden = int(request.POST['hidden'])
    learning_rate = float(request.POST['learning_rate'])

    rbm = RBMModel.build_rbm(request.POST['name'], visible, hidden, learning_rate)
    rbm.train(training_data)
    rbm.save()
    return redirect('index')

def regenerate(request, rbm_id):
    rbm = get_object_or_404(RBMModel , pk=rbm_id)
    data = [map(int, request.POST['data'].split(','))]
    (visible_state, hidden_state) = rbm.regenerate(data)
    visible_state = np.array_str(visible_state)
    hidden_state = np.array_str(hidden_state)
    return render(request, 'rbm/regenerate.html', {'old_data': request.POST['data'], 'rbm': rbm, 'visible_state': visible_state, 'hidden_state': hidden_state})

