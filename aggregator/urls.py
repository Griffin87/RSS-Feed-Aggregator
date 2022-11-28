from django.urls import path

from .views import ArticleView, SourceView, BookmarkView
from . import views

urlpatterns = [
    # urls pertaining to Articles
    path("", ArticleView.as_view(), name="homepage"),
    path('articles', ArticleView.as_view(), name="articles"),
    path('mark_read/<int:id>', views.mark_read, name='mark_read'),
    path('refresh', views.refresh, name='refresh'),

    # urls pertaining to Sources
    path("sources", SourceView.as_view(), name="sources"),
    path("add_new_source/", views.add_new_source, name='add_new_source'),
    path("add_new_source/add/", views.add, name='add'),
    path('update_source/<int:id>', views.update_source, name='update_source'),
    path('update_source/update/<int:id>', views.update, name="update"),
    path('delete/<int:id>', views.unfollow, name='unfollow'),

    # urls pertaining to Bookmarks
    path("bookmarks", BookmarkView.as_view(), name="bookmarks"),
    path('toggle_bookmark/<int:id>', views.toggle_bookmark, name='toggle_bookmark'),
]