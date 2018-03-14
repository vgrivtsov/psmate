from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    
    # path('change-password/', auth_views.PasswordChangeView.as_view()),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^cabinet/$', views.UserCabinetView.as_view(),  name='cabinet'),
    url(r'^settings/$',views.UserSettingsView.as_view(), name='settings'),
     
]
