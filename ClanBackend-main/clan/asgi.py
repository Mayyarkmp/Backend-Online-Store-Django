import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack,BaseMiddleware

from django.core.asgi import get_asgi_application
from .middlewares.channels import JWTAuthMiddleware
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from .wsgi import application as wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clan.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(dict(http=django_asgi_app, websocket=JWTAuthMiddleware(
    URLRouter(
        chat_websocket_urlpatterns,
    )
)))
