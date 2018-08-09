from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=5000, blank=True, default='')
    datetime_created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField()
    datetime_published = models.DateTimeField(blank=True, null=True)