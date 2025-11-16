'''from django import forms
from .models import Voter

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your full name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Your email'}),
        }

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter OTP'}))'''
from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'})
    )
    email = forms.EmailField(
        label="Gmail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your registered Gmail'})
    )

class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter OTP'})
    )
