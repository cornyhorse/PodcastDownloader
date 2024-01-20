from django.db import models


class Podcast(models.Model):
    name = models.CharField(max_length=200)
    rss_url = models.URLField()

    def __str__(self):
        return self.name


class Keyword(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word


class PodcastDetail(models.Model):
    podcast = models.OneToOneField(Podcast, on_delete=models.CASCADE, related_name='detail')
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    new_feed_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    copyright = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    image_location = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    explicit = models.BooleanField(default=False, blank=True, null=True)
    keywords = models.ManyToManyField(Keyword)

    def __str__(self):
        return self.title


class PodcastCache(models.Model):
    podcast = models.OneToOneField(Podcast, on_delete=models.CASCADE, related_name='cache')
    content = models.TextField()
    last_fetched = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cache for {self.podcast.name}"


class PodcastEpisode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='episodes')
    title = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    enclosure_length = models.IntegerField(blank=True, null=True)
    enclosure_type = models.CharField(max_length=100, blank=True, null=True)
    enclosure_url = models.URLField(blank=True, null=True)
    guid = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    explicit = models.BooleanField(default=False)

    def __str__(self):
        return self.title
