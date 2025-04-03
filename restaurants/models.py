from django.db import models
from django.db.models import Avg

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    cuisine_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def average_score(self):
        return self.reviews.aggregate(Avg('score'))['score__avg'] or 0
