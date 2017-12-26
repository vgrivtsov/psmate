from dal import autocomplete
from django import forms
from psmate.models import Eks



# class SearchPsForm(forms.ModelForm):
#     nameeks = forms.ModelChoiceField(
#         queryset=Eks.objects.all(),
#         widget=autocomplete.ModelSelect2(url='profstandart-autocomplete',
#                                          attrs={'data-minimum-input-length': 2})
#     )
# 
#     class Meta:
#         model = Eks
#         fields = ('nameeks', )

class SearchPsForm(forms.ModelForm):
    
    #first_name = forms.CharField(max_length=30, required=True,label="Имя")
    
    class Meta:
        model = Eks
        fields = ('nameeks', )
        widgets = {
            'nameeks': autocomplete.Select2('profstandart-autocomplete',
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
