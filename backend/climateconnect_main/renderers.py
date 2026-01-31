"""
Custom DRF renderers using orjson for faster JSON serialization.
orjson is up to 10x faster than the standard json library.
"""

import orjson
from rest_framework.renderers import BaseRenderer


class ORJSONRenderer(BaseRenderer):
    """
    Renderer that uses orjson for JSON serialization.
    
    orjson provides:
    - 10x faster serialization than standard json
    - Native datetime/date/time serialization
    - Native UUID serialization
    - Native numpy array support
    """
    
    media_type = "application/json"
    format = "json"
    charset = None  # orjson returns bytes, not str
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b""
        
        # orjson options for optimal serialization
        # OPT_SERIALIZE_NUMPY: Serialize numpy arrays
        # OPT_NAIVE_UTC: Serialize naive datetime as UTC
        # OPT_UTC_Z: Use "Z" suffix for UTC timezone
        options = (
            orjson.OPT_SERIALIZE_NUMPY
            | orjson.OPT_NAIVE_UTC
            | orjson.OPT_UTC_Z
        )
        
        try:
            return orjson.dumps(data, option=options)
        except TypeError:
            # Fallback: try with default serializer for edge cases
            return orjson.dumps(data, option=options, default=str)
