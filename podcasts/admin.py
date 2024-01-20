from django.contrib import admin
from .models import Podcast, PodcastDetail, Keyword, PodcastCache

admin.site.register(Podcast)
admin.site.register(PodcastDetail)
admin.site.register(Keyword)
admin.site.register(PodcastCache)