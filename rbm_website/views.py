from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

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
        return render(request, 'admin.html', {})
