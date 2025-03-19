from django.db import models
from django.contrib.auth.models import User


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey("Books", on_delete=models.CASCADE, related_name="reviews")
    rating = models.FloatField(null=False)
    comment = models.CharField(max_length=155, null=False)
    date = models.DateField(null=False)
