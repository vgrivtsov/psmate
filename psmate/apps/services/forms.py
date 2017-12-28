from dal import autocomplete
from django import forms
from psmate.models import *


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
        
