try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy


from django.shortcuts import render
from django.views.generic import FormView
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.forms import SearchPsForm
###
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect

### Search PS ###

class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = Psinfo.objects.all()

        if self.q:

            qs = qs.filter(nameps__icontains=self.q) # icontains - Case-insensitive

        return qs
    

class SearchPs(FormView):
    model = Psinfo
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    #success_url = reverse_lazy('search-profstandart')

    def get_object(self):
        return Psinfo.objects.first()


class SearchPSView(FormView):
    model = Psinfo
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'    
    success_url = None

    def get(self, request, *args, **kwargs):

        form=SearchPsForm
        data = self.request.GET.get('nameps', None)
        if data != None:
            ps_get = Psinfo.objects.filter(id=data) # id=num of autocomplete element. Need to rewrite to psregnum
            psinfo = ps_get[0]
            psregnum = ps_get[0].psregnum
            tfinfo = Tfinfo.objects.filter(psregnum=psregnum)
            okzinfo = Okz.objects.filter(psregnum=psregnum).distinct('codeokz')
            okvedinfo = Okved.objects.filter(psregnum=psregnum).distinct('codeokved')
            
            
            return render(request, self.template_name, {'psinfo': psinfo,
                                                        'tfinfo': tfinfo,
                                                        'okzinfo': okzinfo,
                                                        'okvedinfo': okvedinfo,
                                                        'form': form})
        return render(request, self.template_name, {'form': form})





##################
