from functools import wraps
from urllib.parse import urlparse
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url
from django.contrib import messages


def user_passes_test(test_func, message='Please, login to observe this page'):
	"""
	Decorator for views that checks that the user passes the given test,
	redirecting to the log-in page if necessary. The test should be a callable
	that takes the user object and returns True if the user passes.
	"""
	def decorator(view_func):
		@wraps(view_func)
		def _wrapped_view(request, *args, **kwargs):
			if not test_func(request.user):
				messages.warning(request, message)
			return view_func(request, *args, **kwargs)

		return _wrapped_view
	return decorator


def login_required_message(function=None, message='Please, login to observe this page'):
	"""
	Decorator for views that checks that the user is logged in, redirecting
	to the log-in page if necessary.
	"""
	actual_decorator = user_passes_test(
		lambda u: u.is_authenticated,
		message=message
	)
	if function:
		return actual_decorator(function)
	return actual_decorator


def special_user(fn):
	def wrapper(request, *args, **kwargs):
		if request.user.is_superuser or request.user.is_staff:
			return fn(request)
		else:
			messages.warning(request, 'You cannot view this page!')
			# don't forget to add messages to the template\
			return redirect('start-page')
	wrapper.__doc__ = fn.__doc__
	wrapper.__name__ = fn.__name__

	return wrapper
