try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

import json
from django.shortcuts import render
from django.views.generic import FormView, ListView, View, UpdateView
from dal import autocomplete
from psmate.models import *
from psmate.apps.services.forms import SearchPsForm, CvGenForm, GetJTlistForm
###
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from time import time


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


class CvEditView(LoginRequiredMixin, UpdateView):
    
    template_name = 'services/generator-cv-resume.html'
    login_url = '/'
    permission_denied_message = 'Необходима авторизация!' 
    form_class = CvGenForm
    
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

    def form_valid(self, form):
        self.object = self.get_object()
    
        return super(CvEditView, self).form_valid(form) 


class LoadPS(View):

    def get(self, request, *args, **kwargs):

        data = self.request.GET.get('id', None)
        
        if data != None:
            ps_get = Psinfo.objects.filter(otraslid_id=data)            
            jtresult = []
            
            for ps in ps_get:
                
                jt_get = Jobtitles.objects.filter(ps_id=ps.id).distinct('jobtitle')
                
                for jt in jt_get:

                    jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle,
                                     # 'pspurposekind' : ps.pspurposekind,
                                     'nameps' : ps.nameps, 'psregnum' : ps.psregnum,
                                     'ps_id' : ps.id,
                                     'pspurposekind' : ps.pspurposekind})
  
            return JsonResponse(jtresult, safe=False) 


class LoadCompt(View):

    def get(self, request, *args, **kwargs):
        
        t0 = time()

        data = self.request.GET.getlist('psvars', None)

        if data != None:
            
            tf_get_raw = Tfinfo.objects.filter(ps_id=data[0])

            otf_get_raw = Jobtitles.objects.filter(id=data[1]) # get OTF by jobtitle
            print(otf_get_raw)
            otflist = []
            maintfresult = []
            
            for otf in otf_get_raw:

                otflist.append(otf.gtf_id)
                print(otf)

            for tf in tf_get_raw: # select TF only for selected jobtitle (used in color sheme in generator-cv)

                laresult = []
                nkresult = []
                rsresult = []
                ocresult = []
                
                la_get_raw = Tf_la.objects.filter(tf_id=tf.id)
                nk_get_raw = Tf_rs.objects.filter(tf_id=tf.id)
                rs_get_raw = Tf_nk.objects.filter(tf_id=tf.id)
                oc_get_raw = Tf_oc.objects.filter(tf_id=tf.id)
               
                for la in la_get_raw:
                    laresult.append({'id' : la.id, 'laboraction' : la.laboraction})
                    
                for nk in nk_get_raw:
                    nkresult.append({'id' : nk.id, 'necessaryknowledge' : nk.requiredskill}) # !!!Swap with RS becouse rosmintrud edition!!!
                    
                for rs in rs_get_raw:
                    rsresult.append({'id' : rs.id, 'requiredskill' : rs.necessaryknowledge}) #  # !!!Swap with NK becouse rosmintrud edition!!!                     
                    
                for oc in oc_get_raw:
                    ocresult.append({'id' : oc.id, 'othercharacteristic' : oc.othercharacteristic})  
                 
                # time test 
                t1 = time()
                time_res = t1 - t0
                print(time_res)

                #dynamic  mdbootstrap class for TF matched of JT:


                tfsel = ''
                if tf.gtf_id in otflist: 

                    tfsel = 'card info-color white-text mb-0 py-2 z-depth-2'

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


###Get competences - search from index.html###


###Autocompete###
# class SearchJtAuto(autocomplete.Select2QuerySetView):
#      def get_queryset(self):
# 
#         qs = Jobtitles.objects.all()
# 
#         if self.q:
# 
# 
#             qs = qs.filter(jobtitle__icontains=self.q) # icontains - Case-insensitive
#            
# 
#         return qs
# 
# 
# 
# class SearchJtView(FormView):
#     model = Jobtitles
#     form_class = SearchJtForm
#     template_name = 'index.html'    
#     success_url = None

class SearchJT(FormView):
    template_name = 'index.html'
    form_class = GetJTlistForm

    def form_valid(self, form):
        jobtitle = form.cleaned_data.get('jobtitle')

        return redirect('search-jobtitles', jobtitle)


class ShowJTlist(ListView):
    # services/jobtitles-list.html
    template_name = 'services/jobtitles-list.html'
    model = Jobtitles
    #form_class = GetJTlistForm

   
    def get(self, request, *args, **kwargs):

        jt = self.request.GET.get('jt', None)

        # if jt = None:
        #     print("NONE!!!")
        #     return search-jobtitles
        
        if jt:
            
            jtresult = []
            jt_get = Jobtitles.objects.filter(jobtitle__icontains=jt).distinct('id')
            for jt in jt_get:
                #print(jt.jobtitle)
                ps = Psinfo.objects.filter(psregnum=jt.psregnum)
                
                otrasl = ps[0].otraslid
                

                
                jtresult.append({'id' : jt.id, 'jobtitle' : jt.jobtitle, 'nameotf' : jt.nameotf,
                                 # 'pspurposekind' : ps.pspurposekind,
                                 'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum,
                                 'otraslname' : otrasl.name,
                                 'otraslicon' : otrasl.icon},
                    )
                
            return render(request, self.template_name, {'jtresult': jtresult,
                                                                                                          
                                                        })
        
        
class JTDetailsView(ListView):

    template_name = 'services/jobtitle-details.html'
    model = Jobtitles

    
    def get(self, request, *args, **kwargs):
        
        jt_id =  self.kwargs['id'] 

        if jt_id:

            jt = Jobtitles.objects.filter(id=jt_id)

            ps = Psinfo.objects.filter(psregnum=jt[0].psregnum)
            educationalreqs = Educationalreqs.objects.filter(nameotf=jt[0].nameotf)
            reqworkexperiences = Reqworkexperiences.objects.filter(nameotf=jt[0].nameotf)
            specialconditions = Specialconditions.objects.filter(nameotf=jt[0].nameotf)
            othercharacts = Othercharacts.objects.filter(nameotf=jt[0].nameotf)
            tfs = Tfinfo.objects.filter(nameotf=jt[0].nameotf)
            
            otrasl = ps[0].otraslid
            
            
            
            
            jtresult = {'id' : jt[0].id,
                        'jobtitle' : jt[0].jobtitle,
                        'nameotf' : jt[0].nameotf,
                        'pspurposekind' : ps[0].pspurposekind,
                        'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum,
                        'otraslname' : otrasl.name,
                        'otraslicon' : otrasl.icon,
                        'educationalreqs' : educationalreqs,
                        'reqworkexperiences' : reqworkexperiences,
                        'specialconditions' : specialconditions,
                        'othercharacts' : othercharacts,
                        'tfs' : tfs,
                        
                        }
                

            return render(request, self.template_name, {'jtresult': jtresult,
                                                                                                          
                                                        })
        
        
class OfficialInstructions(ListView):

    template_name = 'services/official-instructions.html'
    model = Jobtitles


    def get(self, request, *args, **kwargs):
        
        t0 = time()

        data =  self.kwargs['id'] 
        
        if data != None:
            
            jt = Jobtitles.objects.filter(id=data)

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id)
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id)
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id)
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id)
            tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
          
            otrasl = ps[0].otraslid

            generaldatas = []
            requirements =[]
            
            generaldatas = {
                
                    'jobtitleid' : jt[0].id,
                    'jobtitle' : jt[0].jobtitle,
                    'nameotf' : jt[0].nameotf,
                    'pspurposekind' : ps[0].pspurposekind,
                    'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum,
                    'otraslname' : otrasl.name,
                    'otraslicon' : otrasl.icon,
                    'educationalreqs' : educationalreqs,
                    'reqworkexperiences' : reqworkexperiences,
                    'specialconditions' : specialconditions,
                    'othercharacts' : othercharacts,
                    'tfs' : tfs,
                    }
            
            for tf in tfs: # select TF only for selected jobtitle
                
                laresult = []
                nkresult = []
                rsresult = []
                ocresult = []

                la_get_raw = Tf_la.objects.filter(tf_id=tf.id)
                nk_get_raw = Tf_rs.objects.filter(tf_id=tf.id)
                rs_get_raw = Tf_nk.objects.filter(tf_id=tf.id)
                oc_get_raw = Tf_oc.objects.filter(tf_id=tf.id)
                print(la_get_raw)
                for la in la_get_raw:
                    laresult.append({'id' : la.id, 'laboraction' : la.laboraction})
                    
                for nk in nk_get_raw:
                    nkresult.append({'id' : nk.id, 'necessaryknowledge' : nk.requiredskill}) # !!!Swap with RS becouse rosmintrud edition!!!
                    
                for rs in rs_get_raw:
                    rsresult.append({'id' : rs.id, 'requiredskill' : rs.necessaryknowledge}) #  # !!!Swap with NK becouse rosmintrud edition!!!                     
                    
                for oc in oc_get_raw:
                    ocresult.append({'id' : oc.id, 'othercharacteristic' : oc.othercharacteristic})  
                 
                # time test 
                t1 = time()
                time_res = t1 - t0
                print(time_res)

                requirements.append({'id' : tf.id, 'codetf' : tf.codetf,
                                     'nametf' : tf.nametf,
                                     'laboractions' : laresult,
                                     'necessaryknowledges' : nkresult,
                                     'requiredskills' : rsresult,
                                     'othercharacteristics' : ocresult,

                                     })



            
            return render(request, self.template_name, {'generaldatas': generaldatas,
                                                        'requirements' : requirements
                                                        })