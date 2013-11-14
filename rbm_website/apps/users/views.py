from django.shortcuts import render

# Create your views here.
def view_user(request, username):
    return render(request, 'users/view_user.html', {'username':username})

