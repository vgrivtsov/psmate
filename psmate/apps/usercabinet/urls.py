from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^cabinet/$', views.usercabinet, name='usercabinet'),
    url(r'^settings/$', views.SettingsFormView.as_view()),
    
]
