from dal import autocomplete
from django import forms
from psmate.models import *
from django.contrib.auth.models import User

class SearchPsForm(forms.ModelForm):
    
    class Meta:
        model = Psinfo
        fields = ['nameps']
        widgets = {
            'nameps': autocomplete.Select2('profstandart-autocomplete',
                                                attrs={
                                                # Set some placeholder
                                                'data-placeholder': 'Введите слово из названия ПС',
                                                #autfocus
                                                'autofocus':'autofocus',
                                                # Only trigger autocompletion after 2 characters have been typed
                                                #'data-minimum-input-length': 2,                                                
        
                                            },                                 
                                            )
                }
        


class CvGenForm(forms.ModelForm):

    resume = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:
        
        model = User
        fields = ('resume', )

    def __init__(self, *args, **kwargs):

        super(CvGenForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super(CvGenForm, self).save(commit=False)

        if commit:
            user.save()

        user.profiles.resume = self.cleaned_data['resume']
        user.profiles.save()




