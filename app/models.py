"""
Definition of models.
"""

from django.db import models


class ReaperResult(models.Model):
    owner = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    language = models.CharField(max_length=255)

    options = {'max_digits': 12, 'decimal_places': 6}
    score = models.DecimalField(**options)
    architecture = models.DecimalField(null=True, **options)
    community = models.DecimalField(null=True, **options)
    continuous_integration = models.NullBooleanField(null=True)
    documentation = models.DecimalField(null=True, **options)
    history = models.DecimalField(null=True, **options)
    license = models.NullBooleanField(null=True)
    management = models.DecimalField(null=True, **options)
    unit_test = models.DecimalField(null=True, **options)
    state = models.CharField(max_length=10, null=True)
    stars = models.DecimalField(null=True, **options)
    timestamp = models.DateTimeField()
