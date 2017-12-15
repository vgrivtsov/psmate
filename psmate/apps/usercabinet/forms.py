from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
#from psmate.models import Users

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
        # fill users table
        user.users.email= self.cleaned_data["email"]
        user.users.fl_name= self.cleaned_data["first_name"]
        user.users.fl_fam= self.cleaned_data["last_name"]
        user.users.resume = '[]'
        user.users.save()
