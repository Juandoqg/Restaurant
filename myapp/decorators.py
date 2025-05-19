# decorators.py
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        if not request.user.is_waiter and not request.user.is_chef:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied  # 403 si no es admin
    return _wrapped_view

def waiter_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        if request.user.is_waiter:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view

def chef_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('signin')
        if request.user.is_chef:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return _wrapped_view
