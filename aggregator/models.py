from django.db import models

# Create your models here.

class Source(models.Model):
    """
    Each RSS feed has a source/channel
    """
    title = models.CharField(max_length=200,default="No Title")
    link = models.CharField(max_length=200)
    description = models.CharField(max_length=500,default="No Description")

    def __str__(self):
        return self.title

class Article(models.Model):
    """
    RSS feed channels are composed of individual items (or Articles)
    These should be supplied by feedparser.parse() in startjobs.py except for 'marked_read'
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    link = models.URLField()
    image = models.URLField()
    source_name = models.ForeignKey(Source, on_delete=models.CASCADE)
    guid = models.CharField(max_length=50)
    marked_read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.source_name}: {self.title}"
