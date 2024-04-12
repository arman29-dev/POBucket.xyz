from django import forms
from .models import Buyer


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ('fullname', 'email', 'phone', 'password')