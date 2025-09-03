from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class PointOfInterest(models.Model):
    """
    A Point of Interest (PoI) imported from CSV, JSON, or XML files.
    Stores geographical location, category, ratings, and optional metadata.
    """

    # External ID from source files
    external_id = models.CharField(
        max_length=255,
        db_index=True,
        help_text="External identifier from the source file"
    )

    # Basic PoI information
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text="Latitude in decimal degrees (-90 to 90)"
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text="Longitude in decimal degrees (-180 to 180)"
    )
    category = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Category of the PoI (e.g., restaurant, park, school)"
    )

    # Store ratings data
    ratings_data = models.TextField(
        help_text="Raw ratings data (JSON array or comma-separated string)"
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Average rating calculated from ratings_data"
    )

    # Optional fields
    description = models.TextField(blank=True, null=True)
    source_file = models.CharField(
        max_length=255,
        blank=True,
        help_text="Name of the file where this record originated"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"
        ordering = ["name"]  # standard practice: deterministic ordering

    def __str__(self) -> str:
        """Human-readable string representation of the PoI."""
        return f"{self.name} ({self.external_id})"

    def save(self, *args, **kwargs):
        """
        Override save to compute the average rating
        whenever ratings_data is provided.
        """
        if self.ratings_data:
            self.average_rating = self.calculate_average_rating()
        super().save(*args, **kwargs)

    def calculate_average_rating(self):
        """
        Calculate the average rating from ratings_data.
        Supports JSON arrays (e.g., [1,2,3]) and
        comma-separated strings (e.g., "1,2,3").
        """
        if not self.ratings_data:
            return None

        try:
            ratings_str = self.ratings_data.strip()

            # Handle JSON list format
            if ratings_str.startswith("[") and ratings_str.endswith("]"):
                ratings = json.loads(ratings_str)
            else:
                # Handle comma-separated values
                ratings = [
                    float(r.strip())
                    for r in ratings_str.split(",")
                    if r.strip()
                ]

            if ratings:
                return round(sum(ratings) / len(ratings), 2)

        except (ValueError, json.JSONDecodeError):
            return None

        return None