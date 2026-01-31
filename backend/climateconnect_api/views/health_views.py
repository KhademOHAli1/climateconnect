"""
Health check endpoint for load balancers and monitoring.

Returns system health status including:
- Database connectivity
- Redis connectivity
- Basic application info
"""

from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time


class HealthCheckView(View):
    """
    Lightweight health check endpoint for load balancers.
    
    GET /health/ - Quick check (no DB)
    GET /health/?full=1 - Full check with DB and Redis
    """
    
    def get(self, request):
        start = time.perf_counter()
        
        # Basic response
        response = {
            "status": "healthy",
            "version": "2.0.0",
            "environment": settings.SENTRY_ENVIRONMENT or "unknown",
        }
        
        # Full check includes DB and Redis
        if request.GET.get("full"):
            checks = {}
            
            # Database check
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                checks["database"] = "ok"
            except Exception as e:
                checks["database"] = f"error: {str(e)[:50]}"
                response["status"] = "degraded"
            
            # Redis check
            try:
                cache.set("health_check", "ok", 10)
                if cache.get("health_check") == "ok":
                    checks["redis"] = "ok"
                else:
                    checks["redis"] = "error: cache read failed"
                    response["status"] = "degraded"
            except Exception as e:
                checks["redis"] = f"error: {str(e)[:50]}"
                response["status"] = "degraded"
            
            response["checks"] = checks
        
        # Add response time
        response["responseTime"] = f"{(time.perf_counter() - start) * 1000:.1f}ms"
        
        status_code = 200 if response["status"] == "healthy" else 503
        return JsonResponse(response, status=status_code)
