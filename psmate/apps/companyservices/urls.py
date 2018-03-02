from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    
    url(r'^registercompany/$', views.RegisterCompanyFormView.as_view(), name='registercompany'),
    #url(r'^organizations-list/$', views.OrgListCabinetView.as_view(), name='organizations-list'),
    url(r'^organization-profile/$', views.OrgProfileView.as_view(), name='organization-profile'),
    url(r'^organization-settings/$', views.OrgSettingsView.as_view(), name='organization-settings'),    
]
