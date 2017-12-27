from dal import autocomplete
from django import forms
from psmate.models import *


class SearchPsForm(forms.ModelForm):
    
    #first_name = forms.CharField(max_length=30, required=True,label="Имя")
    # nameps = forms.ModelChoiceField(
    #     queryset=Psinfo.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='profstandart-autocomplete')
    # )    
    class Meta:
        model = Psinfo
        fields = ['nameps']
        widgets = {
            'nameps': autocomplete.Select2('profstandart-autocomplete',
                                                attrs={
                                                # Set some placeholder
                                                'data-placeholder': 'Поиск профстандарта по названию',
                                                #autfocus
                                                'autofocus':'autofocus',
                                                # Only trigger autocompletion after 2 characters have been typed
                                                #'data-minimum-input-length': 2,
        
                                            },                                 
                                            )
                }
        
