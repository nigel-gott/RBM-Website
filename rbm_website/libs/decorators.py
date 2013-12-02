from django.utils.functional import wraps
from django.utils.decorators import available_attrs
from django.contrib import messages

login_message = "You must be logged in to access this content!"

def message_user_test(test_function, message):
    def decorator(view_func):
        @wraps(view_func, assigned = available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not test_function(request.user):
                messages.add_message(request, messages.ERROR, message)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def message_login_required(function=None, message=login_message):
    actual_decorator = message_user_test(
        lambda u: u.is_authenticated(),
        message=message,)
    if function:
        return actual_decorator(function)
    return actual_decorator