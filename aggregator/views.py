
from xml.dom import xmlbuilder
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from .models import Article
from .models import Source
from django.template import loader
import feedparser
from django.urls import reverse
from dateutil import parser
import uuid
import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

def request_guid():
    """
    Helper function, utilizes ZeroMQ Microservice to generate GUIDs.
    Called when a newly parsed article is missing a GUID.
    Microservice must be running locally for this to function.
    """

    # functionally equivalent to the following:
    message = uuid.uuid4()
    # socket.send_string("generateGUID")

    # message = socket.recv_pyobj()
    return message


# Create your views here.

class ArticleView(ListView):
    """
    View for articles associated with a source
    """
    template_name = "homepage.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["articles"] = Article.objects.filter(marked_read=False).order_by("-pub_date")[:40]
        context["count"] = Article.objects.filter(marked_read=False).count()
        return context

class SourceView(ListView):
    """
    View for sources
    """
    template_name = "sources.html"
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sources"] = Source.objects.all()
        context["source_count"] = Source.objects.all().count()
        return context

class BookmarkView(ListView):
    """
    View for bookmarked articles
    """
    template_name = "bookmarks.html"
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bookmarks"] = Article.objects.filter(bookmark=True).order_by("-pub_date")
        context["bookmark_count"] = Article.objects.filter(bookmark=True).count()
        return context

def add_new_source(request):
    """
    Renders template
    """
    template = loader.get_template("add_new_source.html")
    return HttpResponse(template.render({}, request))

def add(request):
    """
    Takes a user-provided link to an RSS feed source and uses it
    to create a new Source object.
    """
    x = request.POST["source_link"]
    feed = feedparser.parse(x)
    new_source = save_source(x, feed)

    for item in feed.entries:
        if 'guid' not in item:
            item.guid = request_guid()
        if not Article.objects.filter(guid=item.guid).exists():
            save_article(item, new_source)

    return HttpResponseRedirect(reverse("add_new_source"))

def refresh(request):
    """
    Iterates across all saves Sources, looking for new
    Articles; if any are found, saves them to database.
    Returns redirect to /articles (homepage)
    """
    sources = Source.objects.all()
    for source in sources:
        rss = source.feed_link
        feed = feedparser.parse(rss)
        for item in feed.entries:
            if 'guid' not in item:
                item.guid = request_guid()
            if not Article.objects.filter(guid=item.guid).exists():
                save_article(item, source)
    
    return HttpResponseRedirect(reverse('articles'))

def save_source(source_link, feed):
    """
    Helper function
    Creates, saves, and returns a new Source object
    """
    feed_title = feed.channel.title
    feed_description = feed.channel.description if 'description' in feed.feed else "Not Provided by Source"
    feed_link = feed.channel.link

    new_source = Source(
        title = feed_title,
        description = feed_description,
        link = feed_link,
        feed_link = source_link,
    )
    new_source.save()
    return new_source

def save_article(entry, source):
    """
    Helper Function
    Accepts an entry in a parsed RSS feed
    Creates and saves an Article objects using information
    from the parsed feed entry
    Returns None
    """
    new_article = Article(
        title = entry.title,
        description=entry.description,
        pub_date = parser.parse(entry.published),
        link = entry.link,
        source_name = source,
        guid = entry.guid,
    )
    new_article.save()

def unfollow(request, id):
    """
    Removes corresponding Source from database
    Deletes every Article associated with Source in a cascade
    Returns redirect to source.html
    """
    source = Source.objects.get(id=id)
    source.delete()
    return HttpResponseRedirect(reverse('sources'))

def update_source(request, id):
    """
    Renders Update URL associated with Source
    """
    source = Source.objects.get(id=id)
    template=loader.get_template('update_source.html')
    context = {
        'source': source
    }
    return HttpResponse(template.render(context, request))

def update(request, id):
    """
    Requests updates information about Source from user,
    updates database entry
    """
    title = request.POST["title"]
    description = request.POST["description"]
    source = Source.objects.get(id=id)
    source.title = title
    source.description = description
    source.save()
    return HttpResponseRedirect(reverse('sources'))

def mark_read(request, id):
    """
    Marks Article objects as "Read", removing them from 
    feed but keeping them in the database to avoid duplicates
    Returns status 204 - No Content
    """
    article = Article.objects.get(id=id)
    article.marked_read = not article.marked_read
    article.save()
    return HttpResponse(status=204)

def toggle_bookmark(request, id):
    """
    Adds or removes a Bookmark tag from an Article object
    Articles where bookmark = True are saved even when marked read,
    and can be viewed separately from other Articles
    Returns status 204 - No Content
    """
    article = Article.objects.get(id=id)
    article.bookmark = not article.bookmark
    article.save()
    return HttpResponse(status=204)