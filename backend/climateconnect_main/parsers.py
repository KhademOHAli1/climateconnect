"""
Custom DRF parsers using orjson for faster JSON parsing.
orjson is up to 10x faster than the standard json library.
"""

import orjson
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser


class ORJSONParser(BaseParser):
    """
    Parser that uses orjson for JSON parsing.
    
    orjson provides:
    - Faster parsing than standard json
    - Stricter JSON compliance
    - Better memory efficiency
    """
    
    media_type = "application/json"
    
    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parse the incoming bytestream as JSON and return the resulting data.
        """
        try:
            data = stream.read()
            if not data:
                return None
            return orjson.loads(data)
        except orjson.JSONDecodeError as exc:
            raise ParseError(f"JSON parse error - {exc}")
        except Exception as exc:
            raise ParseError(f"JSON parse error - {exc}")
