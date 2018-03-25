"""psmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from allauth.account.views import SignupView

admin.autodiscover()

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/signup', SignupView.as_view(success_url='/settings/'), name='account_signup'),
    path('account_login', auth_views.LoginView.as_view(template_name='layouts/layout.html',
                                               success_url='/'), name='account_login'),
    path('account_logout', auth_views.LogoutView.as_view(template_name='layouts/layout.html'), name='account_logout'),
    url(r'^mongolia/', admin.site.urls),
    # url(r'^$', TemplateView.as_view(template_name='index.html')),account_signup
    url(r'^agreement/$', TemplateView.as_view(template_name='agreement.html')),
    url(r'^faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^contacts/', include('envelope.urls')),
    url(r'^', include('psmate.apps.usercabinet.urls')),
    url(r'^', include('psmate.apps.resume.urls')),
    url(r'^', include('psmate.apps.services.urls')),
    url(r'^', include('psmate.apps.blog.urls')),
    url(r'^', include('psmate.apps.companyservices.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
