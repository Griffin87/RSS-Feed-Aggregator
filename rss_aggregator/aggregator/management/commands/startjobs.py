from django.core.management.base import BaseCommand
import feedparser
from dateutil import parser

from aggregator.models import Article
from aggregator.models import Source

def add_new_source(source):
    feed = feedparser.parse(source)
    feed_title = feed.channel.title
    feed_description = feed.channel.description if 'description' in feed.feed else "None"
    feed_link = feed.channel.link

    new_source = Source(
        title = feed_title,
        description = feed_description,
        link = feed_link,
    )
    new_source.save()

    fetch_new_episodes(feed, new_source)

def remove_source(source):
    """
    Delete a single source
    Should cascade to delete all associated items
    """
    Source.objects.filter(title=source).delete()

def fetch_new_episodes(feed, source):
    feed_title = feed.channel.title

    for item in feed.entries:
        if not Article.objects.filter(guid=item.guid).exists():
            new_article = Article(
                title = item.title,
                description=item.description,
                pub_date = parser.parse(item.published),
                link = item.link,
                source_name = source,
                guid = item.guid,
            )
            new_article.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("It works?")
        # add_new_source("https://realpython.com/podcasts/rpp/feed")
        # add_new_source("https://www.theatlantic.com/feed/all/")

        remove_source("The Real Python Podcast")
        remove_source("The Atlantic")
        remove_source("")

        for item in Article.objects.all():
            print(str(item))