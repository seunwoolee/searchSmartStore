from django import forms
from django.forms import TextInput, Textarea
from crispy_forms.helper import FormHelper
from log.models import Log


class SearchForm(forms.ModelForm):

    class Meta:
        model = Log
        fields = ('company_name', 'keywords')
        widgets = {
            'company_name': TextInput(attrs={'class': 'fadeIn second', 'placeholder': '상호명'}),
            'keywords': TextInput(attrs={'class': 'fadeIn third', 'placeholder': '검색어'})
        }
