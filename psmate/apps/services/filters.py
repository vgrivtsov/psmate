from psmate.models import Psinfo
from django import forms
import django_filters

class PSFilter(django_filters.FilterSet):
    nameps = django_filters.CharFilter(lookup_expr='icontains')
    psregnum = django_filters.NumberFilter(name='psregnum')
    psdateappr = django_filters.NumberFilter(name='psdateappr', lookup_expr='year')



    # psdateappr = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Psinfo
        fields = ['nameps', 'psregnum', 'psdateappr']
        
