"""
Slim serializers optimized for Server-Side Rendering (SSR).

These serializers return the absolute minimum data needed for initial
page render (FCP/LCP), reducing payload size and serialization time.
The frontend can fetch full data after hydration if needed.
"""

from rest_framework import serializers
from django.utils.translation import get_language

from organization.models import Project, Organization
from organization.utility.project import get_project_name, get_project_short_description


class ProjectSSRSerializer(serializers.ModelSerializer):
    """
    Minimal project serializer for SSR - only what's needed for initial render.
    
    Reduces payload from ~2KB to ~300 bytes per project.
    """
    name = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    project_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "url_slug",
            "image",
            "location",
            "project_type",
            "start_date",
            "end_date",
        )
    
    def get_name(self, obj):
        return get_project_name(obj, get_language())
    
    def get_short_description(self, obj):
        return get_project_short_description(obj, get_language())
    
    def get_image(self, obj):
        # Prefer thumbnail for faster load
        if obj.thumbnail_image:
            return obj.thumbnail_image.url
        if obj.image:
            return obj.image.url
        return None
    
    def get_location(self, obj):
        if obj.loc is None:
            return None
        return obj.loc.name
    
    def get_project_type(self, obj):
        # Return just the type ID string, not full object
        return obj.project_type


class OrganizationSSRSerializer(serializers.ModelSerializer):
    """
    Minimal organization serializer for SSR - only what's needed for initial render.
    """
    image = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "url_slug",
            "image",
            "location",
            "short_description",
        )
    
    def get_image(self, obj):
        if obj.thumbnail_image:
            return obj.thumbnail_image.url
        if obj.image:
            return obj.image.url
        return None
    
    def get_location(self, obj):
        if obj.location is None:
            return None
        return obj.location.name
