try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

import json
from django.shortcuts import render
from django.views.generic import FormView, ListView, View, UpdateView
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.forms import SearchPsForm, CvGenForm 
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
            psregnum = ps_get[0].psregnum
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

class CvEditView(UpdateView):

    form_class = CvGenForm
    template_name = 'services/generator-cv-resume.html'
    model = User
    # success_url = None

    def get_object(self, queryset=None):

        user = self.request.user
        
        if user.profiles.fl_tlph_mob == None: # if user not set settings
            user.profiles.fl_tlph_mob = ''
        if user.profiles.fl_otch == None:
            user.profiles.fl_otch = ''
        if user.profiles.fl_pd_date == None:
            user.profiles.fl_pd_date = ''
        if user.profiles.fl_adress_real == None:
            user.profiles.fl_adress_real = ''            
            

        return user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CvEditView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(CvEditView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('presentation-cv-resume')    


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

        data = self.request.GET.getlist('psvars', None)
        
        if data != None:
            
            tf_get_raw = Tfinfo.objects.filter(psregnum=data[0])
            otf_get_raw = Jobtitles.objects.filter(jobtitle=data[1]) # get OTF by jobtitle
            otflist = []
            maintfresult = []
            
            for otf in otf_get_raw:
                
                otflist.append(otf.nameotf)

            for tf in tf_get_raw: # select TF only for selected jobtitle (used in color sheme in generator-cv)
                print(tf.nametf)

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

                #dynamic  mdbootstrap class for TF matched of JT:
                

                tfsel = ''
                if tf.nameotf in otflist: 

                    tfsel = 'card info-color white-text mb-0 z-depth-2'

                maintfresult.append({'id' : tf.id, 'codetf' : tf.codetf,
                                     'nametf' : tf.nametf, 'tfsel' : tfsel, # tfcell use for color ligth of jobtitels tf's
                                     'laboractions' : laresult,
                                     'necessaryknowledges' : nkresult,
                                     'requiredskills' : rsresult,
                                     'othercharacteristics' : ocresult,

                                     })

                
            return JsonResponse(maintfresult, safe=False) 

#####################


#### Load CV ########


class LoadCV(View):

    def get(self, request, *args, **kwargs):

        usercv = self.request.user.profiles.resume

        return JsonResponse(usercv, safe=False) 


###CV Presentation###

class CvPresentView(ListView):

    template_name = 'services/presentation-cv-resume.html'
    model = User
   
    def get_context_data(self, **kwargs):

        udata = super(CvPresentView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.profiles.fl_tlph_mob == None: # if user not set settings
            user.profiles.fl_tlph_mob = ''
        if user.profiles.fl_otch == None:
            user.profiles.fl_otch = ''
        if user.profiles.fl_pd_date == None:
            user.profiles.fl_pd_date = ''
        if user.profiles.fl_adress_real == None:
            user.profiles.fl_adress_real = ''             
 
        cv =user.profiles.resume # get resume - JSONb field

        cvcleared = []

        key,value = 'selected', True
        for i in cv:

            quali = []
            
            for s in i['Quali'] :
      
                tf_arr = [] 
                la_arr = [] 
                rs_arr = [] 
                nk_arr = []
                oc_arr = []
                # found and append only selected competences in cv
                for tf in s['FL_cv_TF']:
                    
                    if key in tf and value == tf[key]:
                        tf_arr.append({'nametf' : tf['nametf'], 'codetf' : tf['codetf']})
                        # append if tf_arr != []
                         
                    for la in tf['laboractions'] :
                        if key in la and value == la[key]:
                            la_arr.append({'laboraction' : la['laboraction']})
                            
                    for rs in tf['requiredskills'] :
                        if key in rs and value == rs[key]:
                            rs_arr.append({'requiredskill' : rs['requiredskill']})
                            
                    for nk in tf['necessaryknowledges'] :
                        if key in nk and value == nk[key]:
                            nk_arr.append({'necessaryknowledge' : nk['necessaryknowledge']})                            
                
                    for oc in tf['othercharacteristics'] :
                        if key in oc and value == oc[key]:
                            oc_arr.append({'othercharacteristic' : oc['othercharacteristic']})

                quali.append({ 'PS' :s['FL_cv_PS'],
                               'Otrasl' :s['FL_cv_Otrasl'],
                               'tf' : tf_arr,
                               'la' : la_arr,
                               'rs' : rs_arr,
                               'nk' : nk_arr,
                               'oc' : oc_arr
                            })
            
            cvcleared.append(
                            {'companyname' : i['FL_cv_companyName'],
                            'startdate' :   i['FL_cv_WorkStartDate'],
                            'enddate' :     i['FL_cv_WorkEndDate'],
                            'keyskills' :    i['KeySkills'],
                            'quali' : quali})
                   
            
        return {'cvcleared' :cvcleared} 




