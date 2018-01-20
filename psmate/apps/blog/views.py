from django.shortcuts import render
from django.views.generic import  ListView, DetailView, TemplateView
from psmate.models import News
# Create your views here.


class IndexNewsView(TemplateView):
    
    model = News

    template_name = 'index.html'    
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all()[:3]

        for item in context['news']:
            item.short = item.text[:150]+'...' # get preview text

        
        return context



class ArticleListView(TemplateView):
    
    model = News

    template_name = 'blog/blog.html'    
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = News.objects.all()
        for item in context['articles'] :
            item.short = item.text[:150]+'...' # get preview text


        return context
    
class ArticleDetailView(DetailView):

    model = News
    template_name = "blog/blog-post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']

        return context