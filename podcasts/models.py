# models.py

from django.db import models

class Podcast(models.Model):
    name = models.CharField(max_length=200)
    rss_url = models.URLField()

    def __str__(self):
        return self.name
