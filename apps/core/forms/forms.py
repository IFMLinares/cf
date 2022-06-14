from turtle import width
from django import forms
from pkg_resources import require

PAYMENT_OPTIONS = (
    ('W','WebPay'),
)

class CheckoutForm(forms.Form):
    CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)
    country = forms.ChoiceField(widget=forms.Select(attrs={
        'class':'nice-select nice-select-style-3 cart-tax-select'
    }), choices=CHOICES)
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Dirección',
    }))
    apartment_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Apartamento', 'class':'street-first form-control'}))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Código postal'
    }))
    save = forms.BooleanField(required=False)
