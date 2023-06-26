from django import forms
from .models import PollingUnit

class PollingUnitForm(forms.ModelForm):
    class Meta:
        model = PollingUnit
        fields = '__all__'