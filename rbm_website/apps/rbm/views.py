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
        description = forms.CharField(max_length=1000, widget=forms.Textarea)
        visible = forms.IntegerField()
        labels = forms.IntegerField()
        learning_rate = forms.FloatField()
        training_data = forms.CharField(max_length=2000)
        layer_count = forms.IntegerField(widget = forms.HiddenInput())

        def __init__(self, *args, **kwargs):
            layers = kwargs.pop('layer', 0)

            super(RBMForm, self).__init__(*args, **kwargs)
            self.fields['layer_count'].initial = layers

            for index in range(int(layers)):
                self.fields['layer_{index}'.format(index=index)] = forms.IntegerField()


def create(request):
    if request.method == 'POST':

        form = RBMForm(request.POST, layer=request.POST.get('layer_count'))

        if form.is_valid():
            visible = form.cleaned_data['visible']
            labels = form.cleaned_data['labels']
            learning_rate = form.cleaned_data['learning_rate']
            description = form.cleaned_data['description']
            name = form.cleaned_data['name']
            training_data = [map(int, x.split(',')) for x in form.cleaned_data['training_data'].split(';')]
            layer_count = form.cleaned_data['layer_count']

            # topology of the network
            # MOVE HTML JAVASCRIPT TO FILE
            # OPtimise errors and form input. Separate from form.as p
            # Incorporate with DBN
            # separate css and js from html
            # Maybe change visibles to image dimensions
            topology = []
            topology.append(visible)
            for index in range(layer_count):
                topology.append(form.cleaned_data['layer_{index}'.format(index=index)])
            topology.append(labels)

            rbm = RBMModel.build_rbm(name, description, visible, labels, learning_rate)
            rbm.train(training_data)
            rbm.save()
            return redirect('index')

    else:
        form = RBMForm()

    return render(request, 'rbm/create.html', { 'form' : form })

def regenerate(request, rbm_id):
    rbm = get_object_or_404(RBMModel , pk=rbm_id)
    data = [map(int, request.POST['data'].split(','))]
    (visible_state, hidden_state) = rbm.regenerate(data)
    visible_state = np.array_str(visible_state)
    hidden_state = np.array_str(hidden_state)
    return render(request, 'rbm/regenerate.html', {'old_data': request.POST['data'], 'rbm': rbm, 'visible_state': visible_state, 'hidden_state': hidden_state})

