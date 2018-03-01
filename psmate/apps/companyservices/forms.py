from django import forms
from django.contrib.auth.models import User
from psmate.models import Enterprises

from django.forms import ModelForm


class CompanyRegisterForm(ModelForm):

    e_name = forms.CharField(max_length=255, required=True,label="Название компании")
    e_op_form = forms.CharField(max_length=30, required=True, label="Организационно-правовая форма")    
    e_director = forms.CharField(max_length=255, required=True,label="Имя")
    e_fam_ul = forms.CharField(max_length=255, required=True, label="Фамилия")       
    e_name_ul = forms.CharField(max_length=255, required=True, label="Имя")  
    e_otch_ul = forms.CharField(max_length=255, required=True, label="Отчество")  


    class Meta:
        model = Enterprises
        fields = ("e_name", "e_op_form", "e_director", "e_fam_ul", "e_name_ul", "e_otch_ul")

    def __init__(self, *args, **kwargs):
        super(CompanyRegisterForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        company = super(CompanyRegisterForm, self).save(commit=False)

        if commit:
            company.save()

        company.e_name= self.cleaned_data["e_name"]
        company.e_op_form= self.cleaned_data["e_op_form"]
        company.e_director= self.cleaned_data["e_director"]
        company.e_fam_ul= self.cleaned_data["e_fam_ul"]
        company.e_name_ul= self.cleaned_data["e_name_ul"]
        company.e_otch_ul= self.cleaned_data["e_otch_ul"]

        company.save()


class CompanySettingsForm(ModelForm):

    e_name = forms.CharField(max_length=255, required=True,label="Название компании")
    e_op_form = forms.CharField(max_length=30, required=True, label="Организационно-правовая форма")    
    e_director = forms.CharField(max_length=255, required=True,label="Имя")
    e_fam_ul = forms.CharField(max_length=255, required=True, label="Фамилия")       
    e_name_ul = forms.CharField(max_length=255, required=True, label="Имя")  
    e_otch_ul = forms.CharField(max_length=255, required=True, label="Отчество")  

    class Meta:
        model = Enterprises
        fields = ("e_name", "e_op_form", "e_director", "e_fam_ul", "e_name_ul", "e_otch_ul")



    def __init__(self, *args, **kwargs):
        if kwargs.get('company'):
            user = kwargs.pop('company', None)

            instance = kwargs.get('instance', None)

           
            kwargs.update(initial={
                
                 'e_name' : company.e_name,
                 'e_op_form' : company.e_op_form,
                 'e_director' : companye_director,
                 'e_fam_ul' : company.e_fam_ul,
                 'e_name_ul' : company.e_name_ul,
                 'e_otch_ul' : company.e_otch_ul          
                
            })               
            
            
            
        super(CompanySettingsForm, self).__init__(*args,**kwargs)

    def save(self, commit=True):
        company = super(CompanySettingsForm, self).save(commit=False)


        if commit:
            
            
            user.save()


        company.e_name = self.cleaned_data["e_name"]
        company.e_op_form = self.cleaned_data["e_op_form"]
        company.e_director = self.cleaned_data["e_director"]
        company.e_fam_ul = self.cleaned_data["e_fam_ul"]
        company.e_name_ul = self.cleaned_data["e_name_ul"]
        company.e_otch_ul  =  self.cleaned_data["e_otch_ul"]


        user.profiles.fl_name= self.cleaned_data["first_name"]
        user.profiles.fl_fam= self.cleaned_data["last_name"]
        user.profiles.fl_otch= self.cleaned_data["fl_otch"]
        user.profiles.fl_tlph_mob= self.cleaned_data["fl_tlph_mob"]
        user.profiles.fl_adress_real= self.cleaned_data["fl_adress_real"]
        user.profiles.fl_pd_date= self.cleaned_data["fl_pd_date"]

        user.profiles.save()
    
        