from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^resume-index', views.cv_index, name='resume_index'),
    url(r'^resume-edit', views.cv_edit, name='resume_edit'),
]
