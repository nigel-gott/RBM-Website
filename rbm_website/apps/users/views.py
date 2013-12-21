from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import logout
from django.contrib.auth.models import User

# Create your views here.
def view_user(request, username):
    user = User.objects.get(username=username)
    # CHECK FOR NO USER
    return render(request, 'users/view_user.html', {'user': user})

def user_logout(request):
    messages.add_message(request, messages.INFO, 'Successfully logged out!')
    return logout(request, next_page = 'home')

