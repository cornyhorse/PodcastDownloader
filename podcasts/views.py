# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import PodcastForm
from .models import Podcast
from .utils.feed_fetch import fetch_cache, parse_cache


def home(request):
    return render(request, 'home.html')


def add_podcast(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('podcast_list')
    else:
        form = PodcastForm()
    return render(request, 'add_podcast.html', {'form': form})


def podcast_list(request):
    podcasts = Podcast.objects.all().select_related('detail')
    return render(request, 'podcast_list.html', {'podcasts': podcasts})


def podcast_detail(request, podcast_id):
    podcast = get_object_or_404(Podcast, pk=podcast_id)
    return render(request, 'podcast_detail.html', {'podcast': podcast})


def refresh_all_metadata(request):
    for podcast in Podcast.objects.all():
        fetch_cache(podcast.id)
    return redirect(reverse('podcast_list'))

def parse_metadata(request):
    for podcast in Podcast.objects.all():
        parse_cache(podcast.id)
    return redirect(reverse('podcast_list'))
