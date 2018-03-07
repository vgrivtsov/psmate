from django import forms
from django.contrib.auth.models import User
from psmate.models import Enterprises, Departs

from django.forms import ModelForm


################ COMPANY FORMS ###################################################

class OrgRegisterForm(ModelForm):
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
        super(OrgRegisterForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        
        company = super(OrgRegisterForm, self).save(commit=False)


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


class OrgSettingsForm(ModelForm):
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
        

    def __init__(self, company, user, *args, **kwargs):
        
        self.user = user
        self.company_id = company.id
        self.company_name= company.e_name
        self.company_form= company.e_op_form

            
        super(OrgSettingsForm, self).__init__(*args,**kwargs)
        

    def save(self, commit=True):
        company = super(OrgSettingsForm, self).save(commit=False)


        if commit:
                        
            company.save()

        company.e_name = self.cleaned_data["e_name"]
        company.e_op_form = self.cleaned_data["e_op_form"]
        company.e_director = self.cleaned_data["e_director"]
        company.e_fam_ul = self.cleaned_data["e_fam_ul"]
        company.e_name_ul = self.cleaned_data["e_name_ul"]
        company.e_otch_ul  =  self.cleaned_data["e_otch_ul"]
        company.regname_id= self.user.id

        company.save()
    
    
################ DEPART FORMS ###################################################


class DepartRegisterForm(ModelForm):

    name = forms.CharField(max_length=255, required=True,label="Наименование подразделения")
    cheef = forms.CharField(max_length=255, required=False,label="Должность руководителя подразделения")
    cheef_fam = forms.CharField(max_length=255, required=False, label="Фамилия руководителя подразделения")       
    cheef_name = forms.CharField(max_length=255, required=False, label="Имя руководителя подразделения")  
    cheef_otch = forms.CharField(max_length=255, required=False, label="Отчество руководителя подразделения")  
    phone = forms.CharField(max_length=255, required=False, label="Телефон подразделения")    

    class Meta:
        model = Departs        
        fields = ("name", "cheef", "cheef_fam", "cheef_name", "cheef_otch", "phone")
        exclude = ('company_id','company_name','company_form')


    def __init__(self, company, user, *args, **kwargs):
        
        self.company_id = company.id
        self.company_name= company.e_name
        self.company_form= company.e_op_form

        super(DepartRegisterForm , self).__init__(*args, **kwargs)


    def save(self, commit=True):
        
        dep = super(DepartRegisterForm, self).save(commit=False)


        if commit:
            dep.save()

        dep.name= self.cleaned_data["name"]
        dep.cheef= self.cleaned_data["cheef"]
        dep.cheef_fam= self.cleaned_data["cheef_fam"]
        dep.cheef_name= self.cleaned_data["cheef_name"]
        dep.cheef_otch= self.cleaned_data["cheef_otch"]
        dep.phone= self.cleaned_data["phone"]
        dep.company_id= self.company_id

        dep.save()


class DepartSettingsForm(ModelForm):

    name = forms.CharField(max_length=255, required=True,label="Наименование подразделения")
    cheef = forms.CharField(max_length=255, required=False,label="Должность руководителя подразделения")
    cheef_fam = forms.CharField(max_length=255, required=False, label="Фамилия руководителя подразделения")       
    cheef_name = forms.CharField(max_length=255, required=False, label="Имя руководителя подразделения")  
    cheef_otch = forms.CharField(max_length=255, required=False, label="Отчество руководителя подразделения")  
    phone = forms.CharField(max_length=255, required=False, label="Телефон подразделения")   

    class Meta:
        model = Departs        
        fields = ("name", "cheef", "cheef_fam", "cheef_name", "cheef_otch", "phone")
        exclude = ('company_id','company_name','company_form')



    def __init__(self, company, user, *args, **kwargs):
        
        self.company_id = company.id
        self.company_name= company.e_name
        self.company_form= company.e_op_form

        super(DepartSettingsForm , self).__init__(*args, **kwargs)

        
        

    def save(self, commit=True):
        
        dep = super(DepartSettingsForm, self).save(commit=False)


        if commit:
            dep.save()

        dep.name= self.cleaned_data["name"]
        dep.cheef= self.cleaned_data["cheef"]
        dep.cheef_fam= self.cleaned_data["cheef_fam"]
        dep.cheef_name= self.cleaned_data["cheef_name"]
        dep.cheef_otch= self.cleaned_data["cheef_otch"]
        dep.phone= self.cleaned_data["phone"]
        dep.company_id= self.company_id

        dep.save()
            