from django import forms
from .models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):

    password=forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))

    confirm_password=forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
        'class':'form-control'
    }))

    class Meta:

        model=User
        fields=["first_name","last_name","email","phone_number","password"]

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)

        self.fields["email"].help_text="enter email @"
        self.fields["first_name"].label=''
        self.fields["last_name"].label=''
        self.fields["email"].label=''
        self.fields["phone_number"].label=''
        self.fields["phone_number"].widget_attrs={
            "placeholder":'phon'}


    def clean(self) :
        cleaned_data= super(SignUpForm,self).clean()

        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        if password!=confirm_password:
            
            raise forms.ValidationError("Password  Does not Match")
            
        return cleaned_data