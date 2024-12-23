# App/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

class SessionExpirationMiddleware:
    """
    Middleware que detecta cuando la sesión ha expirado y redirige a la página principal.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Si la sesión ha expirado, redirige a la página principal
        if not request.user.is_authenticated:
            if 'sessionid' not in request.COOKIES:  # Verifica si la cookie de sesión está presente
                return redirect('index') # redirije al index
        
        response = self.get_response(request)
        return response