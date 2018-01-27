from django.conf.urls import url
# from django_pdfkit import PDFView
from . import views
# from psmate.apps.services.filters import JTsearchFilter
# from django_filters.views import FilterView

urlpatterns = [
    url(r'^profstandart-autocomplete/$', views.SearchPsAuto.as_view(), name='profstandart-autocomplete'),
    url(r'^search-profstandart/$', views.SearchPSView.as_view(), name='search-profstandart'),
    url(r'^generator-cv-resume/$', views.CvEditView.as_view(template_name='layouts/layout.html'), name='generator-cv-resume'),
    url(r'^load_ps/$', views.LoadPS.as_view(), name='load_ps'),
    url(r'^load_cv/$', views.LoadCV.as_view(), name='load_cv'),
    url(r'^load_compt/$', views.LoadCompt.as_view(), name='load_compt'),
    url(r'^presentation-cv-resume/$', views.CvPresentView.as_view(),  name='presentation-cv-resume'),
    url(r'^search-jobtitles/$', views.ShowJTlist.as_view(), name='search-jobtitles'),
    
    # url(r'^search-jobtitles/$', FilterView.as_view(filterset_class=JTsearchFilter,
    #     template_name='services/jobtitles-list.html'), name='search-jobtitles'),    
    
    
    
    # url(r'^jt-autocomplete/$', views.SearchJtAuto.as_view(), name='jt-autocomplete'),    
    # url(r'^', views.SearchJtView.as_view()),
    # url(r'^cvtopdf/$', views.html_to_pdf_view, name='cvtopdf'),    

]
