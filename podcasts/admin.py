from django.contrib import admin

from .models import Podcast, PodcastDetail, Keyword, PodcastCache, PodcastEpisode


@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ['name', 'rss_url']
    search_fields = ['name']  # Define search_fields for PodcastAdmin

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ['word']
    search_fields = ['word']  # Define search_fields for KeywordAdmin


@admin.register(PodcastDetail)
class PodcastDetailAdmin(admin.ModelAdmin):
    list_display = ['podcast', 'title', 'link', 'language', 'author', 'explicit']
    list_filter = ['podcast', 'language', 'author', 'explicit']
    search_fields = ['podcast__name', 'title', 'link', 'language', 'author', 'explicit']
    autocomplete_fields = ['podcast', 'keywords']
    ordering = ['podcast', 'title', 'link', 'language', 'author', 'explicit']


@admin.register(PodcastCache)
class PodcastCacheAdmin(admin.ModelAdmin):
    list_display = ['podcast', 'last_fetched']


@admin.register(PodcastEpisode)
class PodcastEpisodeAdmin(admin.ModelAdmin):
    list_display = ['podcast', 'title', 'link', 'pub_date', 'explicit']
    list_filter = ['podcast', 'explicit']
    search_fields = ['podcast__name', 'title', 'link', 'pub_date', 'explicit']
