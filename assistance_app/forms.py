from django import forms

from .models import Assistance, AssistanceType


class AssistanceForm(forms.Form):
    victim_number = forms.IntegerField(min_value=1,initial=1)
    assistance_type = forms.ModelChoiceField(queryset=AssistanceType.objects.all(),limit_choices_to=1)
    remark = forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control'}))

