from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.models import Enterprises, Departs, Jobtitles
from psmate.apps.services.views import ShowJTlist, JTDetailsView, OfficialInstructions

from psmate.apps.companyservices.forms import OrgCreateForm, OrgUpdateForm
from psmate.apps.companyservices.forms import DepartCreateForm, DepartUpdateForm
from django.http import Http404
from django.contrib import messages

from psmate.models import *

from time import time
from operator import itemgetter
import pymorphy2
from pymorphy2 import units
import pytils
from django.views.generic.detail import SingleObjectMixin


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


class OIsearchJTView(ShowJTlist):

    template_name = "companyservices/jobtitles-list.html"

    def get_context_data(self, **kwargs):
        context = super(OIsearchJTView, self).get_context_data(**kwargs)
        
        companyid = self.kwargs['id']
        departid = self.kwargs['pk']        
        
        context['cmpd'] =  {'companyid' : companyid, 'departid' : departid}
        
        return context    


class OIJTDetailsView(JTDetailsView):

    template_name = "companyservices/jobtitle-details.html"
    model = Jobtitles
    
    def get(self, request, *args, **kwargs):
        
        jt_slug =  self.kwargs['slug']

        companyid = self.kwargs['id']
        departid = self.kwargs['pk']        
        
        cmpd = {'companyid' : companyid, 'departid' : departid}
        if jt_slug:

            jt = Jobtitles.objects.filter(slug=jt_slug)

            ps = Psinfo.objects.filter(id=jt[0].ps_id)
            educationalreqs = Educationalreqs.objects.filter(gtf_id=jt[0].gtf_id)
            reqworkexperiences = Reqworkexperiences.objects.filter(gtf_id=jt[0].gtf_id)
            specialconditions = Specialconditions.objects.filter(gtf_id=jt[0].gtf_id)
            othercharacts = Othercharacts.objects.filter(gtf_id=jt[0].gtf_id)
            tfs = Tfinfo.objects.filter(gtf_id=jt[0].gtf_id)
            
            otrasl = ps[0].otraslid

            jtresult = {'id' : jt[0].id,
                        'slug' : jt[0].slug,
                        'jobtitle' : jt[0].jobtitle,
                        'nameotf' : jt[0].nameotf,
                        'pspurposekind' : ps[0].pspurposekind,
                        'nameps' : ps[0].nameps, 'psregnum' : ps[0].psregnum, 'psid' : ps[0].id,
                        'otraslname' : otrasl.name,
                        'otraslicon' : otrasl.icon,
                        'educationalreqs' : educationalreqs,
                        'reqworkexperiences' : reqworkexperiences,
                        'specialconditions' : specialconditions,
                        'othercharacts' : othercharacts,
                        'tfs' : tfs,
                        'companyid' : companyid,
                        'departid' : departid

                        }
                

            return render(request, self.template_name, {'jtresult': jtresult})

    
class OICreateView(OfficialInstructions):
 
    template_name = "companyservices/official-instructions.html"

