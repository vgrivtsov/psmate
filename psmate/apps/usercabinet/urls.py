from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='layouts/layout.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='layouts/layout.html'), name='logout'), 
    # path('change-password/', auth_views.PasswordChangeView.as_view()),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^cabinet/$', login_required(views.UserCabinetView.as_view(), login_url='/login'), name='cabinet'),
    url(r'^settings/$',login_required( views.UserSettingsView.as_view(), login_url='/login'), name='settings'),
     
]
