from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    shipping_full_name=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name'}),)
    shipping_email=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your email '}),)
    shipping_address1=forms.CharField(label='', max_length=255,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address Line 1'}),required=True)
    shipping_address2=forms.CharField(label='', max_length=255,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address Line 2'}),required=True)
    shipping_city=forms.CharField(label='', max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}),required=True)
    shipping_state=forms.CharField(label='', max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter State'}),required=False)
    shipping_zipcode=forms.CharField(label='', max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Zip Code'}),required=False)
    shipping_country=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Country'}),required=True)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country']
        exclude=['user',]