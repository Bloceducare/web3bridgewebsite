from rest_framework import HTTP_HEADER_ENCODING, authentication
import requests
from django.conf import settings
from ..exceptions.requests import JWTException, RequestException

class JWTAuthenticationByAuthServer(authentication.BaseAuthentication):
    www_authenticate_realm = "api"
    media_type = "application/json"
    AUTH_HEADER_TYPES = ["Bearer", "bearer"]
    AUTH_HEADER_TYPE_BYTES = { h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES}
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            raise JWTException("Authentication credentials were not provided")
        
        raw_token = self.get_raw_token(header)
        try:
            # Verify token against authentication server
            response = requests.post(settings.AUTH_SERVER_URL + "/api/token/verify/", headers={'Authorization': raw_token.decode(HTTP_HEADER_ENCODING)})
            if response.status_code != 200:
                raise RequestException("Error authenticating from auth server")

            user_data = response.json()
            return user_data, str(raw_token)

        except Exception as e:
            raise RequestException(str(e))

    def get_header(self, request):
        header = request.META.get("HTTP_AUTHORIZATION")

        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) == 0:
            raise JWTException("Authentication credentials were not provided")

        if parts[0] not in self.AUTH_HEADER_TYPE_BYTES:
            raise JWTException("Authentication credentials missing bearer")

        if len(parts) != 2:
            raise JWTException("Authorization header must contain two space-delimited values")

        return parts[1]