try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


from django.shortcuts import render
from django.views.generic import UpdateView
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.forms import SearchPsForm
###
from django.contrib.auth.models import User
from .filters import PSFilter

# Create your views here.
# def search(request):
#     ps_list = Psinfo.objects.filter(psregnum=204)
#     ps_filter = PSFilter(request.GET, queryset=ps_list)
#     return render(request, 'services/user_list.html', {'filter': ps_filter})


    
class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = Psinfo.objects.all()

        if self.q:

            qs = qs.filter(nameeks__istartswith=self.q)

        return qs
    

class SearchPs(UpdateView):
    model = Psinfo
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    success_url = reverse_lazy('search-profstandart')

    def get_object(self):
        return Psinfo.objects.first()
    

