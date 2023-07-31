from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList


class SigninPageForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField()
    email2 = forms.EmailField(label='confirm email')
    password = forms.CharField()
    Username = forms.CharField(required=True,label='Username/Handle')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            print(field)
            default_css_class = 'form-control'
            new_attrs = {
                "class": default_css_class,
                "placeholder": f"{field}",
            }
            if field == 'email2':
                new_attrs['placeholder'] = f"Confirm your email" 
            self.fields[field].widget.attrs.update(new_attrs)
       
   
    def clean(self):
        data = self.cleaned_data
        email = data.get("email")
        email2 = data.get("email2")
        if email2 != email:
            self.add_error('email', "Your emails must match!")
        return data



   
