"""
API Response Caching Utilities for Performance Optimization

This module provides caching utilities to reduce database load and improve API response times.
"""
import hashlib
import json
from functools import wraps
from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response

# Cache timeouts (in seconds)
BROWSE_CACHE_TIMEOUT = 60  # 1 minute for browse page - balances freshness with performance
FILTER_OPTIONS_CACHE_TIMEOUT = 3600  # 1 hour for filter options (sectors, skills, etc.)
PROJECT_DETAIL_CACHE_TIMEOUT = 300  # 5 minutes for individual project pages


def generate_cache_key(prefix: str, **kwargs) -> str:
    """
    Generate a consistent cache key from a prefix and keyword arguments.
    
    Args:
        prefix: A string prefix to namespace the cache key
        **kwargs: Key-value pairs to include in the cache key
        
    Returns:
        A hashed cache key string
    """
    # Sort kwargs for consistent key generation
    sorted_params = sorted(kwargs.items())
    params_string = json.dumps(sorted_params, sort_keys=True, default=str)
    params_hash = hashlib.md5(params_string.encode()).hexdigest()[:12]
    return f"{prefix}:{params_hash}"


def cached_api_response(prefix: str, timeout: int = BROWSE_CACHE_TIMEOUT, vary_on_user: bool = False):
    """
    Decorator to cache API responses.
    
    Args:
        prefix: Cache key prefix
        timeout: Cache timeout in seconds
        vary_on_user: If True, cache separately for authenticated users
        
    Usage:
        @cached_api_response("projects_list", timeout=60)
        def list(self, request, *args, **kwargs):
            ...
    """
    def decorator(view_method):
        @wraps(view_method)
        def wrapper(self, request, *args, **kwargs):
            # Build cache key from query parameters
            query_dict = dict(request.query_params)
            
            if vary_on_user and request.user.is_authenticated:
                query_dict['_user_id'] = request.user.id
            
            cache_key = generate_cache_key(
                prefix,
                **query_dict,
                page=request.query_params.get('page', 1),
            )
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                return Response(cached_response)
            
            # Generate fresh response
            response = view_method(self, request, *args, **kwargs)
            
            # Only cache successful responses
            if response.status_code == 200:
                cache.set(cache_key, response.data, timeout)
            
            return response
        return wrapper
    return decorator


def invalidate_project_cache():
    """
    Invalidate all project-related caches.
    Call this when a project is created, updated, or deleted.
    """
    # Use cache versioning or key patterns to invalidate
    # For django-redis, you can use delete_pattern
    try:
        cache.delete_pattern("projects_list:*")
        cache.delete_pattern("project_detail:*")
    except AttributeError:
        # Fallback for caches that don't support delete_pattern
        pass


def invalidate_organization_cache():
    """
    Invalidate all organization-related caches.
    """
    try:
        cache.delete_pattern("organizations_list:*")
        cache.delete_pattern("organization_detail:*")
    except AttributeError:
        pass


def get_or_set_filter_options(key: str, queryset_func, serializer_class, timeout: int = FILTER_OPTIONS_CACHE_TIMEOUT):
    """
    Cache filter options (sectors, skills, tags, etc.) which change infrequently.
    
    Args:
        key: Cache key
        queryset_func: Function that returns the queryset
        serializer_class: DRF serializer class
        timeout: Cache timeout
        
    Returns:
        Serialized data
    """
    cached_data = cache.get(key)
    if cached_data is not None:
        return cached_data
    
    queryset = queryset_func()
    serializer = serializer_class(queryset, many=True)
    data = serializer.data
    
    cache.set(key, data, timeout)
    return data
