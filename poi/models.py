from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class PointOfInterest(models.Model):
    # External ID from source files
    external_id = models.CharField(max_length=255, db_index=True)
    
    # Basic PoI information
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        max_digits=10, 
        decimal_places=7,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    category = models.CharField(max_length=100, db_index=True)
    
    # Store ratings data
    ratings_data = models.TextField(help_text="Raw ratings data")
    average_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Optional fields
    description = models.TextField(blank=True, null=True)
    source_file = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"

    def __str__(self):
        return f"{self.name} ({self.external_id})"

    def save(self, *args, **kwargs):
        if self.ratings_data:
            self.average_rating = self.calculate_average_rating()
        super().save(*args, **kwargs)

    def calculate_average_rating(self):
        if not self.ratings_data:
            return None
        
        try:
            ratings_str = self.ratings_data.strip()
            
            if ratings_str.startswith('[') and ratings_str.endswith(']'):
                ratings = json.loads(ratings_str)
            else:
                ratings = [float(r.strip()) for r in ratings_str.split(',') if r.strip()]
            
            if ratings:
                return round(sum(ratings) / len(ratings), 2)
        except (ValueError, json.JSONDecodeError):
            pass
        
        return None