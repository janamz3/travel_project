from django.db import models
from django.contrib.auth.models import User

class Destination(models.Model):
    TYPE_CHOICES = [
        ('nature', 'طبيعة'),
        ('city', 'مدن'),
        ('heritage', 'آثار'),
    ]

    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    trip_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    avg_cost = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    title = models.CharField(max_length=150)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='trips')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    description = models.TextField()
    best_places = models.TextField()
    tips = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    image = models.ImageField(upload_to='trips/', blank=True, null=True)
    duration = models.IntegerField()
    budget = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title