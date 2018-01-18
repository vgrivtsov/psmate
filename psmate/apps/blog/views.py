from django.shortcuts import render
from django.views.generic import  ListView, DetailView, TemplateView
from psmate.models import News
# Create your views here.

class ArticleListView(TemplateView):
    
    model = News

    template_name = 'blog/blog.html'    
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = News.objects.all() #[:5]
        # [x.text[:150]+'...' for x in context['articles']]


        return context