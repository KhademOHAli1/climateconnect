"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.

Optimized for performance with uvicorn/uvloop.
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "climateconnect_main.settings")
django.setup()

from channels.routing import get_default_application  # noqa: E402

application = get_default_application()


def get_application():
    """
    Factory function for creating the ASGI application.
    Used by uvicorn for better process management.
    """
    return application
