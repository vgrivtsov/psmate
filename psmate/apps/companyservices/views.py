from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.models import Enterprises, Departs
from psmate.apps.companyservices.forms import CompanyRegisterForm, CompanySettingsForm
from psmate.apps.companyservices.forms import DepartRegisterForm, DepartSettingsForm
from django.http import Http404
from django.contrib import messages

class RegisterCompanyFormView(FormView):
    form_class = CompanyRegisterForm
    template_name = "companyservices/regform.html"
    success_url = "/cabinet/"

    def get_form_kwargs(self):
        kwargs = super(RegisterCompanyFormView, self).get_form_kwargs()
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
        return super(RegisterCompanyFormView, self).form_valid(form)



class OrgProfileView(View):

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
        # try:
        #     company = Enterprises.objects.filter(id=company_id)[0]
        # except IndexError:
        #     company = 'null'
        return render(request, self.template_name, {'company' : company,
                                                    'departs' :departs})  






class OrgSettingsView(UpdateView):
    form_class = CompanySettingsForm
    template_name = 'companyservices/settings.html'
    model = User
    success_url = "/organization-profile/"

    def dispatch(self, *args, **kwargs):
        return super(CompanySettingsView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):

        user = self.request.user
        
        return user


    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        return super(CompanySettingsView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        
        return super(CompanySettingsView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('company')    

    def get_form_kwargs(self):
        kwargs = super(CompanySettingsView, self).get_form_kwargs()
        user = self.request.user

        if user:
            kwargs['user'] = user
    
        return kwargs


    def form_valid(self, form):
        self.object = self.get_object()
        return super(CompanySettingsView, self).form_valid(form)
    
    
    
class RegisterDepartFormView(FormView):
    form_class = DepartRegisterForm
    template_name = "companyservices/departregform.html"

    def get_form_kwargs(self):
        kwargs = super(RegisterDepartFormView, self).get_form_kwargs()
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
        return super(RegisterDepartFormView, self).form_valid(form)

    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})  


class DepartSettingsView(UpdateView):
    
    form_class = DepartSettingsForm
    template_name = 'companyservices/departsettings.html'
    model = Departs

    def get_object(self, queryset=None):
        
        obj = Departs.objects.get(id=self.kwargs['pk'])
        return obj
   

    def get(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        return super(DepartSettingsView, self).get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
    
        
        return super(DepartSettingsView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        company_id = self.kwargs['id']
        return reverse_lazy('organization-profile', kwargs={'id': company_id})    

    def get_form_kwargs(self):
        
        kwargs = super(DepartSettingsView, self).get_form_kwargs()
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
        return super(DepartSettingsView, self).form_valid(form)



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


