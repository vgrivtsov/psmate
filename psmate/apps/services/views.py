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
from django.http import HttpResponse
from django.shortcuts import redirect

# def searchps(request):
#     ps_list = Psinfo.objects.all() # .objects.filter(psregnum=204)
#     ps_filter = PSFilter(request.GET, queryset=ps_list)
#     
#     return render(request, 'services/search-profstandart.html', {'filter': ps_filter})






### Search PS ###

class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = Psinfo.objects.all()

        if self.q:

            qs = qs.filter(nameps__istartswith=self.q)

        return qs
    

class SearchPs(UpdateView):
    model = Psinfo
    form_class = SearchPsForm
    template_name = 'services/search-profstandart.html'
    #success_url = reverse_lazy('search-profstandart')

    def get_object(self):
        return Psinfo.objects.first()
 
    # def get_queryset(self):
    #     queryset = Psinfo.objects.all()
    # 
    #     if self.request.GET.get('nameps'):
    #         queryset = queryset.filter(nameps=self.request.GET.get('nameps'))
    #     return queryset
    
    
def searchps(request):
    if request.method == 'GET':
        search_ps = request.GET.get('nameps', None)
        print("NAME_PS",search_ps)
        try:
            ps = Psinfo.objects.filter(id=search_ps)
            #for i in nameofps:
            
                #print("",i.psregnum)
                
                #do something with user
                #html = ("<H1>%s</H1>" % i.psregnum)
            psinfo = {'psinfo': ps}
            return render(request, 'search-profstandart', psinfo)
        except Psinfo.DoesNotExist:
            return HttpResponse("Нет такого профстандарта")  
    else:
        return render(request, 'services/search-profstandart.html')    
        
    




##################
