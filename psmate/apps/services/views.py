try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


from django.shortcuts import render
from django.views.generic import UpdateView
from dal import autocomplete
from psmate.models import OtraslList
from psmate.apps.services.forms import SearchPsForm

# Create your views here.

    
class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = OtraslList.objects.all()

        if self.q:

            qs = qs.filter(name__istartswith=self.q)

        return qs
    

class SearchPs(UpdateView):
    model = OtraslList
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    success_url = reverse_lazy('search-autocomplete')

    def get_object(self):
        return OtraslList.objects.first()
    
