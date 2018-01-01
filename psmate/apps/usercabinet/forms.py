from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True,label="Имя")
    last_name = forms.CharField(max_length=30, required=True, label="Фамилия")    
    

    class Meta:
        model = User
        fields = ("email", 'first_name', 'last_name', "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)

        user.email = self.cleaned_data["email"]
        # write email to username
        user.username = user.email

        if commit:
            user.save()
        # fill profiles table
        user.profiles.email= self.cleaned_data["email"]
        user.profiles.fl_name= self.cleaned_data["first_name"]
        user.profiles.fl_fam= self.cleaned_data["last_name"]
        user.profiles.resume = '[]'
        user.profiles.save()


class ProfileSettingsForm(ModelForm):

    fl_otch = forms.CharField(max_length=30, required=False, label="Отчество")
    fl_tlph_mob = forms.CharField(max_length=30, required=False, label="Моб. номер") 

    class Meta:
        model = User

        fields = ( 'email', 'last_name', 'first_name', 'fl_otch', 'fl_tlph_mob')

    def __init__(self, user, *args, **kwargs):
        
        
        # get values from current user extended model to form field
        self.user = user
            
        instance = kwargs.get('instance', None)
        
        kwargs.update(initial={
             'fl_otch': user.profiles.fl_otch,
             'fl_tlph_mob': user.profiles.fl_tlph_mob
           
        })        
        
        
        super(ProfileSettingsForm, self).__init__(*args, **kwargs)


    def save(self, commit=True):
        user = super(ProfileSettingsForm, self).save(commit=False)

        user.email = self.cleaned_data["email"]
        # write email to username
        user.username = user.email

        if commit:
            user.save()
        # fill profiles table
        user.profiles.email= self.cleaned_data["email"]
        user.profiles.fl_name= self.cleaned_data["first_name"]
        user.profiles.fl_fam= self.cleaned_data["last_name"]
        user.profiles.fl_otch= self.cleaned_data["fl_otch"]
        user.profiles.fl_tlph_mob= self.cleaned_data["fl_tlph_mob"]
        user.profiles.resume = '[]'
        user.profiles.save()
    
        