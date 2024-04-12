from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from django.urls import resolve
from ..helpers.requests import Utils as requestUtils
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from ..exceptions.requests import JWTException, RequestException

class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            resolver_match = resolve(request.path_info)
            kwargs = resolver_match.kwargs
            pk = kwargs.get('pk')
            return requestUtils.error_response(f"object {pk} does not exist", str(exception), http_status=status.HTTP_400_BAD_REQUEST)
        if isinstance(exception, JWTException):
            return requestUtils.error_response(f"Authentication failed", str(exception), http_status=status.HTTP_400_BAD_REQUEST)
        if isinstance(exception, RequestException):
            return requestUtils.error_response(f"Request failed", str(exception), http_status=status.HTTP_400_BAD_REQUEST)
        return None