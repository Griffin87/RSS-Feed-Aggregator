from django.test import TestCase
from django.utils import timezone
from .models import Article
from django.urls.base import reverse
from datetime import datetime
from .models import Source

# Create your tests here.

class SourceTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            title = "Test Source",
            link = "https://testsource.com",
            description = "This is a test source",
        )

    def test_source_contents(self):
        self.assertEqual(self.source.title, "Test Source")
        self.assertEqual(self.source.link, "https://testsource.com")
        self.assertEqual(self.source.description, "This is a test source")

    def test_source_str_rep(self):
        self.assertEqual(str(self.source), "Test Source")

class ArticleTests(TestCase):
    def setUp(self):
        self.source = Source.objects.create(
            title = "Test Source",
            link = "https://testsource.com",
            description = "This is a test source",
        )

        self.article = Article.objects.create(
            title = "Test Article",
            description = "This is a test",
            pub_date=timezone.now(),
            link = "https://test.com",
            source_name=self.source,
            guid="de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_feed_content(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.link, "https://test.com")
        self.assertEqual(self.article.description, "This is a test")
        self.assertEqual(self.article.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")
        self.assertEqual(self.article.source_name, self.source)

    def test_article_str_representation(self):
        self.assertEqual(str(self.article), "Test Source: Test Article")

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "homepage.html")

    def test_homepage_list_contents(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Test Source")