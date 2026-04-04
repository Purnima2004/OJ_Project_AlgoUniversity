from django.shortcuts import redirect
from functools import wraps


def redirect_if_authenticated(view_func):
    """
    Decorator to redirect authenticated users to home page.
    Used for login and register views.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
