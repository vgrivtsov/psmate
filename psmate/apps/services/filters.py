from psmate.models import Psinfo
from django import forms
import django_filters
from dal import autocomplete

class PSFilter(django_filters.FilterSet):
    #nameps = django_filters.CharFilter(lookup_expr='icontains')
    
    nameps = django_filters.ModelChoiceFilter(
            label='Received Date Range',
            queryset=Psinfo.objects.all(),
            widget=autocomplete.ModelSelect2(url='profstandart-autocomplete')   
       )
    
    psregnum = django_filters.NumberFilter(name='psregnum')
    psdateappr = django_filters.NumberFilter(name='psdateappr', lookup_expr='year')



    # psdateappr = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Psinfo
        fields = ['nameps', 'psregnum', 'psdateappr']
