# cookieapp/authenticate.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions

def enforce_csrf(request):
    # Create a CsrfViewMiddleware instance
    print("TTTTTTTTTTTTTTTT",reason)
    csrf_middleware = CsrfViewMiddleware(get_response=lambda request: None)
    csrf_middleware.process_request(request)
    reason = csrf_middleware.process_view(request, None, (), {})
    if reason:
        raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Skip authentication for specific paths
        if request.path in ['/request-otp/']:
            return None  # Skip authentication for this endpoint

        # Existing authentication logic
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)  # Enforce CSRF check
        return self.get_user(validated_token), validated_token
