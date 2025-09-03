from django.contrib import admin
from .models import PointOfInterest


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    """Admin configuration for PointOfInterest."""

    list_display = (
        'id',              # Internal ID (AutoField PK)
        'name',            # PoI name
        'external_id',     # External ID from source
        'category',        # Category
        'average_rating',  # Computed avg. rating
        'latitude',
        'longitude',
        'created_at',
    )

    list_filter = (
        'category',      # Required filter
        'created_at',
        'source_file',
    )

    search_fields = (
        'id__exact',     # Exact search on internal ID
        'external_id',
        'name',
    )

    readonly_fields = (
        'id',
        'average_rating',
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Basic Information', {
            'fields': ('external_id', 'name', 'category', 'description')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Ratings', {
            'fields': ('ratings_data', 'average_rating')
        }),
        ('Metadata', {
            'fields': ('source_file', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    ordering = ('-created_at',)