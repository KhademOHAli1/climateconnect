"""
SSR (Server-Side Rendering) optimized views for sub-500ms FCP.

These endpoints are specifically designed for Next.js getServerSideProps:
- Bundle multiple API calls into one request
- Return minimal payload for initial render
- Heavily cached with aggressive stale-while-revalidate
- Async views for better concurrency under load (Django 5.x)
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch, Count
from asgiref.sync import sync_to_async

from organization.models import Project, Organization
from organization.serializers.ssr import ProjectSSRSerializer, OrganizationSSRSerializer
from climateconnect_api.models.common import Skill
from climateconnect_api.serializers.common import SkillSerializer
from hubs.models.hub import Hub
from hubs.serializers.hub import HubStubSerializer


class BrowseSSRView(APIView):
    """
    Bundled endpoint for /browse page SSR.
    
    Returns all data needed for initial render in a single request:
    - First page of projects (slim format)
    - First page of organizations (slim format)
    - Filter options (skills, project types)
    - Hub list
    
    This reduces 6+ API calls to 1, dramatically improving TTFB.
    """
    permission_classes = [AllowAny]
    
    # Cache for 30 seconds with stale-while-revalidate (via middleware)
    # Short cache reduces Redis memory while still improving TTFB
    @method_decorator(cache_page(30, key_prefix="browse_ssr"))
    def get(self, request, *args, **kwargs):
        # Limit for SSR - just enough for above-the-fold content
        PROJECT_LIMIT = 12
        ORG_LIMIT = 6
        
        # Efficient queries with minimal fields
        projects = (
            Project.objects
            .filter(is_draft=False, is_active=True)
            .select_related("loc")
            .only(
                "id", "url_slug", "image", "thumbnail_image",
                "project_type", "start_date", "end_date",
                "loc__name"
            )
            .order_by("-id")[:PROJECT_LIMIT]
        )
        
        organizations = (
            Organization.objects
            .select_related("location")
            .only(
                "id", "name", "url_slug", "image", "thumbnail_image",
                "short_description", "location__name"
            )
            .order_by("-id")[:ORG_LIMIT]
        )
        
        # Get hubs (cached separately, changes rarely)
        hubs = Hub.objects.filter(
            hub_type__in=[Hub.LOCATION_HUB_TYPE, Hub.SECTOR_HUB_TYPE]
        ).only("id", "name", "url_slug", "hub_type")[:20]
        
        # Serialize with slim serializers
        project_data = ProjectSSRSerializer(projects, many=True).data
        org_data = OrganizationSSRSerializer(organizations, many=True).data
        hub_data = HubStubSerializer(hubs, many=True).data
        
        return Response({
            "projects": {
                "results": project_data,
                "hasMore": Project.objects.filter(is_draft=False, is_active=True).count() > PROJECT_LIMIT,
            },
            "organizations": {
                "results": org_data,
                "hasMore": Organization.objects.count() > ORG_LIMIT,
            },
            "hubs": hub_data,
            # Include timestamp for cache debugging
            "cacheTimestamp": None,  # Will be set by cache
        }, status=status.HTTP_200_OK)


class ProjectTypesSSRView(APIView):
    """
    Cached project types for SSR.
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(3600, key_prefix="project_types_ssr"))
    def get(self, request, *args, **kwargs):
        from organization.models.type import PROJECT_TYPES
        
        types = [
            {"id": pt.type_id, "name": pt.name}
            for pt in PROJECT_TYPES.values()
        ]
        return Response(types, status=status.HTTP_200_OK)


class FilterOptionsSSRView(APIView):
    """
    All filter options bundled for SSR.
    
    Returns skills, sectors, project types in one call.
    Cached for 1 hour (filter options rarely change).
    """
    permission_classes = [AllowAny]
    
    @method_decorator(cache_page(3600, key_prefix="filter_options_ssr"))
    def get(self, request, *args, **kwargs):
        from organization.models import Sector
        from organization.serializers.sector import SectorSerializer
        from organization.models.type import PROJECT_TYPES
        
        # Skills - just parent skills for filter dropdown
        skills = Skill.objects.filter(parent_skill=None).only("id", "name")
        
        # Sectors
        sectors = Sector.objects.all().only("id", "name")
        
        # Project types
        project_types = [
            {"id": pt.type_id, "name": pt.name}
            for pt in PROJECT_TYPES.values()
        ]
        
        return Response({
            "skills": SkillSerializer(skills, many=True).data,
            "sectors": SectorSerializer(sectors, many=True).data,
            "projectTypes": project_types,
        }, status=status.HTTP_200_OK)


# =============================================================================
# ASYNC VIEWS (Django 5.x) - Better concurrency under load
# =============================================================================

class AsyncBrowseSSRView(APIView):
    """
    Async version of BrowseSSRView for better concurrency.
    
    Use this endpoint when running with uvicorn/daphne for
    improved performance under high concurrent load.
    
    Endpoint: /api/ssr/browse/async/
    """
    permission_classes = [AllowAny]
    
    async def get(self, request, *args, **kwargs):
        PROJECT_LIMIT = 12
        ORG_LIMIT = 6
        
        # Run DB queries concurrently using sync_to_async
        @sync_to_async
        def get_projects():
            projects = list(
                Project.objects
                .filter(is_draft=False, is_active=True)
                .select_related("loc")
                .only(
                    "id", "url_slug", "image", "thumbnail_image",
                    "project_type", "start_date", "end_date",
                    "loc__name"
                )
                .order_by("-id")[:PROJECT_LIMIT]
            )
            return ProjectSSRSerializer(projects, many=True).data
        
        @sync_to_async
        def get_organizations():
            orgs = list(
                Organization.objects
                .select_related("location")
                .only(
                    "id", "name", "url_slug", "image", "thumbnail_image",
                    "short_description", "location__name"
                )
                .order_by("-id")[:ORG_LIMIT]
            )
            return OrganizationSSRSerializer(orgs, many=True).data
        
        @sync_to_async
        def get_hubs():
            hubs = list(
                Hub.objects.filter(
                    hub_type__in=[Hub.LOCATION_HUB_TYPE, Hub.SECTOR_HUB_TYPE]
                ).only("id", "name", "url_slug", "hub_type")[:20]
            )
            return HubStubSerializer(hubs, many=True).data
        
        @sync_to_async
        def get_counts():
            return {
                "projects": Project.objects.filter(is_draft=False, is_active=True).count() > PROJECT_LIMIT,
                "orgs": Organization.objects.count() > ORG_LIMIT,
            }
        
        # Execute all queries concurrently
        import asyncio
        project_data, org_data, hub_data, counts = await asyncio.gather(
            get_projects(),
            get_organizations(),
            get_hubs(),
            get_counts(),
        )
        
        return Response({
            "projects": {
                "results": project_data,
                "hasMore": counts["projects"],
            },
            "organizations": {
                "results": org_data,
                "hasMore": counts["orgs"],
            },
            "hubs": hub_data,
        }, status=status.HTTP_200_OK)

