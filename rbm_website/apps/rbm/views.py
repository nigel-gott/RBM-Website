# Create your views here.
import numpy as np
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView

from django import forms

from rbm_website.apps.rbm.models import RBMModel

class RBMListView(ListView):
    model = RBMModel

class RBMDetailView(DetailView):
    model = RBMModel


class RBMForm(forms.Form):
        name =  forms.CharField(max_length=200)
        visible = forms.IntegerField()
        hidden = forms.IntegerField()
        learning_rate = forms.FloatField()
        training_data = forms.CharField(max_length=2000)


def create(request):
    error = False 
    if request.method == 'POST':
        form = RBMForm(request.POST, request.FILES)

        if form.is_valid():
            visible = form.cleaned_data['visible']
            hidden = form.cleaned_data['hidden']
            learning_rate = form.cleaned_data['learning_rate']
            name = form.cleaned_data['name']
            training_data = [map(int, x.split(',')) for x in form.cleaned_data['training_data'].split(';')] 

            rbm = RBMModel.build_rbm(name, visible, hidden, learning_rate)
            rbm.train(training_data)
            rbm.save()
            return redirect('index')
        else: 
            error = True 

    form = RBMForm()
    return render(request, 'rbm/create.html', { 'form' : form , 'error' : error })

def regenerate(request, rbm_id):
    rbm = get_object_or_404(RBMModel , pk=rbm_id)
    data = [map(int, request.POST['data'].split(','))]
    (visible_state, hidden_state) = rbm.regenerate(data)
    visible_state = np.array_str(visible_state)
    hidden_state = np.array_str(hidden_state)
    return render(request, 'rbm/regenerate.html', {'old_data': request.POST['data'], 'rbm': rbm, 'visible_state': visible_state, 'hidden_state': hidden_state})

