from dal import autocomplete
from django import forms
from psmate.models import OtraslList


# class SearchPsForm(forms.ModelForm):
#     model = Profiles
#   
#     
#     class Meta:
#         widgets = {
#                 'email': autocomplete.ModelSelect2(url='search-profstandart')
#         }
        

# class SearchPsForm(forms.ModelForm):
#     name = forms.ModelChoiceField(
#         queryset=OtraslList.objects.all(),
#         widget=autocomplete.ModelSelect2(url='profstandart-autocomplete')
#     )
# 
#     class Meta:
#         model = OtraslList
#         fields = ('name', )

class SearchPsForm(autocomplete.FutureModelForm):
    
    #first_name = forms.CharField(max_length=30, required=True,label="Имя")
    
    class Meta:
        model = OtraslList
        fields = ('__all__')
        widgets = {
            'name': autocomplete.ListSelect2('profstandart-autocomplete')
        }
