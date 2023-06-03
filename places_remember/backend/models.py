from django.db import models
from django.contrib.auth.models import User


class Place(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def to_json(self):
        return {
            'latitude': float(self.latitude),
            'longitude': float(self.longitude),
            'name': self.name,
            'comment': self.comment,
        }