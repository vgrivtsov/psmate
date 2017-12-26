try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


from django.shortcuts import render
from django.views.generic import UpdateView
from dal import autocomplete
from psmate.models import Eks
from psmate.apps.services.forms import SearchPsForm

# Create your views here.

    
class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = Eks.objects.all()

        if self.q:

            qs = qs.filter(nameeks__istartswith=self.q)

        return qs
    

class SearchPs(UpdateView):
    model = Eks
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    success_url = reverse_lazy('search-profstandart')

    def get_object(self):
        return Eks.objects.first()
    
