from django.urls import path

from .views import ArticleView, SourceView
from . import views

urlpatterns = [
    # path("", SourceView.as_view(), name="homepage"),
    path("", ArticleView.as_view(), name="homepage"),
    path("add_new_source/", views.add_new_source, name='add_new_source'),
    path("add_new_source/add/", views.add, name='add'),
    path("sources", SourceView.as_view(), name="sources"),
    path('delete/<int:id>', views.unfollow, name='unfollow'),
    path('mark_read/<int:id>', views.mark_read, name='mark_read')
]