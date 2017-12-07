from django.shortcuts import render

from django.http import HttpResponse


def cv_index(request):
    return render(request, 'resume/resume_index.html')


def cv_edit(request):
    return render(request, 'resume/resume_edit.html')
