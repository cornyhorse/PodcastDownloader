# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_podcast, name='add_podcast'),
    path('', views.podcast_list, name='podcast_list'),
]
