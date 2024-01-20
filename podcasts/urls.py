# urls.py

from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_podcast, name='add_podcast'),
    path('', views.podcast_list, name='podcast_list'),
    path('<int:podcast_id>/', views.podcast_detail, name='podcast_detail'),
    path('refresh/', views.refresh_all_metadata, name='refresh_all_metadata'),
    path('parse/', views.parse_metadata, name='parse_metadata')
]
