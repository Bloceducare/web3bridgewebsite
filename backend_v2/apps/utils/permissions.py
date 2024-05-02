from rest_framework import permissions
import requests
from django.conf import settings
from .exceptions.requests import RequestException, JWTException


class IsAuthenticatedByAuthServer(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users
    whose credentials are validated by the authentication server.
    """

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if not token:
            raise JWTException("Authentication token not provided")

        try:
            # Verify token against authentication server
            response = requests.post(settings.AUTH_SERVER_URL + "/api/token/verify/", json={"token": token})
            
            if response.status_code != 200:
                raise RequestException("Error authenticating from auth server")

            response = response.json()
            user_data = response.get("user", {})

            # Check if the user has admin role
            if user_data.get("role") == "admin":
                return True
            else:
                return False

        except Exception as e:
            raise RequestException(str(e))