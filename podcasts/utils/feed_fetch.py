# podcasts/utils/feed_fetch.py
import logging
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup as bs

if __name__ != '__main__':
    from podcasts.models import Podcast, PodcastCache, PodcastDetail, Keyword

from datetime import datetime


def sanitize_date_format(date_str):
    try:
        # Attempt to parse the date string with the expected format
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
        # Reformat the date to the desired format
        formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S%z')
        return formatted_date
    except ValueError:
        # Handle invalid date formats here
        return None


def sanitize_boolean(value):
    if value.lower() == 'yes':
        return True
    elif value.lower() == 'no':
        return False
    else:
        return None

class Feed:
    def __init__(self, podcast_id, xml_content):
        self.podcast_id = podcast_id
        self.xml_content = xml_content
        self.root = None
        self.channel = None
        self.soup = None
        self.fetch_root()

    def fetch_root(self):
        try:
            self.root = ET.fromstring(self.xml_content)
            self.channel = self.root.find('channel')
            self.soup = bs(self.xml_content, 'xml')

        except ET.ParseError as e:
            logging.error(f"XML parsing error for podcast {self.podcast_id}: {e}")

    def parse(self):
        if self.root is None:
            logging.error(f"Root element not found for podcast {self.podcast_id}")
            return None

        detail_data = self.get_podcast_detail()

        if __name__ != '__main__':
            self.update_database(detail_data)
        else:
            # pass
            from pprint import pprint
            pprint(detail_data)

        episodes = self.get_podcast_episodes()

        if __name__ != '__main__':
            self.add_podcast_episodes(episodes)

        # try:
        #     logging.info(f"Parsing podcast detail for podcast {self.podcast_id}")
        #     self.get_podcast_detail()
        # except Exception as e:
        #     logging.error(f"Error parsing podcast detail for podcast {self.podcast_id}: {e}")

        # try:
        #     logging.info(f"Parsing podcast episodes for podcast {self.podcast_id}")
        #     self.get_podcast_episodes()
        # except Exception as e:
        #     logging.error(f"Error parsing podcast episodes for podcast {self.podcast_id}: {e}")

    def _find_element(self, path, optional=False, attribute=None):
        # Define the namespaces
        namespaces = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

        # Split the path into parts
        path_parts = path.split('/')

        # Initialize the root element
        current_element = self.channel

        for part in path_parts:
            # Try to find the element with the current part
            element_with_namespace = current_element.find(f".//itunes:{part}", namespaces=namespaces)

            # If not found, try without the namespace
            if element_with_namespace is None:
                element_without_namespace = current_element.find(f".//{part}")

                # If still not found, return None
                if element_without_namespace is None:
                    if optional:
                        return None
                    logging.warning(f"Element {path} not found in podcast {self.podcast_id}")
                    return None

                current_element = element_without_namespace
            else:
                current_element = element_with_namespace

        if attribute:
            # If an attribute is specified, return its value from the element
            return current_element.get(attribute)

        return current_element.text

    def get_podcast_detail(self):
        if self.root is None:
            return None

        detail_data = {
            'title': self._find_element('title', optional=True),
            'link': self._find_element('link', optional=False),
            'language': self._find_element('language', optional=True),
            'copyright': self._find_element('copyright', optional=True),
            'author': self._find_element('author', optional=True),
            'description': self._find_element('description', optional=True),
            'keywords': self._find_element('keywords', optional=True),
            'new_feed_url': self._find_element('new-feed-url', optional=True),
            'owner': self._find_element('owner/name', optional=True),
            'owner_email': self._find_element('owner/email', optional=True),
            'image_location': self._find_element('image', optional=True, attribute='href'),
            'category': self._find_element('category', optional=True, attribute='text'),
            'explicit': sanitize_boolean(self._find_element('explicit', optional=True)),
        }
        return detail_data

    def update_database(self, detail_data):
        podcast = Podcast.objects.get(pk=self.podcast_id)

        # Try to retrieve an existing PodcastDetail instance
        try:
            detail = PodcastDetail.objects.get(podcast=podcast)
        except PodcastDetail.DoesNotExist:
            # If it doesn't exist, create a new one
            detail = PodcastDetail(podcast=podcast)

        # Save the PodcastDetail instance to the database before updating many-to-many
        detail.save()

        # Update its fields with the new data
        for key, value in detail_data.items():
            if key == 'keywords':
                # Handle the many-to-many field separately using .set()
                keywords = value.split(',')
                keyword_objs = []
                for keyword in keywords:
                    keyword = keyword.strip()
                    if keyword:
                        keyword_obj, created = Keyword.objects.get_or_create(word=keyword)
                        keyword_objs.append(keyword_obj)
                detail.keywords.set(keyword_objs)
            else:
                # Update other fields directly
                setattr(detail, key, value)

        logging.info(f"Updated podcast detail for podcast {self.podcast_id}")

    def get_podcast_episodes(self):
        if self.root is None:
            return None
        episodes = []

        for item in self.root.findall('channel/item'):
            episode = {
                'title': self._find_element('title', attribute=None),
                'link': self._find_element('link', attribute=None),
                'description': self._find_element('description', attribute=None),
                'enclosure_length': self._find_element('enclosure', attribute='length'),
                'enclosure_type': self._find_element('enclosure', attribute='type'),
                'enclosure_url': self._find_element('enclosure', attribute='url'),
                'guid': self._find_element('guid', attribute=None),
                'pub_date': self._find_element('pubDate', attribute=None),
                'duration': self._find_element('duration', attribute=None),
                'explicit': sanitize_boolean(self._find_element('explicit', attribute=None)),
            }
            if episode.get('pub_date'):
                episode['pub_date'] = sanitize_date_format(episode['pub_date'])

            episodes.append(episode)
        return episodes

    def add_podcast_episodes(self, episodes):
        podcast = Podcast.objects.get(pk=self.podcast_id)
        for episode in episodes:
            print(episode)

            podcast.episodes.update_or_create(
                guid=episode['guid'],
                defaults=episode
            )
        logging.info(f"Updated podcast episodes for podcast {self.podcast_id}")


def fetch_cache(podcast_id):
    logging.info(f"Fetching and updating cache for podcast {podcast_id}")
    podcast = Podcast.objects.get(pk=podcast_id)
    response = requests.get(podcast.rss_url)

    if response.status_code == 200:
        logging.info(f"Fetched content for podcast {podcast_id}")
        cache, created = PodcastCache.objects.update_or_create(
            podcast=podcast,
            defaults={'content': response.text}
        )


    else:
        logging.error(f"Error fetching podcast {podcast_id}: {response.status_code}")


def parse_cache(podcast_id):
    logging.info(f"Fetching and updating cache for podcast {podcast_id}")
    podcast = Podcast.objects.get(pk=podcast_id)
    cache = PodcastCache.objects.get(podcast=podcast)
    feed = Feed(podcast_id, cache.content)
    feed.parse()


if __name__ == '__main__':
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, 'sample_data/agile_mentors.xml')) as f:
        xml_content = f.read()
    feed = Feed(1, xml_content)
    feed.parse()
