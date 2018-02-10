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
        context['news'] = News.objects.all().order_by('-created_at')[:3] # -created_at - reversed date

        for item in context['news']:
            item.short = item.text[:150]+'...' # get preview text

        
        return context



class ArticleListView(ListView):
    
    model = News

    template_name = 'blog/blog.html'    
    success_url = None
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):

        context = News.objects.all().order_by('-created_at')
        
        for item in context :
            item.short = item.text[:150]+'...' # get preview text

        return context
    
class ArticleDetailView(DetailView):

    model = News
    template_name = "blog/blog-post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['slug']

        return context