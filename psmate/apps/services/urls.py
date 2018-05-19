from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^profstandart-autocomplete/$', views.SearchPsAuto.as_view(), name='profstandart-autocomplete'),
    url(r'^search-profstandart/$', views.SearchPSView.as_view(), name='search-profstandart'),
    url(r'^generator-cv-resume/$', views.CvEditView.as_view(), name='generator-cv-resume',),
    url(r'^load_ps/$', views.LoadPS.as_view(), name='load_ps'),
    url(r'^load_cv/$', views.LoadCV.as_view(), name='load_cv'),
    url(r'^load_compt/$', views.LoadCompt.as_view(), name='load_compt'),
    url(r'^presentation-cv-resume/$', views.CvPresentView.as_view(),  name='presentation-cv-resume'),
    url(r'^jt-autocomplete/$', views.AutoLoadJT.as_view(), name='jt-autocomplete'),
    url(r'^search-jobtitles/$', views.ShowJTlist.as_view(), name='search-jobtitles'),
    url(r'^competences/(?P<slug>[\w-]+)/$', views.JTDetailsView.as_view(), name='competences'),
    url(r'^official-instructions/(?P<slug>[\w-]+)/(?:(?P<docx>[\w-]+)/)?$', views.OfficialInstructions.as_view(), name='official-instructions'),


]
