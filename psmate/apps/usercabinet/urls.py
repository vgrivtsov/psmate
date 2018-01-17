from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^cabinet/$', login_required(views.UserCabinetView.as_view(), login_url='/login'), name='cabinet'),
    url(r'^settings/$',login_required( views.UserSettingsView.as_view(), login_url='/login'), name='settings'),
    
]
