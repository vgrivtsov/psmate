from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from psmate.models import Users

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
        # fill users table
        user.users.email= self.cleaned_data["email"]
        user.users.resume = '[]'
        user.users.save()
