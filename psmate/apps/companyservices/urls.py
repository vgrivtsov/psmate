from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    
    url(r'^registercompany/$', views.RegisterCompanyFormView.as_view(), name='registercompany'),
    #url(r'^organizations-list/$', views.OrgListCabinetView.as_view(), name='organizations-list'),
    url(r'^organization-profile/(?P<id>[-\d]+)/$', views.OrgProfileView.as_view(), name='organization-profile'),
    url(r'^organization-settings/(?P<id>[-\d]+)/$', views.OrgSettingsView.as_view(), name='organization-settings'),    
    url(r'^organization-profile/(?P<id>[-\d]+)/registerdepart/$', views.RegisterDepartFormView.as_view(), name='registerdepart'),
    url(r'^organization-profile/(?P<id>[-\d]+)/editdepart/(?P<pk>[-\d]+)/$', views.DepartSettingsView.as_view(), name='editdepart'),
    url(r'^organization-profile/(?P<id>[-\d]+)/removedepart/(?P<pk>[-\d]+)/$', views.DepartDeleteView.as_view(), name='removedepart'),
    
]
