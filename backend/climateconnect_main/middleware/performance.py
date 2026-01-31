"""
Performance middleware for sub-500ms FCP optimization.

These middleware classes add HTTP headers that help browsers and CDNs
cache and prioritize resources for faster First Contentful Paint.
"""

import hashlib
import time
from django.conf import settings
from django.utils.cache import patch_cache_control


class CacheControlMiddleware:
    """
    Add Cache-Control headers with stale-while-revalidate for API responses.
    
    This enables the CDN/browser to serve stale content immediately while
    revalidating in the background, reducing TTFB to near-zero for cached responses.
    """
    
    # Endpoints that should be aggressively cached (static filter options)
    LONG_CACHE_PREFIXES = (
        '/api/skills/',
        '/api/availabilities/',
        '/api/project_status/',
        '/api/projecttypes/',
        '/api/sectors/',
        '/api/organization_tags/',
    )
    
    # Endpoints that need short cache but benefit from stale-while-revalidate
    SHORT_CACHE_PREFIXES = (
        '/api/projects/',
        '/api/organizations/',
        '/api/hubs/',
        '/api/members/',
    )
    
    # Endpoints that should never be cached (user-specific or mutation)
    NO_CACHE_PREFIXES = (
        '/api/me/',
        '/api/notifications/',
        '/api/messages/',
        '/api/chat/',
        '/api/login/',
        '/api/signup/',
    )
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only apply to GET requests on API endpoints
        if request.method != 'GET' or not request.path.startswith('/api/'):
            return response
        
        # Skip if already has cache-control or is an error
        if response.get('Cache-Control') or response.status_code >= 400:
            return response
        
        path = request.path
        
        # Check no-cache endpoints first
        if any(path.startswith(prefix) for prefix in self.NO_CACHE_PREFIXES):
            patch_cache_control(response, private=True, no_store=True)
            return response
        
        # Long-cache static endpoints (filter options, etc.)
        if any(path.startswith(prefix) for prefix in self.LONG_CACHE_PREFIXES):
            # Cache for 1 hour, allow stale for 24 hours while revalidating
            patch_cache_control(
                response,
                public=True,
                max_age=3600,  # 1 hour
                stale_while_revalidate=86400,  # 24 hours
                stale_if_error=86400,  # Serve stale on backend errors
            )
            return response
        
        # Short-cache dynamic endpoints
        if any(path.startswith(prefix) for prefix in self.SHORT_CACHE_PREFIXES):
            # Cache for 60 seconds, allow stale for 5 minutes while revalidating
            patch_cache_control(
                response,
                public=True,
                max_age=60,  # 1 minute
                stale_while_revalidate=300,  # 5 minutes
                stale_if_error=3600,  # 1 hour on errors
            )
            return response
        
        return response


class ETagMiddleware:
    """
    Add ETag headers to API responses for conditional requests.
    
    This allows browsers and CDNs to make conditional requests with
    If-None-Match, receiving 304 Not Modified for unchanged content.
    This drastically reduces bandwidth and parsing time.
    """
    
    # Skip ETag for these (large payloads where hashing is expensive)
    SKIP_ETAG_PREFIXES = (
        '/api/messages/',
        '/api/chat/',
    )
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only for successful GET requests on API endpoints
        if (request.method != 'GET' or 
            not request.path.startswith('/api/') or
            response.status_code != 200):
            return response
        
        # Skip large endpoints
        if any(request.path.startswith(p) for p in self.SKIP_ETAG_PREFIXES):
            return response
        
        # Skip if already has ETag
        if response.get('ETag'):
            return response
        
        # Generate ETag from response content
        # Use weak ETag for JSON (semantic equivalence)
        try:
            content = response.content
            etag = 'W/"' + hashlib.md5(content).hexdigest()[:16] + '"'
            response['ETag'] = etag
            
            # Check for conditional request
            if_none_match = request.META.get('HTTP_IF_NONE_MATCH', '')
            if if_none_match and etag in if_none_match:
                # Content unchanged - return 304
                response.status_code = 304
                response.content = b''
                response['Content-Length'] = 0
        except Exception:
            # Don't fail the request if ETag generation fails
            pass
        
        return response


class ServerTimingMiddleware:
    """
    Add Server-Timing header for debugging backend performance.
    
    This header is visible in browser DevTools Network tab and helps
    identify which part of the request is slow.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.perf_counter()
        
        response = self.get_response(request)
        
        # Calculate total time
        total_ms = (time.perf_counter() - start_time) * 1000
        
        # Add Server-Timing header (only in debug or for API)
        if settings.DEBUG or request.path.startswith('/api/'):
            response['Server-Timing'] = f'total;dur={total_ms:.1f}'
        
        return response


class PreloadHintsMiddleware:
    """
    Add Link headers with preload hints for critical resources.
    
    For the browse/projects pages, hint the browser to preload
    the first project image (LCP element) and critical CSS/JS.
    """
    
    # API endpoints that return data with images
    IMAGE_DATA_ENDPOINTS = (
        '/api/projects/',
        '/api/organizations/',
    )
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only for successful API requests that might have images
        if (response.status_code != 200 or 
            not any(request.path.startswith(p) for p in self.IMAGE_DATA_ENDPOINTS)):
            return response
        
        # Add preconnect hints for Azure blob storage (where images are hosted)
        if hasattr(settings, 'AZURE_ACCOUNT_NAME') and settings.AZURE_ACCOUNT_NAME:
            azure_origin = f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net"
            existing_link = response.get('Link', '')
            preconnect = f'<{azure_origin}>; rel=preconnect'
            
            if existing_link:
                response['Link'] = f'{existing_link}, {preconnect}'
            else:
                response['Link'] = preconnect
        
        return response
