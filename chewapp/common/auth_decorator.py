from functools import wraps
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from ..models import Account


def with_auth(*, manager=False, administrator=False, owner=False, staff=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # Extract the request
            req = [r for r in args if isinstance(r, WSGIRequest)][0]

            # Check if the user is logged in
            if req.user is None or req.user.is_anonymous:
                return redirect("/login")

            # Get the Account object
            account = Account.objects.get(user=req.user)

            # Check if the user has the right permissions
            profile = account.profile
            if (
                (manager and not profile.is_manager)
                or (administrator and not profile.is_administrator)
                or (owner and not profile.is_owner)
                or (staff and not profile.is_staff)
            ):
                return redirect("/login")

            # Continue to the function
            return function(*args, **kwargs)

        return wrapper

    return decorator
