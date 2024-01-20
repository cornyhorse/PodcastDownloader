# forms.py

from django import forms

from .models import Podcast, PodcastDetail


class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['name', 'rss_url']


class PodcastDetailForm(forms.ModelForm):
    class Meta:
        model = PodcastDetail
        fields = ['title', 'link', 'language', 'copyright', 'author', 'description', 'owner', 'owner_email',
                  'image_location', 'category', 'explicit', 'keywords']
        widgets = {
            'keywords': forms.CheckboxSelectMultiple,
        }
