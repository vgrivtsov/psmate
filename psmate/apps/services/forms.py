from dal import autocomplete
from django import forms
from psmate.models import *


class SearchPsForm(forms.ModelForm):
    
    #first_name = forms.CharField(max_length=30, required=True,label="Имя")
    
    class Meta:
        model = Psinfo
        fields = ('nameps', )
        widgets = {
            'nameps': autocomplete.Select2('profstandart-autocomplete',
                                                attrs={
                                                # Set some placeholder
                                                'data-placeholder': 'Название должности по ЕКС',
                                                #autfocus
                                                'autofocus':'autofocus',
                                                # Only trigger autocompletion after 2 characters have been typed
                                                #'data-minimum-input-length': 2,

                                            },                                 
                                            )
                }

