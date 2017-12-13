from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from psmate.models import Users


# class UserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')
# 
# class ProfileForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         # magic 
#         self.user = kwargs.user
#         user_kwargs = kwargs.copy()
#         user_kwargs['instance'] = self.user
#         self.uf = UserForm(*args, **user_kwargs)
#         # magic end 
# 
#         super(ProfileForm, self).__init__(*args, **kwargs)
# 
#         self.fields.update(self.uf.fields)
#         self.initial.update(self.uf.initial)
#          
#         # define fields order if needed
#         self.fields.keyOrder = (
#             'fl_fam',
#         )
# 
#     def save(self, *args, **kwargs):
#         # save both forms   
#         self.uf.save(*args, **kwargs)
#         return super(ProfileForm, self).save(*args, **kwargs)
# 
#     class Meta:
#         model = Users
#         fields = "__all__"


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')    
    
    
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


class ProfileForm(forms.ModelForm):
    
    surname =  forms.CharField(max_length=255, required=False, help_text='Optional.')
    
    class Meta:
        model = Users
        fields = ["fl_fam", ]
        
        