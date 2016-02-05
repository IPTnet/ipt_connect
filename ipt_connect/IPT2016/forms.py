from django import forms
from models import Participant


# class RegisterForm(forms.ModelForm):
#     class Meta:
#         model = Participant
#         exclude = ('country',)

#class RegisterForm(forms.Form):
#
#    name = forms.CharField(max_length=20)
#
#    surname = forms.CharField(max_length=20)
#
#    email = forms.EmailField(label="Email address")
#
#    veteran = forms.BooleanField(help_text="Have you already participated in the IPT?", required=True)