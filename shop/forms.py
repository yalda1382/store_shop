#create forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UpdateUserInfo(forms.ModelForm):
    phone=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Phone Number'}),)
    address1=forms.CharField(label='', max_length=255,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address Line 1'}),required=False)
    address2=forms.CharField(label='', max_length=255,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Address Line 2'}),required=False)
    city=forms.CharField(label='', max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter City'}),required=False)
    state=forms.CharField(label='', max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter State'}),required=False)
    zipcode=forms.CharField(label='', max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Zip Code'}),required=False)
    country=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Country'}),required=False)

    class Meta:
        model=Profile
        fields=('phone','address1','address2','city','state','zipcode','country')



    

class UpdatePasswordForm(SetPasswordForm):
    new_password1= forms.CharField(label='', max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control','name':'new_password1','type':'password','placeholder':'Enter New Password'}))
    new_password2= forms.CharField(label='', max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control','name':'new_password2','type':'password','placeholder':'Confirm New Password'})) 
    class Meta:
        model=User
        fields=('new_password1','new_password2')
        
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length=30,
                                 widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}))
    last_name = forms.CharField(label='', max_length=30,
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}))
    email= forms.EmailField(label='', max_length=254,
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}))
    username = forms.CharField(label='', max_length=30,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}))  # ❌ تغییر داده شد
    password1= forms.CharField(label='', max_length=30,
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2= forms.CharField(label='', max_length=30,
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    class Meta:
        model=User
        fields=('first_name','last_name','email','username','password1','password2')  # username

class UpdateUserForm(UserChangeForm):
    password = None  # Hide the password field
    first_name = forms.CharField(label='', max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),required=False)
    last_name = forms.CharField(label='', max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),required=False)
    email= forms.EmailField(label='', max_length=254,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Email'}),required=False) 
    user_name = forms.CharField(label='', max_length=30,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username'}),required=False)
    class Meta:
        model=User
        fields=('first_name','last_name','email','user_name')