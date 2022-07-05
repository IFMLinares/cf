from turtle import width
from django import forms
from pkg_resources import require
from requests import request
from ..models import BillingAddress, Address

class CheckoutForm(forms.Form):
    directionforms = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Dirección', 'required':True, 
    }))
    CodeLocation = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Código Postal','required':True,
    }))
    Province = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Provincia','required':True, 
    }))
    district = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Distrito','required':True, 
    }))
    # CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)
    # country = forms.ChoiceField(widget=forms.Select(attrs={
    #     'class':'nice-select nice-select-style-3 cart-tax-select'
    # }), choices=CHOICES)
    # street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
    #     'placeholder':'Dirección',
    # }))
    # apartment_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
    #     'placeholder':'Apartamento', 'class':'street-first form-control'}))
    # postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
    #     'placeholder':'Código postal'
    # }))
    save = forms.BooleanField(required=False)
    same_shipping_address = forms.BooleanField(required=False)

class CheckoutForm1(forms.Form):
    directionforms1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Dirección', 
    }))
    CodeLocation1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Código Postal',
    }))
    Province1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Provincia',
    }))
    district1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Distrito',
    }))
    save1 = forms.BooleanField(required=False)
