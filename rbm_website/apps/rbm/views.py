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
    new_rbm = RBM(name=request.POST['name'], matrix=request.POST['matrix'])
    new_rbm.save()
    return redirect('index')

def view(request, rbm_id):
    stored_rbm = get_object_or_404(RBM , pk=rbm_id)
    return render(request, 'rbm/view.html', {'rbm': stored_rbm})

