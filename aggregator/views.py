
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
        return context

def add_new_source(request):
    template = loader.get_template("add_new_source.html")
    return HttpResponse(template.render({}, request))

def add(request):
    x = request.POST["source_link"]
    feed = feedparser.parse(x)
    feed_title = feed.channel.title
    feed_description = feed.channel.description if 'description' in feed.feed else "Not Provided by Source"
    feed_link = feed.channel.link

    new_source = Source(
        title = feed_title,
        description = feed_description,
        link = feed_link,
        feed_link = x,
    )
    new_source.save()

    for item in feed.entries:
        if 'guid' not in item:
            item.guid = uuid.uuid4()
        if not Article.objects.filter(guid=item.guid).exists():
            new_article = Article(
                title = item.title,
                description=item.description,
                pub_date = parser.parse(item.published),
                link = item.link,
                source_name = new_source,
                guid = item.guid if 'guid' in feed.entries else uuid.uuid4(),
            )
            new_article.save()

    return HttpResponseRedirect(reverse("add_new_source"))

def refresh(request):
    sources = Source.objects.all()
    for source in sources:
        rss = source.feed_link
        feed = feedparser.parse(rss)
        for item in feed.entries:
            if 'guid' not in item:
                item.guid = uuid.uuid4()
            if not Article.objects.filter(guid=item.guid).exists():
                new_article = Article(
                    title = item.title,
                    description=item.description,
                    pub_date = parser.parse(item.published),
                    link = item.link,
                    source_name = source,
                    guid = item.guid if 'guid' in feed.entries else uuid.uuid4(),
                )
                new_article.save()
    
    return HttpResponseRedirect(reverse('articles'))

def unfollow(request, id):
    source = Source.objects.get(id=id)
    source.delete()
    return HttpResponseRedirect(reverse('sources'))

def update_source(request, id):
    source = Source.objects.get(id=id)
    template=loader.get_template('update_source.html')
    context = {
        'source': source
    }
    return HttpResponse(template.render(context, request))

def update(request, id):
    title = request.POST["title"]
    description = request.POST["description"]
    source = Source.objects.get(id=id)
    source.title = title
    source.description = description
    source.save()
    return HttpResponseRedirect(reverse('sources'))

def mark_read(request, id):
    article = Article.objects.get(id=id)
    article.marked_read = True
    article.save()
    return HttpResponseRedirect(reverse('articles'))