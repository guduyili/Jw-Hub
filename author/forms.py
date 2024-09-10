from django import forms
from django.contrib.auth import get_user_model
from .models import CaptchaModel


User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=2,error_messages={
        'register':'Please enter a username',
        "max_length":'The length of the username is between 2~20',
        "min_length":'The length of the username is between 2~20',

    })
    email  = forms.EmailField(error_messages={"required":'Please enter email','invalid':'Please send in a correct email address'})
    captcha = forms.CharField(max_length=4,min_length=4)
    password = forms.CharField(max_length=20,min_length=6)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('The email address has been registered!')
        return email
    

    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        email = self.cleaned_data.get('email')


        captcha_model = CaptchaModel.objects.filter(email=email,captcha=captcha).first()
        if not captcha_model:
            raise forms.ValidationError("The verification code and email address do not match")
        captcha_model.delete()
        return captcha
    

class LoginForms(forms.Form):
   email  = forms.EmailField(error_messages={"required":'Please enter email','invalid':'Please send in a correct email address'})
   password = forms.CharField(max_length=20,min_length=6)
   remember = forms.BooleanField(required=False)