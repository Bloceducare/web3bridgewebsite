from rest_framework import permissions
import requests
from django.conf import settings

class IsAuthenticatedByAuthServer(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users
    whose credentials are validated by the authentication server.
    """

    def has_permission(self, request, view):
        token = request.headers.get('Authorization')

        if not token:
            return False

        try:
            # Verify token against authentication server
            response = requests.post(settings.AUTH_SERVER_URL + "/api/token/verify/", headers={'Authorization': token})
            if response.status_code != 200:
                return False

            user_data = response.json()
            # Check if the user has permission (e.g., is_admin)
            is_admin = user_data.get('is_admin', False)

            # Customize permission logic based on your requirements
            # For example, you might want to allow access only to admin users:
            return is_admin

        except Exception as e:
            return False
