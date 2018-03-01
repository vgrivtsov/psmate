from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    
    url(r'^registercompany/$', views.RegisterCompanyFormView.as_view(), name='registercompany'),
    url(r'^companylist/$', views.CompanyCabinetView.as_view(), name='companylist'),
    url(r'^companyprofile/$', views.CompanyCabinetView.as_view(), name='companyprofile'),
    
]
