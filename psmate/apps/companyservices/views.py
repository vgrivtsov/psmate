from django.shortcuts import render
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, ListView, View, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from psmate.models import Enterprises
from psmate.apps.companyservices.forms import CompanyRegisterForm, CompanySettingsForm


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



class OrgProfileView(ListView):

    template_name = 'companyservices/organization-profile.html'
    model = User
    #success_url = "/organization-profile/"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     slug = self.kwargs['slug']
    # 
    #     return context



    def get(self, request, *args, **kwargs):
        
        user = self.request.user
        company_id = self.kwargs['id']
        try:
            company = Enterprises.objects.filter(id=company_id)[0]
        except IndexError:
            company = 'null'
        return render(request, self.template_name, {'company' : company})  


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