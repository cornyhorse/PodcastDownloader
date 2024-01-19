# views.py

from django.shortcuts import render, redirect

from .forms import PodcastForm
from .models import Podcast


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
    podcasts = Podcast.objects.all()
    return render(request, 'podcast_list.html', {'podcasts': podcasts})
