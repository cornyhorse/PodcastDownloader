from django.apps import AppConfig
from django.db.models.signals import post_migrate


class PodcastsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'podcasts'


# class PodcastsConfig(AppConfig):
#     name = 'podcasts'
#     default_auto_field = 'django.db.models.BigAutoField'
#
#     def ready(self):
#         from .utils import feed_fetch
#         # Ensuring that the method runs only once and not for each worker (in case of WSGI servers)
#         post_migrate.connect(feed_fetch.process_all_cached_feeds, sender=self)
