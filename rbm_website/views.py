from django.shortcuts import render, get_object_or_404
from rbm_website.apps.rbm.models import DBNModel#
from django.conf import settings

# Loads the home page with the required DBN
def home(request):
    dbnset = DBNModel.objects.filter(id=settings.HOME_DBN)
    if dbnset.count() == 0:
        dbn = DBNModel.objects.all()[0]
    else:
        dbn = dbnset[0]
    return render(request, 'home.html', {'dbn' : dbn})

# Loads the FAQ page
def faq(request):
    return render(request, 'faq.html', {})

# Loads the tutorial page
def tutorial(request):
    return render(request, 'tutorial.html', {})
