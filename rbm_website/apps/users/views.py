from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import logout

# Create your views here.
def view_user(request, username):
    return render(request, 'users/view_user.html', {'username':username})

def user_logout(request):
    messages.add_message(request, messages.INFO, 'Successfully logged out!')
    return logout(request, next_page = 'home')

