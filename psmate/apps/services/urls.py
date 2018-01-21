from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django_pdfkit import PDFView
from . import views

urlpatterns = [
    url(r'^profstandart-autocomplete/$', views.SearchPsAuto.as_view(), name='profstandart-autocomplete'),
    url(r'^search-profstandart/$', views.SearchPSView.as_view(), name='search-profstandart'),
    url(r'^generator-cv-resume/$', login_required(views.CvEditView.as_view(), login_url='/login'), name='generator-cv-resume'),
    url(r'^load_ps/$', views.LoadPS.as_view(), name='load_ps'),
    url(r'^load_cv/$', views.LoadCV.as_view(), name='load_cv'),
    url(r'^load_compt/$', views.LoadCompt.as_view(), name='load_compt'),
    url(r'^presentation-cv-resume/$', login_required(views.CvPresentView.as_view(), login_url='/login'), name='presentation-cv-resume'),
    # url(r'^cvtopdf/$', views.html_to_pdf_view, name='cvtopdf'),    

]
