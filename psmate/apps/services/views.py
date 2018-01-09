try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

import json
from django.shortcuts import render
from django.views.generic import FormView, ListView, View
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.forms import SearchPsForm
###
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers

### Search PS ###

class SearchPsAuto(autocomplete.Select2QuerySetView):
     def get_queryset(self):
         # if not self.request.user.is_authenticated(): 
         #       return User.objects.none() 
        qs = Psinfo.objects.all()

        if self.q:

            qs = qs.filter(nameps__icontains=self.q) # icontains - Case-insensitive

        return qs
    

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
            
            tfinfo = Tfinfo.objects.filter(psregnum=psregnum).distinct('codetf') # dinstinct delete doubles
            otfinfo = Gtfinfo.objects.filter(psregnum=psregnum).distinct('codeotf')
            okzinfo = Okz.objects.filter(psregnum=psregnum).distinct('codeokz')
            okvedinfo = Okved.objects.filter(psregnum=psregnum).distinct('codeokved')
            
            mixed_tf_otf = []
            
            # for OTF -TF dividing in table used nex list:
            # [[otf1,[tf1, tf2]],[otf2,[tf1, tf2]]]
            for otf in otfinfo:
                mixed_tf = []
                
                for tf in tfinfo:
                    if tf.nameotf == otf.nameotf:
                        mixed_tf.append(tf)
                
                mixed_tf_otf.append([otf, mixed_tf])

            return render(request, self.template_name, {'psinfo': psinfo,
                                                        'mixed_tf_otf': mixed_tf_otf,
                                                        'okzinfo': okzinfo,
                                                        'okvedinfo': okvedinfo,
                                                        'ngshow' : 'true', # ng-show for id="showps
                                                        'form': form})
        return render(request, self.template_name, {'form': form})

##################

###CV generator###

class CvEditView(FormView):

    form_class = SearchPsForm
    template_name = 'services/generator-cv-resume.html'
    success_url = None
    queryset = User.objects.filter()
    

    # def dispatch(self, *args, **kwargs):
    #     """Use this to check for 'user'."""
    #     if self.request.session.get('user'):
    #         return redirect('/')
    #     return super(CvEditView, self).dispatch(*args, **kwargs)


    # def get_context_data(self, **kwargs):
    #     context = super(CvEditView, self).get_context_data(**kwargs)
    #     context['user'] = self.queryset
    #     context['psinfo'] = Psinfo.objects.filter(psregnum=204)
    #     context['eks'] = Eks.objects.filter(psregnum=204)
    #     context['jobtitles'] = Jobtitles.objects.filter(psregnum=204)
    #     return context


class LoadPS(View):

    def get(self, request, *args, **kwargs):

        data = self.request.GET.get('id', None)
        
        if data != None:
            ps_get = Psinfo.objects.filter(otraslid_id=data)            
            jtresult = []
            
            for ps in ps_get:
                
                jt_get = Jobtitles.objects.filter(psregnum=ps.psregnum).distinct('jobtitle')
                
                for jt in jt_get:

                    jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle,
                                     # 'pspurposekind' : ps.pspurposekind,
                                     'nameps' : ps.nameps, 'psregnum' : ps.psregnum,
                                     'pspurposekind' : ps.pspurposekind})
  
            return JsonResponse(jtresult, safe=False) 


class LoadCompt(View):

    def get(self, request, *args, **kwargs):

        data = self.request.GET.get('id', None)
        
        if data != None:
            tf_get_raw = Tfinfo.objects.filter(psregnum=data)
            # la_get_raw = Tf_la.objects.filter(psregnum=data).distinct('laboraction')
            # la_get_raw = Tf_la.objects.filter(psregnum=data).distinct('laboraction')
            # la_get_raw = Tf_la.objects.filter(psregnum=data).distinct('laboraction')
            
            maintfresult = []
            

            for tf in tf_get_raw:
                # laboractions, necessary knowleges, required skills, other characteristics
                laresult = []
                nkresult = []
                rsresult = []
                ocresult = []

                la_get_raw = Tf_la.objects.filter(nametf=tf.nametf)
                nk_get_raw = Tf_rs.objects.filter(nametf=tf.nametf)
                rs_get_raw = Tf_nk.objects.filter(nametf=tf.nametf)
                oc_get_raw = Tf_oc.objects.filter(nametf=tf.nametf)
                                
                for la in la_get_raw:
                    laresult.append({'id' : la.id, 'laboraction' : la.laboraction})
                    
                for nk in nk_get_raw:
                    nkresult.append({'id' : nk.id, 'necessaryknowledge' : nk.requiredskill}) # !!!Swap with RS becouse rosmintrud edition!!!
                    
                for rs in rs_get_raw:
                    rsresult.append({'id' : rs.id, 'requiredskill' : rs.necessaryknowledge}) #  # !!!Swap with NK becouse rosmintrud edition!!!                     
                    
                for oc in oc_get_raw:
                    ocresult.append({'id' : oc.id, 'othercharacteristic' : oc.othercharacteristic})  
                    
                maintfresult.append({'id' : tf.id, 'codetf' : tf.codetf, 'nametf' : tf.nametf,
                                     'laboractions' : laresult,
                                     'necessaryknowledges' : nkresult,
                                     'requiredskills' : rsresult,
                                     'othercharacteristics' : ocresult,

                                     })

            return JsonResponse(maintfresult, safe=False) 
