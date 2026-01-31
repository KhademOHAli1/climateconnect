from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication
from channels.sessions import CookieMiddleware
from rest_framework.exceptions import AuthenticationFailed
import logging

logger = logging.getLogger(__name__)


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 4.x (ASGI 3)
    
    This middleware authenticates users via Knox tokens stored in cookies.
    Updated for async support in Channels 4.x.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # Get cookies from scope
        cookies = dict(scope.get("cookies", {}))
        
        if "token" in cookies:
            scope["user"] = await self._authenticate_token(cookies["token"])
        else:
            scope["user"] = AnonymousUser()
        
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def _authenticate_token(self, token_string):
        """Authenticate user from Knox token - wrapped for async safety."""
        try:
            knox_auth = TokenAuthentication()
            user, auth_token = knox_auth.authenticate_credentials(
                token_string.encode("utf-8")
            )
            return user
        except AuthenticationFailed:
            logger.error("authentication failed!")
            return AnonymousUser()
        except Exception as e:
            logger.error(f"Token authentication error: {e}")
            return AnonymousUser()


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(TokenAuthMiddleware(AuthMiddlewareStack(inner)))
