from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.models import Enterprises, Departs, Jobtitles
from psmate.apps.companyservices.forms import OrgCreateForm, OrgUpdateForm
from psmate.apps.companyservices.forms import DepartCreateForm, DepartUpdateForm
from django.http import Http404
from django.contrib import messages

################ ORGANIZATIONS VIEWS ###################################################

class OrgCreateView(FormView):
    form_class = OrgCreateForm
    template_name = "companyservices/regform.html"
    success_url = "/cabinet/"

    def get_form_kwargs(self):
        kwargs = super(OrgCreateView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user
    
        return kwargs  

    def form_valid(self, form):

        # create company
        form.save()

        e_name = self.request.POST['e_name']
        e_op_form = self.request.POST['e_op_form']
        e_director = self.request.POST['e_director']
        e_fam_ul = self.request.POST['e_fam_ul']
        e_name_ul = self.request.POST['e_name_ul']
        e_otch_ul = self.request.POST['e_otch_ul']
        regname_id = self.request.user.id

        # call base class method
        return super(OrgCreateView, self).form_valid(form)



class OrgReadView(View):

    template_name = 'companyservices/organization-profile.html'
    model = User


    def get(self, request, *args, **kwargs):
        
        user = self.request.user
        company_id = self.kwargs['id']
        
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404        
        else:
            company = Enterprises.objects.get(pk=company_id)
            departs = Departs.objects.filter(company_id=company_id)

        return render(request, self.template_name, {'company' : company,
                                                    'departs' :departs})  



class OrgUpdateView(UpdateView):
    form_class = OrgUpdateForm
    template_name = 'companyservices/settings.html'
    model = Enterprises


    def get_object(self, queryset=None):

        obj = Enterprises.objects.get(id=self.kwargs['id'])
        return obj


    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        return super(OrgUpdateView, self).get(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        
        return super(OrgUpdateView, self).post(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})    


    def get_form_kwargs(self):
        
        kwargs = super(OrgUpdateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user
        
        # check if company belongs auth user 
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user
    
    
        return kwargs  


    def form_valid(self, form):
        
        self.object = self.get_object()
        return super(OrgUpdateView, self).form_valid(form)
    
    

class OrgDeleteView(DeleteView):
    
    template_name = "companyservices/enterprises_confirm_delete.html"
    success_url = "/cabinet/"


    def get_object(self, queryset=None):
        
        obj = Enterprises.objects.get(pk=self.kwargs['id'])
        return obj


    def get(self, request, *args, **kwargs):
        
        user = self.request.user
        company_id = self.kwargs['id']
        
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404        
        else:
            company = Enterprises.objects.get(pk=company_id)

        return render(request, self.template_name, {'company' : company})


    def get_queryset(self):
        
        user = self.request.user
        company_id =  self.kwargs['id']


        # check if company belongs auth user 
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]
    
        if int(company_id) not in orgs:
            raise Http404
        else:
            return Enterprises.objects.get(pk=company_id)
            

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "Организация %s была удалена" % obj.e_name)
        return super(OrgDeleteView, self).delete(request, *args, **kwargs)      


################ DEPARTS VIEWS ###################################################

    
class DepartCreateView(FormView):
    form_class = DepartCreateForm
    template_name = "companyservices/departregform.html"


    def get_form_kwargs(self):
        
        kwargs = super(DepartCreateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user
        
        # check if company belongs auth user 
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user
    
    
        return kwargs  

        
    def form_valid(self, form):

        # create company
        form.save()

        name = self.request.POST['name']
        cheef = self.request.POST['cheef']
        cheef_fam = self.request.POST['cheef_fam']
        cheef_name = self.request.POST['cheef_name']
        cheef_otch = self.request.POST['cheef_otch']
        phone = self.request.POST['phone']        
        #company_id = self.company_id

        # call base class method
        return super(DepartCreateView, self).form_valid(form)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})  


class DepartUpdateView(UpdateView):
    
    form_class = DepartUpdateForm
    template_name = 'companyservices/departsettings.html'
    model = Departs


    def get_object(self, queryset=None):
        
        obj = Departs.objects.get(id=self.kwargs['pk'])
        return obj
   

    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        return super(DepartUpdateView, self).get(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        
        return super(DepartUpdateView, self).post(request, *args, **kwargs)


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})    


    def get_form_kwargs(self):
        
        kwargs = super(DepartUpdateView, self).get_form_kwargs()
        company_id = self.kwargs['id']
        user = self.request.user
        
        # check if company belongs auth user 
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404
        else:
            kwargs['company'] = Enterprises.objects.get(pk=company_id)

        if user:
            kwargs['user'] = user
    
    
        return kwargs   


    def form_valid(self, form):
        self.object = self.get_object()
        return super(DepartUpdateView, self).form_valid(form)



class DepartDeleteView(DeleteView):
    
    template_name = "companyservices/departs_confirm_delete.html"


    def get(self, request, *args, **kwargs):
        
        user = self.request.user
        company_id = self.kwargs['id']
        dep_id =  self.kwargs['pk']
        
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]

        if int(company_id) not in orgs:
            raise Http404        
        else:
            company = Enterprises.objects.get(pk=company_id)
            department = Departs.objects.filter(id=dep_id)[0]

        return render(request, self.template_name, {'company' : company, 'department' : department }) 


    def get_queryset(self):
        
        user = self.request.user
        company_id =  self.kwargs['id']
        dep_id =  self.kwargs['pk']

        # check if company belongs auth user 
        get_all_orgs = Enterprises.objects.filter(regname_id=user.id)
        orgs = [x.id for x in get_all_orgs]
    
        if int(company_id) not in orgs:
            raise Http404
        else:
            return Departs.objects.filter(id=dep_id)
            

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, "Подразделение %s было удалено" % obj.name)
        return super(DepartDeleteView, self).delete(request, *args, **kwargs)      


    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})  

################### OFFICIAL INSTRUCTIONS VIEW ########################3


class OfficialInstructions(ListView):

    template_name = 'companyservices/depart_official_instructions.html'
    model = Jobtitles


    def get(self, request, *args, **kwargs):
        
        t0 = time()

        data =  self.kwargs['slug'] 
        
        if data != None:
            
            jt = Jobtitles.objects.filter(slug=data)

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id)
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id)
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id)
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id)
            tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
          
            otrasl = ps[0].otraslid

            generaldatas = []
                        
            #make jobtitle Roditelny paezh

            jt_rod = []
            morph = pymorphy2.MorphAnalyzer()
       
            #cut non need padezh string beenween '( )'
            pattern = re.compile("[\(\[].*?[\)\]]")
            if re.findall(pattern, jt[0].jobtitle):
                cuttedstring = re.findall(pattern, jt[0].jobtitle)[0]
            else:
                cuttedstring = ''
            
            cleared_jt = re.sub("[\(\[].*?[\)\]]", "", jt[0].jobtitle)
            
           # print(cuttedstring)
            
            pos_list = ['NOUN', 'ADJF', 'ADJS', 'PRTF', 'PRTS'] 
            case_list = []

            
            for i in cleared_jt.split(' '):
                p = morph.parse(i)[0]
                print(p)
                print(p.inflect({'gent'}))
                if p.tag.POS in pos_list and p.tag.case == 'nomn': # Chast' rechi & padezh

                    #print(jt_rod_word)
                    if p.inflect({'gent'}) :
                        
                        changed_word = p.inflect({'sing', 'gent'}).word
                        if changed_word == 'риска-менеджера':
                            changed_word = 'риск-менеджера'
                        if changed_word == 'бренда-менеджера':
                            changed_word = 'бренд-менеджера'                        
                        if changed_word == 'брэнда-менеджера':
                            changed_word = 'брэнд-менеджера'                         
                        
                        jt_rod.append(changed_word)
                    
                    else:
                        
                        jt_rod.append(i)

                else:
                    jt_rod.append(i)


           # print(jt_rod)
            jobtitlerod = ' '.join(jt_rod) + ' '+cuttedstring
            
            generaldatas = {
                
                    'jobtitleid' : jt[0].id,
                    'jobtitle' : jt[0].jobtitle,
                    'jobtitlerod' : jobtitlerod,
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
            
            laresult = []
            nkresult = []
            rsresult = []
            ocresult = []            
            tfresult = []
            
            for tf in tfs: # select TF only for selected jobtitle

                la_get_raw = Tf_la.objects.filter(tf_id=tf.id)
                nk_get_raw = Tf_rs.objects.filter(tf_id=tf.id)
                rs_get_raw = Tf_nk.objects.filter(tf_id=tf.id)
                oc_get_raw = Tf_oc.objects.filter(tf_id=tf.id)


                tfresult.append({'id' : tf.id, 'codetf' : tf.codetf, 'nametf' : tf.nametf})

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
                #print(time_res)

            requirements = {'tf' : tfresult,
                            'laboractions' : laresult,
                            'necessaryknowledges' : nkresult,
                            'requiredskills' : rsresult,
                            'othercharacteristics' : ocresult,
                            }



            
            return render(request, self.template_name, {'generaldatas': generaldatas,
                                                        'requirements' : requirements
                                                        })