from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from rbm_website.apps.rbm.models import DBNModel
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def admin(request):
    if (not (request.user.username == 'admin')):
        messages.add_message(request, messages.ERROR,
            "You must have administrator priveliges to access this page!")
        return redirect('home')
    else:
        users = User.objects.values('username', 'email' , 'is_superuser', 'last_login', 'date_joined')
        dbns = DBNModel.objects.values('name', 'creator', 'created', 'private', 'training', 'trained')
        for d in dbns:
            name = User.objects.get(id=d['creator'])
            d['creator'] = name
        return render(request, 'admin.html', {'users': users, 'dbns': dbns})
