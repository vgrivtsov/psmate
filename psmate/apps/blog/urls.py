from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^news/$', views.ArticleListView.as_view(), name='news'),
    url(r'^news/(?P<slug>[-\w]+)/$', views.ArticleDetailView.as_view(), name='article-detail'),
    url(r'^$', views.IndexNewsView.as_view(), name='indexnews'),

    
]
