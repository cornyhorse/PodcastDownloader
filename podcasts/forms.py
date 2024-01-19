# forms.py

from django import forms
from .models import Podcast

class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['name', 'rss_url']