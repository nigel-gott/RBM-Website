from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.contrib import messages

# Adding extra functonality to the decoraters used by Django

# Message to display
login_message = "You must be logged in to access this content!"

# Checks to make sure a user passes a test, if not outputs a message
def message_user_test(test_function, message):
    def decorator(view_func):
        @wraps(view_func, assigned = available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not test_function(request.user):
                messages.add_message(request, messages.ERROR, message)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Checks to make sure a user is logged in, or returns a message
def message_login_required(function=None, message=login_message):
    actual_decorator = message_user_test(
        lambda u: u.is_authenticated(),
        message=message,)
    if function:
        return actual_decorator(function)
    return actual_decorator