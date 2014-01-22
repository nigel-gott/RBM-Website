from django.shortcuts import render, get_object_or_404
from rbm_website.apps.rbm.models import DBNModel#
from django.conf import settings

# Loads the home page with the required DBN
def home(request):
    dbnSet = DBNModel.objects.filter(id=settings.HOME_DBN)
    has_dbn = True
    dbn = None
    if dbnSet.count() == 0:
        dbnAll = DBNModel.objects.filter(private=False, trained=True)
        if dbnAll.count() == 0:
            has_dbn = False
        else:
            dbn = dbnAll[0]
    else:
        dbn = dbnSet[0]
    return render(request, 'home.html', {'dbn' : dbn, 'has_dbn': has_dbn})

# Loads the FAQ page
def faq(request):
    return render(request, 'faq.html', {})

# Loads the tutorial page
def tutorial(request):
    return render(request, 'tutorial.html', {})
