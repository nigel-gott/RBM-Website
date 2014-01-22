from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.views import logout
from django.contrib.auth.models import User

# The views for the user objects

# The view to a users profile
# Loads the profile and the DBNs and renders the page
def view_user(request, username):
    prof_user = User.objects.get(username=username)
    public_dbns = prof_user.dbns.filter(private=False)
    private_dbns = prof_user.dbns.filter(private=True)
    return render(request, 'users/view_user.html', {'prof_user': prof_user,
        'public_dbns': public_dbns, 'private_dbns':private_dbns})

# Logs the user out with a message
def user_logout(request):
    messages.add_message(request, messages.INFO, 'Successfully logged out!')
    return logout(request, next_page = 'home')

