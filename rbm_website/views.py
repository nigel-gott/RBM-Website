from django.shortcuts import render, get_object_or_404
from rbm_website.apps.rbm.models import DBNModel

def home(request):
    dbn = get_object_or_404(DBNModel , pk=12)
    return render(request, 'home.html', {'dbn' : dbn})

def faq(request):
    return render(request, 'faq.html', {})

def terms(request):
    return render(request, 'terms.html', {})

def privacy(request):
    return render(request, 'privacy.html', {})

def tutorial(request):
    return render(request, 'tutorial.html', {})
