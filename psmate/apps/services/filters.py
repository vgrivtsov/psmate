from psmate.models import Psinfo, Jobtitles, OtraslList
from django import forms
import django_filters

class JTsearchFilter(django_filters.FilterSet):
    #nameps = django_filters.CharFilter(lookup_expr='icontains')


    # psregnum = django_filters.NumberFilter(name='psregnum')
    # psdateappr = django_filters.NumberFilter(name='psdateappr', lookup_expr='year')
    #


    # psdateappr = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(),
    #     widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Jobtitles
        fields = ['jobtitle', 'psregnum']

class JTsort(django_filters.FilterSet):
    class Meta:
        model = Jobtitles
        fields = ['jobtitle', 'psregnum']