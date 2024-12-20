import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

from .wsgi import *
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application



os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'chat_app.settings'
)
django_asgi_app = get_asgi_application()
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    )
    }
)