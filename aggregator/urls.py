from django.urls import path

from .views import ArticleView, SourceView, BookmarkView
from . import views

urlpatterns = [
    path("", ArticleView.as_view(), name="homepage"),
    path("add_new_source/", views.add_new_source, name='add_new_source'),
    path("add_new_source/add/", views.add, name='add'),
    path("sources", SourceView.as_view(), name="sources"),
    path('delete/<int:id>', views.unfollow, name='unfollow'),
    path('mark_read/<int:id>', views.mark_read, name='mark_read'),
    path('articles', ArticleView.as_view(), name="articles"),
    path('update_source/<int:id>', views.update_source, name='update_source'),
    path('update_source/update/<int:id>', views.update, name="update"),
    path('refresh', views.refresh, name='refresh'),
    path("bookmarks", BookmarkView.as_view(), name="bookmarks"),
    path('toggle_bookmark/<int:id>', views.toggle_bookmark, name='toggle_bookmark'),
]