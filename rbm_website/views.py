from django.shortcuts import render, get_object_or_404
from rbm_website.apps.rbm.models import DBNModel

# Loads the home page with the required DBN
def home(request):
    dbn = get_object_or_404(DBNModel , pk=12)
    return render(request, 'home.html', {'dbn' : dbn})

# Loads the FAQ page
def faq(request):
    return render(request, 'faq.html', {})

# Loads the tutorial page
def tutorial(request):
    return render(request, 'tutorial.html', {})
