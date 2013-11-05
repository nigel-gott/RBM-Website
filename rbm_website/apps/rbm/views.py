# Create your views here.
import numpy as np
from django.http import HttpResponse
from rbm_website.libs.rbm import rbm

def index(request):
    m = rbm.RBM(6,4)
    data = [[0,0,0,1,1,1],[1,1,1,0,0,0],[0,0,0,1,1,1]]
    m.train(data)
    (v, h) = m.regenerate([[0,0,0,1,1,1]])
    return HttpResponse("It is working: " + np.array_str(v) + " - " + np.array_str(h))

