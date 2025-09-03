from django.contrib import admin
from .models import PointOfInterest


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = [
        'id',  # PoI internal ID
        'name',  # PoI name
        'external_id',  # PoI external ID
        'category',  # PoI category
        'average_rating',  # Avg. rating
        'latitude',
        'longitude',
        'created_at'
    ]
    
    list_filter = [
        'category',  # Filter by category
        'created_at',
        'source_file',
    ]
    
    search_fields = [
        'id',  # Search by PoI internal ID
        'external_id',  # Search by PoI external ID
        'name',
    ]
    
    readonly_fields = [
        'id',
        'average_rating',
        'created_at',
        'updated_at'
    ]
    
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
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']