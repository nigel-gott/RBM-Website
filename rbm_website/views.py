from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def terms(request):
    return render(request, 'terms.html', {})

def privacy(request):
    return render(request, 'privacy.html', {})
