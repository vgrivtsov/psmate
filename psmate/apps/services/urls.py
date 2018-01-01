from django.conf.urls import url
from django_filters.views import FilterView
from psmate.apps.services.filters import PSFilter

from . import views

urlpatterns = [
    url(r'^profstandart-autocomplete/$', views.SearchPsAuto.as_view(), name='profstandart-autocomplete'),
    url(r'^search-profstandart/$', views.SearchPSView.as_view(), name='search-profstandart'),
    url(r'^generator-cv-resume/$', views.CvEditView.as_view(), name='generator-cv-resume'),
    # url(r'^search-profstandart/$', FilterView.as_view(filterset_class=PSFilter,
    #     template_name='services/search-profstandart.html'), name='search-profstandart'),

]
