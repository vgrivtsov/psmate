from django import forms
from django.contrib.auth.models import User
from psmate.models import Enterprises

from django.forms import ModelForm


class CompanyRegisterForm(ModelForm):
    CHOICES = (('ПТ', 'ПТ'),
               ('ТНВ','ТНВ'),
               ('ООО','ООО'),
               ('ОДО','ОДО'),
               ('ОАО','ОАО'),
               ('ЗАО','ЗАО'),
               ('ДХО','ДХО'),
               ('ЗХО','ЗХО'),
               ('СПК','СПК'),
               ('РПК','РПК'),
               ('СКХ','СКХ'),
               ('ГКП','ГКП'),
               ('МП', 'МП'),
               ('КФХ','КФХ'),
               ('ПК', 'ПК')
              )

    e_name = forms.CharField(max_length=255, required=True,label="Наименование организации")
    e_op_form = forms.ChoiceField(widget=forms.Select, choices=CHOICES, required=True, label="Организационно-правовая форма")    
    e_director = forms.CharField(max_length=255, required=True,label="Должность руководителя")
    e_fam_ul = forms.CharField(max_length=255, required=True, label="Фамилия руководителя")       
    e_name_ul = forms.CharField(max_length=255, required=True, label="Имя руководителя")  
    e_otch_ul = forms.CharField(max_length=255, required=True, label="Отчество руководителя")  


    class Meta:
        model = Enterprises        
        fields = ("e_name", "e_op_form", "e_director", "e_fam_ul", "e_name_ul", "e_otch_ul")
        exclude = ('regname_id',)

    def __init__(self, user, *args, **kwargs):
        
        self.user = user
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
        company.regname_id= self.user.id

        company.save()


class CompanySettingsForm(ModelForm):

    e_name = forms.CharField(max_length=255, required=True,label="Название компании")
    e_op_form = forms.CharField(max_length=30, required=True, label="Организационно-правовая форма")    
    e_director = forms.CharField(max_length=255, required=True,label="Должность")
    e_fam_ul = forms.CharField(max_length=255, required=True, label="Фамилия")       
    e_name_ul = forms.CharField(max_length=255, required=True, label="Имя")  
    e_otch_ul = forms.CharField(max_length=255, required=True, label="Отчество")  

    class Meta:
        model = Enterprises
        fields = ("e_name", "e_op_form", "e_director", "e_fam_ul", "e_name_ul", "e_otch_ul")



    def __init__(self, *args, **kwargs):
        
        if kwargs.get('company'):
            
            company = kwargs.pop('company', None)

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
                        
            company.save()

        company.e_name = self.cleaned_data["e_name"]
        company.e_op_form = self.cleaned_data["e_op_form"]
        company.e_director = self.cleaned_data["e_director"]
        company.e_fam_ul = self.cleaned_data["e_fam_ul"]
        company.e_name_ul = self.cleaned_data["e_name_ul"]
        company.e_otch_ul  =  self.cleaned_data["e_otch_ul"]

        company.save()
    
        